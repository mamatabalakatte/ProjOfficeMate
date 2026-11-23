"""
What-If Scenario Simulator for OfficeMate 2.0
CSE472 / Section 5 Requirement: Operational Digital Twin
Implements SimPy discrete-event simulation of departmental service queues.
"""

import random
import simpy
from typing import Dict, Any, List

def run_discrete_event_simulation(
    department_code: str = "IT",
    staff_count: int = 8,
    arrival_interval_mean: float = 12.0, # minutes between ticket arrivals
    service_time_mean: float = 35.0,     # minutes to resolve a ticket
    sim_duration_minutes: float = 480.0  # 8-hour workday
) -> Dict[str, Any]:
    """Runs a discrete-event SimPy queuing simulation for a department."""
    random.seed(42)
    env = simpy.Environment()
    staff_resource = simpy.Resource(env, capacity=max(1, staff_count))

    wait_times = []
    service_times = []
    queue_lengths = []

    def ticket_generator(env, staff_res):
        t_id = 0
        while True:
            # Poisson arrival process
            inter_arrival = random.expovariate(1.0 / max(0.5, arrival_interval_mean))
            yield env.timeout(inter_arrival)
            t_id += 1
            env.process(handle_ticket(env, f"T-{t_id}", staff_res))

    def handle_ticket(env, name, staff_res):
        arrive_time = env.now
        queue_lengths.append(len(staff_res.queue))
        with staff_res.request() as req:
            yield req
            wait = env.now - arrive_time
            wait_times.append(wait)
            service_dur = random.expovariate(1.0 / max(1.0, service_time_mean))
            yield env.timeout(service_dur)
            service_times.append(service_dur)

    env.process(ticket_generator(env, staff_resource))
    env.run(until=sim_duration_minutes)

    total_tickets = len(wait_times)
    avg_wait = sum(wait_times) / max(1, total_tickets)
    max_wait = max(wait_times) if wait_times else 0.0
    sla_breaches = sum(1 for w in wait_times if w > 60.0) # wait > 1 hour
    sla_breach_rate = (sla_breaches / max(1, total_tickets)) * 100
    utilization = (sum(service_times) / max(1, (staff_count * sim_duration_minutes))) * 100

    return {
        "department": department_code,
        "staff_count": staff_count,
        "total_tickets_processed": total_tickets,
        "avg_wait_minutes": round(avg_wait, 1),
        "max_wait_minutes": round(max_wait, 1),
        "sla_breach_rate_pct": round(min(100.0, sla_breach_rate), 1),
        "staff_utilization_pct": round(min(100.0, utilization), 1),
        "peak_queue_length": max(queue_lengths) if queue_lengths else 0
    }

def simulate_scenario(scenario_key: str, custom_params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Runs baseline and scenario simulation to show operational impact and bottlenecks."""
    # Department base configurations: (staff, arrival_interval_mean, service_time_mean)
    dept_defaults = {
        "IT": {"staff": 8, "arrival_interval": 4.5, "service_time": 30.0},
        "HR": {"staff": 5, "arrival_interval": 9.0, "service_time": 40.0},
        "ADMIN": {"staff": 4, "arrival_interval": 8.5, "service_time": 30.0}
    }

    if scenario_key == "it_surge_40":
        dept = "IT"
        base_cfg = dept_defaults["IT"]
        scen_cfg = {
            "staff": base_cfg["staff"],
            "arrival_interval": base_cfg["arrival_interval"] / 1.40, # 40% surge in arrival rate
            "service_time": base_cfg["service_time"]
        }
        name = "40% Increase in IT Tickets (OS Upgrade / Patch Tuesday)"
        description = "Simulates enterprise-wide macOS/Windows security patch release resulting in 40% influx of software and driver compatibility tickets."
        bottleneck = "IT Helpdesk L1 Support Staff saturation. Queue builds up after hour 3."
        recs = [
            "Enable automated self-service software portal for standard patch rollbacks.",
            "Temporarily cross-train 2 Admin personnel for basic peripheral triage.",
            "Deploy proactive patch notification banner in Virtual Office."
        ]

    elif scenario_key == "hr_shortage_50":
        dept = "HR"
        base_cfg = dept_defaults["HR"]
        scen_cfg = {
            "staff": max(1, base_cfg["staff"] // 2), # 50% staff down
            "arrival_interval": base_cfg["arrival_interval"],
            "service_time": base_cfg["service_time"]
        }
        name = "50% HR Staff Shortage (Team Offsite / Sick Leave Wave)"
        description = "Simulates seasonal absence or departmental team offsite cutting active HR support agents from 5 down to 2."
        bottleneck = "HR Benefits and Leave verification queues experience severe SLA degradation."
        recs = [
            "Enable AI Assistant auto-approval for routine casual leave requests.",
            "Route complex payroll inquiries to async ticketing queue with SLA disclaimer.",
            "Set expectant response window to 48 hours on the Virtual Office Reception."
        ]

    elif scenario_key == "network_outage":
        dept = "IT"
        base_cfg = dept_defaults["IT"]
        scen_cfg = {
            "staff": base_cfg["staff"],
            "arrival_interval": base_cfg["arrival_interval"] / 3.0, # 300% arrival spike
            "service_time": base_cfg["service_time"] * 1.3
        }
        name = "Company-wide Core Network & VPN Gateway Outage"
        description = "Core router failure disconnects remote employees and internal development microservices."
        bottleneck = "Total IT phone/ticket queue collapse; wait time exceeds 180 minutes."
        recs = [
            "Broadcast critical incident announcement across Virtual Office Noticeboard.",
            "Auto-acknowledge all network/VPN tickets with link to live Status Page.",
            "Engage secondary BGP peering route automatically."
        ]

    elif scenario_key == "policy_rollout_surge":
        dept = "HR"
        base_cfg = dept_defaults["HR"]
        scen_cfg = {
            "staff": base_cfg["staff"],
            "arrival_interval": base_cfg["arrival_interval"] / 1.8,
            "service_time": base_cfg["service_time"] * 1.1
        }
        name = "New Parental & Leave Policy Rollout Surge"
        description = "Launch of new flexible working policy drives a large influx of clarification inquiries."
        bottleneck = "HR email inbox and ticket triage backlog."
        recs = [
            "Pin interactive FAQ widget in HR lounge.",
            "Host live AMA town hall in Synergy Boardroom."
        ]

    else:
        # Custom scenario
        dept = custom_params.get("dept", "IT") if custom_params else "IT"
        base_cfg = dept_defaults.get(dept, dept_defaults["IT"])
        surge_mult = custom_params.get("surge_mult", 1.25) if custom_params else 1.25
        staff_delta = custom_params.get("staff_delta", 0) if custom_params else 0
        scen_cfg = {
            "staff": max(1, base_cfg["staff"] + staff_delta),
            "arrival_interval": base_cfg["arrival_interval"] / surge_mult,
            "service_time": base_cfg["service_time"]
        }
        name = f"Custom Simulation Scenario ({dept})"
        description = f"Custom configuration: Arrival rate x{surge_mult:.2f}, Staff count {scen_cfg['staff']}."
        bottleneck = "Department specific capacity constraints."
        recs = ["Adjust resource pooling dynamically based on queue wait metrics."]

    # Run simulations
    baseline_res = run_discrete_event_simulation(
        department_code=dept,
        staff_count=base_cfg["staff"],
        arrival_interval_mean=base_cfg["arrival_interval"],
        service_time_mean=base_cfg["service_time"]
    )

    scenario_res = run_discrete_event_simulation(
        department_code=dept,
        staff_count=scen_cfg["staff"],
        arrival_interval_mean=scen_cfg["arrival_interval"],
        service_time_mean=scen_cfg["service_time"]
    )

    wait_delta = scenario_res["avg_wait_minutes"] - baseline_res["avg_wait_minutes"]
    wait_pct = ((scenario_res["avg_wait_minutes"] - baseline_res["avg_wait_minutes"]) / max(0.1, baseline_res["avg_wait_minutes"])) * 100

    return {
        "scenario_key": scenario_key,
        "name": name,
        "description": description,
        "department": dept,
        "baseline": baseline_res,
        "simulated": scenario_res,
        "impact": {
            "wait_time_delta_min": round(wait_delta, 1),
            "wait_time_increase_pct": round(wait_pct, 1),
            "sla_breach_increase_pct": round(scenario_res["sla_breach_rate_pct"] - baseline_res["sla_breach_rate_pct"], 1),
            "utilization_delta_pct": round(scenario_res["staff_utilization_pct"] - baseline_res["staff_utilization_pct"], 1),
            "bottleneck_diagnosis": bottleneck
        },
        "recommendations": recs
    }

if __name__ == "__main__":
    res = simulate_scenario("it_surge_40")
    print(f"Scenario: {res['name']}")
    print(f"Baseline Avg Wait: {res['baseline']['avg_wait_minutes']}m -> Simulated: {res['simulated']['avg_wait_minutes']}m (+{res['impact']['wait_time_increase_pct']}%)")
    print(f"Bottleneck: {res['impact']['bottleneck_diagnosis']}")
