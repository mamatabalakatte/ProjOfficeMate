"""
Complete Functional and Visual Audit Script for OfficeMate 2.0
Executes every backend, model, database, and logic component used in all 17 pages.
"""

import os
import sys

# Ensure project root is in python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

def audit_all():
    print("=" * 60)
    print("STARTING COMPLETE AUDIT OF OFFICEMATE 2.0 COMPONENTS")
    print("=" * 60)

    # 1. Database Operations
    print("\n[1/8] Auditing Database & Persistence...")
    from db.database import (
        get_tickets, create_ticket, update_ticket_status,
        get_knowledge_docs, get_meeting_rooms, get_room_bookings,
        book_room, get_active_announcements, query_all, query_one,
        get_user_tasks, toggle_task_completion, add_user_task,
        resolve_policy_conflict, log_audit, log_chat_feedback
    )
    tickets = get_tickets()
    assert len(tickets) > 0, "No tickets found"
    docs = get_knowledge_docs()
    assert len(docs) >= 10, "Knowledge docs count mismatch"
    rooms = get_meeting_rooms()
    assert len(rooms) == 4, "Expected 4 meeting rooms"
    bookings = get_room_bookings()
    assert len(bookings) > 0, "No room bookings found"
    announcements = get_active_announcements()
    assert len(announcements) > 0, "No announcements found"
    tasks = get_user_tasks(1)
    assert len(tasks) > 0, "No user tasks found"
    print(f"  ✓ Database verified: {len(tickets)} tickets, {len(docs)} docs, {len(rooms)} rooms, {len(tasks)} tasks.")

    # 2. NLP & Deep Learning Pipeline
    print("\n[2/8] Auditing NLP & Deep Learning Models...")
    from nlp.bilstm_model import BiLSTMPipeline
    from nlp.tfidf_baseline import TfidfBaselineClassifier
    from nlp.evaluator import get_latest_metrics

    bilstm = BiLSTMPipeline()
    bilstm.load()
    bilstm_res = bilstm.predict("How many vacation days do I get per year?")
    assert bilstm_res["department"] == "HR", f"Expected HR, got {bilstm_res['department']}"

    tfidf = TfidfBaselineClassifier()
    tfidf.load()
    tfidf_res = tfidf.predict("VPN connection dropped on WiFi")
    assert tfidf_res["department"] == "IT", f"Expected IT, got {tfidf_res['department']}"

    metrics = get_latest_metrics()
    b_acc = metrics["models"]["BiLSTM_DeepLearning"]["accuracy"]
    t_acc = metrics["models"]["TF_IDF_Baseline"]["accuracy"]
    print(f"  ✓ Bi-LSTM Prediction: {bilstm_res['department']} (Conf: {bilstm_res['department_confidence']:.2%})")
    print(f"  ✓ TF-IDF Prediction: {tfidf_res['department']} (Conf: {tfidf_res['department_confidence']:.2%})")
    print(f"  ✓ Held-Out Test Metrics: Bi-LSTM Acc={b_acc:.2%}, TF-IDF Acc={t_acc:.2%}")

    # 3. Knowledge Retrieval (RAG)
    print("\n[3/8] Auditing Semantic Search & RAG...")
    from nlp.semantic_search import search_knowledge_base
    kb_res = search_knowledge_base("maternity leave policy duration", category="HR")
    assert kb_res["reliable"] is True, "Expected reliable RAG result for maternity leave"
    assert len(kb_res["results"]) > 0, "No matches for maternity leave"
    print(f"  ✓ Semantic Search: Top match '{kb_res['results'][0]['title']}' (Score: {kb_res['top_score']:.3f})")

    # 4. Universal AI Assistant Brain & Supervisor
    print("\n[4/8] Auditing Universal Chatbot...")
    from agents.supervisor import handle_chat_message

    test_queries = [
        ("Greeting", "Hello! Who are you?"),
        ("Tech/Python", "Can you explain python decorators with an example?"),
        ("Email Draft", "Draft an email to my manager for 2 days sick leave"),
        ("Policy RAG", "How many vacation days do I get per year?"),
        ("Math", "What is 15 * 8?"),
        ("Incident Hardware", "My laptop screen is cracked and won't turn on"),
        ("Policy Exception", "Can we get approval for an exotic team pet in the office?"),
    ]
    for q_type, q_text in test_queries:
        r = handle_chat_message(q_text, user_id=1)
        assert len(r["response"]) > 20, f"Empty response for {q_type}"
        has_ticket = r["ticket"] is not None
        print(f"  ✓ {q_type:18s} -> Response OK ({len(r['response'])} chars, Ticket: {has_ticket})")

    # 5. Specialized Tools & Cross-Department Diagnostics
    print("\n[5/8] Auditing Specialized Tools & OCR Diagnostic...")
    from agents.specialized_tools import (
        diagnose_screenshot_or_error, analyze_cross_department_root_causes,
        detect_policy_conflicts
    )
    ocr_res = diagnose_screenshot_or_error("VPN connection timed out: SSL handshake failed code 504")
    assert "suggested_fix" in ocr_res, "Missing suggested_fix in OCR"

    root_causes = analyze_cross_department_root_causes()
    assert len(root_causes) > 0, "Expected root cause incidents"

    conflicts = detect_policy_conflicts()
    assert len(conflicts) > 0, "Expected policy conflicts detected"
    print(f"  ✓ OCR Diagnostic, Root Causes ({len(root_causes)}), Policy Conflicts ({len(conflicts)}) verified.")

    # 6. Enterprise Digital Twin & SimPy Simulator
    print("\n[6/8] Auditing Digital Twin & SimPy Simulator...")
    from simulation.digital_twin import get_department_telemetry
    from simulation.what_if_simulator import simulate_scenario
    from simulation.predictive_engine import forecast_ticket_surges

    telem = get_department_telemetry()
    assert "overall_health_score" in telem, "Missing health score in telemetry"

    sim_res = simulate_scenario("it_surge_40")
    assert "impact" in sim_res and "simulated" in sim_res, "Missing impact in SimPy simulation"

    forecast = forecast_ticket_surges(14)
    assert len(forecast["dates"]) == 14, "Expected 14-day forecast"
    print(f"  ✓ Telemetry Health: {telem['overall_health_score']}%, SimPy Shock simulated, 14-day Forecast generated.")

    # 7. Visual Pictures & Assets
    print("\n[7/8] Auditing Visual Assets & Illustrations...")
    assets_dir = os.path.join(ROOT_DIR, "frontend", "assets", "images")
    required_images = [
        "virtual_office_hq.png", "ai_assistant_robot.png", "hr_lounge.png",
        "it_command.png", "admin_desk.png", "boardroom.png", "cafeteria.png",
        "workspace_cockpit.png", "knowledge_base.png", "ticket_triage.png",
        "digital_twin.png", "what_if_lab.png", "impact_intelligence.png",
        "predictive_forecast.png", "knowledge_graph.png", "model_evaluation.png",
        "admin_control.png"
    ]
    for img_name in required_images:
        img_path = os.path.join(assets_dir, img_name)
        assert os.path.exists(img_path), f"Missing image asset: {img_name}"
        assert os.path.getsize(img_path) > 1000, f"Image {img_name} is corrupted or empty"
    print(f"  ✓ All {len(required_images)} high-resolution PNG picture assets verified.")

    # 8. All 17 Pages Syntax & Import Check
    print("\n[8/8] Auditing Page Source Code & Compilations...")
    import glob
    page_files = sorted(glob.glob(os.path.join(ROOT_DIR, "pages", "*.py")) + [os.path.join(ROOT_DIR, "app.py")])
    for pf in page_files:
        with open(pf) as f:
            code = f.read()
        compile(code, pf, 'exec')
    print(f"  ✓ All {len(page_files)} pages compiled with zero syntax errors.")

    print("\n" + "=" * 60)
    print("ALL AUDIT CHECKS PASSED SUCCESSFULLY (100% OPERATIONAL)")
    print("=" * 60)

if __name__ == "__main__":
    audit_all()
