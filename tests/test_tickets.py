"""
Unit Tests for Automatic Ticket Lifecycle & Routing Logic
"""

import pytest
from agents.ticket_agent import determine_priority, auto_create_ticket_from_query
from db.database import get_tickets, update_ticket_status

def test_priority_determination():
    assert determine_priority("Urgent: production server down and outage!") == "CRITICAL"
    assert determine_priority("My laptop battery is broken and cannot work") == "HIGH"
    assert determine_priority("Need a ballpoint pen and notebook for desk") == "LOW"
    assert determine_priority("Inquiry regarding annual leaves") == "MEDIUM"

def test_auto_create_ticket():
    ticket = auto_create_ticket_from_query(
        query="VPN tunnel failed to connect after password reset",
        department_code="IT",
        intent="vpn_network",
        user_id=1
    )
    assert ticket is not None
    assert ticket["ticket_code"].startswith("TKT-IT-")
    assert ticket["status"] == "OPEN"
    assert ticket["priority"] in ["HIGH", "CRITICAL"]

def test_ticket_status_transition():
    tickets = get_tickets(department="IT")
    assert len(tickets) > 0
    t = tickets[0]
    ok = update_ticket_status(t["id"], "RESOLVED", actor_id=2, notes="Resolved by test runner")
    assert ok is True
    updated = [item for item in get_tickets() if item["id"] == t["id"]][0]
    assert updated["status"] == "RESOLVED"
