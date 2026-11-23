"""
Flask REST API Backend for OfficeMate 2.0
Exposes structured JSON endpoints for NLP, multi-agent assistant, tickets,
knowledge base, meeting rooms, digital twin simulations, and model evaluation.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from flask_cors import CORS
from db.database import (
    get_tickets, create_ticket, update_ticket_status,
    get_meeting_rooms, get_room_bookings, book_room,
    get_knowledge_docs, get_active_announcements, query_all
)
from agents.supervisor import handle_chat_message
from nlp.bilstm_model import BiLSTMPipeline
from nlp.tfidf_baseline import TfidfBaselineClassifier
from nlp.semantic_search import search_knowledge_base
from nlp.evaluator import get_latest_metrics
from simulation.digital_twin import get_department_telemetry
from simulation.what_if_simulator import simulate_scenario
from simulation.predictive_engine import forecast_ticket_surges
from simulation.explainable_ai import explain_prediction
from agents.specialized_tools import analyze_cross_department_root_causes, detect_policy_conflicts, diagnose_screenshot_or_error

app = Flask(__name__)
CORS(app)

# Cached models
_bilstm = None
_tfidf = None

def get_models():
    global _bilstm, _tfidf
    if _bilstm is None:
        _bilstm = BiLSTMPipeline()
        try:
            _bilstm.load()
        except Exception:
            pass
    if _tfidf is None:
        _tfidf = TfidfBaselineClassifier()
        try:
            _tfidf.load()
        except Exception:
            pass
    return _bilstm, _tfidf

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "service": "OfficeMate 2.0 REST API",
        "version": "2.0.0",
        "engine": "Bidirectional LSTM + Scikit-Learn + SimPy Digital Twin"
    })

# --- NLP Classification Endpoints ---

@app.route("/api/nlp/classify", methods=["POST"])
def classify():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    use_bilstm = data.get("use_deep_learning", True)
    if not text:
        return jsonify({"error": "text is required"}), 400

    bilstm, tfidf = get_models()
    if use_bilstm and bilstm.model:
        res = bilstm.predict(text)
    else:
        res = tfidf.predict(text)

    # Add XAI explanation
    explanation = explain_prediction(text, res["department"], res["department_confidence"], res["department_probabilities"])
    res["explanation"] = explanation
    return jsonify(res)

# --- AI Assistant Conversation ---

@app.route("/api/assistant/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    user_id = data.get("user_id", 1)
    conversation_id = data.get("conversation_id", None)
    language = data.get("language", "en")

    if not query:
        return jsonify({"error": "query is required"}), 400

    result = handle_chat_message(query, user_id=user_id, conversation_id=conversation_id, language=language)
    return jsonify(result)

# --- Ticket Management ---

@app.route("/api/tickets", methods=["GET"])
def list_tickets():
    dept = request.args.get("department")
    status = request.args.get("status")
    user_id = request.args.get("user_id", type=int)
    tickets = get_tickets(department=dept, status=status, user_id=user_id)
    return jsonify({"count": len(tickets), "tickets": tickets})

@app.route("/api/tickets", methods=["POST"])
def make_ticket():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    department = data.get("department", "IT")
    priority = data.get("priority", "MEDIUM")
    created_by = data.get("created_by", 1)

    if not title or not description:
        return jsonify({"error": "title and description are required"}), 400

    ticket = create_ticket(title, description, department, priority, created_by)
    return jsonify(ticket), 201

@app.route("/api/tickets/<int:ticket_id>/status", methods=["PUT"])
def update_status(ticket_id):
    data = request.get_json() or {}
    new_status = data.get("status")
    actor_id = data.get("actor_id", 1)
    notes = data.get("notes", "")

    if not new_status:
        return jsonify({"error": "status is required"}), 400

    ok = update_ticket_status(ticket_id, new_status, actor_id, notes)
    if not ok:
        return jsonify({"error": "ticket not found"}), 404
    return jsonify({"success": True, "ticket_id": ticket_id, "new_status": new_status})

# --- Knowledge Base & Semantic Search ---

@app.route("/api/knowledge/search", methods=["POST"])
def search_kb():
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    category = data.get("category", "All")
    top_k = data.get("top_k", 3)

    if not query:
        return jsonify({"error": "query is required"}), 400

    res = search_knowledge_base(query, category=category, top_k=top_k)
    return jsonify(res)

@app.route("/api/knowledge/docs", methods=["GET"])
def list_docs():
    cat = request.args.get("category")
    docs = get_knowledge_docs(cat)
    return jsonify({"count": len(docs), "documents": docs})

# --- Meeting Rooms ---

@app.route("/api/rooms", methods=["GET"])
def list_rooms():
    rooms = get_meeting_rooms()
    return jsonify({"rooms": rooms})

@app.route("/api/rooms/bookings", methods=["GET"])
def list_bookings():
    date_str = request.args.get("date")
    bookings = get_room_bookings(date_str)
    return jsonify({"count": len(bookings), "bookings": bookings})

@app.route("/api/rooms/book", methods=["POST"])
def make_booking():
    data = request.get_json() or {}
    room_id = data.get("room_id")
    user_id = data.get("user_id", 1)
    title = data.get("title", "").strip()
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    attendees = data.get("attendees_count", 2)

    if not all([room_id, title, start_time, end_time]):
        return jsonify({"error": "room_id, title, start_time, and end_time are required"}), 400

    res = book_room(room_id, user_id, title, start_time, end_time, attendees)
    if not res["success"]:
        return jsonify(res), 409
    return jsonify(res), 201

# --- Digital Twin & Simulation ---

@app.route("/api/digital-twin/telemetry", methods=["GET"])
def twin_telemetry():
    return jsonify(get_department_telemetry())

@app.route("/api/digital-twin/simulate", methods=["POST"])
def twin_simulate():
    data = request.get_json() or {}
    scenario_key = data.get("scenario", "it_surge_40")
    custom_params = data.get("custom_params")
    res = simulate_scenario(scenario_key, custom_params)
    return jsonify(res)

@app.route("/api/digital-twin/forecast", methods=["GET"])
def twin_forecast():
    days = request.args.get("days", default=14, type=int)
    return jsonify(forecast_ticket_surges(days))

# --- Model Evaluation & Analytics ---

@app.route("/api/model/metrics", methods=["GET"])
def model_metrics():
    return jsonify(get_latest_metrics())

# --- Specialized Tools ---

@app.route("/api/tools/root-causes", methods=["GET"])
def root_causes():
    return jsonify(analyze_cross_department_root_causes())

@app.route("/api/tools/policy-conflicts", methods=["GET"])
def policy_conflicts():
    return jsonify(detect_policy_conflicts())

@app.route("/api/tools/diagnose-error", methods=["POST"])
def diagnose_error():
    data = request.get_json() or {}
    err_text = data.get("error_text", "")
    return jsonify(diagnose_screenshot_or_error(err_text))

@app.route("/api/announcements", methods=["GET"])
def announcements():
    return jsonify(get_active_announcements())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
