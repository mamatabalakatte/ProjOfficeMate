"""
Unit Tests for Enterprise Digital Twin & SimPy Simulator
"""

import pytest
from simulation.digital_twin import get_department_telemetry
from simulation.what_if_simulator import simulate_scenario, run_discrete_event_simulation
from simulation.predictive_engine import forecast_ticket_surges

def test_telemetry_calculation():
    telem = get_department_telemetry()
    assert "overall_health_score" in telem
    assert 0 <= telem["overall_health_score"] <= 100
    assert "IT" in telem["departments"]
    assert "HR" in telem["departments"]
    assert "ADMIN" in telem["departments"]

def test_what_if_simulation_execution():
    res = simulate_scenario("it_surge_40")
    assert res["scenario_key"] == "it_surge_40"
    assert "baseline" in res
    assert "simulated" in res
    assert res["simulated"]["total_tickets_processed"] > 0
    assert "bottleneck_diagnosis" in res["impact"]

def test_predictive_ticket_forecast():
    fc = forecast_ticket_surges(days_ahead=7)
    assert len(fc["dates"]) == 7
    assert len(fc["forecasts"]["IT"]) == 7
    assert len(fc["forecasts"]["HR"]) == 7
