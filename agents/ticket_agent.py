"""
Ticket Triage & Routing Agent for OfficeMate 2.0
CSE472 Deep Learning for NLP - Automatic Ticket Creation Requirement
Rule-based priority assignment, departmental routing, and status tracking.
"""

import re
from typing import Dict, Any, Tuple
from db.database import create_ticket, get_tickets, update_ticket_status

CRITICAL_KEYWORDS = [
    "outage", "server down", "production down", "data breach", "security incident",
    "ransomware", "emergency", "fire", "payroll failure", "critical failure", "fatal error"
]

HIGH_KEYWORDS = [
    "cannot work", "blocked", "urgent", "broken laptop", "vpn failure", "auth error",
    "locked out", "500 internal", "deadline", "immediate", "overheating", "battery swollen"
]

LOW_KEYWORDS = [
    "minor", "stationery", "pen", "notebook", "desk adjustment", "suggestion",
    "question later", "no rush", "whenever possible", "mouse pad"
]

def determine_priority(text: str, intent: str = "") -> str:
    """Assigns priority based on keyword severity rules and intent."""
    text_lower = text.lower()
    
    for kw in CRITICAL_KEYWORDS:
        if kw in text_lower:
            return "CRITICAL"

    for kw in HIGH_KEYWORDS:
        if kw in text_lower:
            return "HIGH"

    for kw in LOW_KEYWORDS:
        if kw in text_lower:
            return "LOW"

    # Intent based defaults
    if intent in ["vpn_network", "hardware_issue"]:
        return "HIGH"
    elif intent in ["payroll_salary"]:
        return "MEDIUM"
        
    return "MEDIUM"

def auto_create_ticket_from_query(
    query: str,
    department_code: str,
    intent: str = "general_inquiry",
    user_id: int = 1,
    reason: str = "Auto-generated: No conclusive knowledge-base answer available."
) -> Dict[str, Any]:
    """Generates unique ticket code, assigns priority, routes to department, and saves in DB."""
    priority = determine_priority(query, intent)
    
    # Generate concise title
    words = query.strip().split()
    short_title = " ".join(words[:8]) + ("..." if len(words) > 8 else "")
    description = f"{query}\n\n[Routing Reason: {reason} | Classified Intent: {intent}]"

    ticket = create_ticket(
        title=short_title,
        description=description,
        department_code=department_code,
        priority=priority,
        created_by=user_id,
        sentiment="neutral"
    )
    return ticket

if __name__ == "__main__":
    t = auto_create_ticket_from_query(
        "Production server is down and VPN connection timed out!",
        department_code="IT",
        intent="vpn_network"
    )
    print(f"Created Ticket: {t['ticket_code']} | Priority: {t['priority']} | Status: {t['status']}")
