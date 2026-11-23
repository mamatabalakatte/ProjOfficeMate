"""
Integration Tests for Flask REST API Endpoints
"""

import pytest
import json
from api.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "online"

def test_classify_endpoint(client):
    payload = {"text": "How do I request a Docker Desktop license?", "use_deep_learning": True}
    res = client.post("/api/nlp/classify", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["department"] == "IT"
    assert "explanation" in data

def test_chat_assistant_endpoint(client):
    payload = {"query": "What is the policy for sick leave?", "language": "en"}
    res = client.post("/api/assistant/chat", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["department"] == "HR"
    assert "response" in data

def test_tickets_endpoints(client):
    # GET list
    res_list = client.get("/api/tickets")
    assert res_list.status_code == 200
    assert "tickets" in res_list.get_json()

    # POST create
    new_ticket = {
        "title": "API Test Ticket",
        "description": "Integration test description",
        "department": "IT",
        "priority": "LOW"
    }
    res_post = client.post("/api/tickets", json=new_ticket)
    assert res_post.status_code == 201
    created = res_post.get_json()
    assert created["ticket_code"].startswith("TKT-IT-")

def test_digital_twin_endpoints(client):
    res_telem = client.get("/api/digital-twin/telemetry")
    assert res_telem.status_code == 200
    assert "departments" in res_telem.get_json()

    res_sim = client.post("/api/digital-twin/simulate", json={"scenario": "it_surge_40"})
    assert res_sim.status_code == 200
    assert "impact" in res_sim.get_json()
