"""
Enterprise Digital Twin Telemetry Engine for OfficeMate 2.0
Computes operational state, department health, resource bottlenecks, and throughput.
"""

from typing import Dict, Any, List
from db.database import query_all, get_tickets, get_meeting_rooms

def get_department_telemetry() -> Dict[str, Any]:
    """Calculates live operational telemetry for HR, IT, and Admin departments."""
    departments = query_all("SELECT * FROM departments")
    tickets = get_tickets()
    rooms = get_meeting_rooms()

    dept_stats = {}
    for d in departments:
        code = d["code"]
        dept_tickets = [t for t in tickets if t["department_code"] == code]
        open_tickets = [t for t in dept_tickets if t["status"] in ["OPEN", "IN_PROGRESS"]]
        resolved_tickets = [t for t in dept_tickets if t["status"] in ["RESOLVED", "CLOSED"]]
        critical_count = sum(1 for t in open_tickets if t["priority"] in ["HIGH", "CRITICAL"])

        staff = d["active_staff"]
        # Queuing load factor: tickets per staff
        load_factor = len(open_tickets) / max(1, staff)

        # Health score: 100 base, penalized by open backlog and critical tickets
        health = max(10, int(100 - (load_factor * 12) - (critical_count * 15)))

        # Average estimated wait time in minutes
        base_service_time = {"HR": 45, "IT": 25, "ADMIN": 35}.get(code, 30)
        est_wait_min = int(load_factor * base_service_time)

        dept_stats[code] = {
            "department_id": d["id"],
            "name": d["name"],
            "code": code,
            "head": d["head"],
            "staff_count": staff,
            "total_tickets": len(dept_tickets),
            "open_tickets": len(open_tickets),
            "resolved_tickets": len(resolved_tickets),
            "critical_tickets": critical_count,
            "health_score": min(100, health),
            "load_factor": round(load_factor, 2),
            "estimated_wait_time_min": est_wait_min,
            "status": "HEALTHY" if health >= 75 else ("WARNING" if health >= 50 else "CRITICAL")
        }

    # Meeting room utilization
    total_rooms = len(rooms)
    available_rooms = sum(1 for r in rooms if r["is_available"])
    room_utilization = round(((total_rooms - available_rooms) / max(1, total_rooms)) * 100, 1)

    overall_health = int(sum(ds["health_score"] for ds in dept_stats.values()) / max(1, len(dept_stats)))

    return {
        "overall_health_score": overall_health,
        "room_utilization_pct": room_utilization,
        "departments": dept_stats,
        "total_active_backlog": sum(ds["open_tickets"] for ds in dept_stats.values()),
        "total_critical_items": sum(ds["critical_tickets"] for ds in dept_stats.values())
    }

if __name__ == "__main__":
    telem = get_department_telemetry()
    print("Digital Twin Telemetry:")
    print(f"Overall Health: {telem['overall_health_score']}%")
    for k, v in telem["departments"].items():
        print(f"[{k}] Health: {v['health_score']}% | Open: {v['open_tickets']} | Wait: {v['estimated_wait_time_min']}m")
