"""
Page 2: AI Workplace Assistant
Multi-Agent Conversational AI with Deep Learning Intent Classification,
RAG Knowledge Retrieval, and Automated Ticket Creation.
"""

import streamlit as st
import json
from frontend.components.illustrations import render_banner_picture
from agents.supervisor import handle_chat_message
from simulation.explainable_ai import explain_prediction
from db.database import query_all, log_chat_feedback
from frontend.components.user_context import get_active_user, render_user_profile_sidebar

st.set_page_config(page_title="AI Workplace Assistant | OfficeMate 2.0", page_icon="🤖", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render Dynamic Sidebar Profile
render_user_profile_sidebar()
active_user = get_active_user()

# Session state initialization for chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hello! I am your **OfficeMate 2.0 Universal Workplace AI Assistant**.\n\n"
                "I can assist you with:\n"
                "• 📋 **Company Policies:** Leave quotas, healthcare benefits, travel per diem, VPN guides\n"
                "• 💻 **Tech & Coding:** Python, algorithms, architecture, debugging, and shell commands\n"
                "• ✉️ **Business Writing:** Draft professional emails, project status reports, meeting agendas\n"
                "• 🎫 **Incident Triage:** Diagnose technical issues and automatically route support tickets\n"
                "• 🏢 **Virtual HQ Navigation:** Book meeting rooms, check cafeteria menus, inspect the Digital Twin\n\n"
                "How can I help you today?"
            ),
            "department": "SYSTEM",
            "sources": []
        }
    ]

# Top header
st.markdown("""
<div class="om-header">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">🤖 AI Workplace Assistant</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">
      Dual-engine AI: Bidirectional LSTM Deep Learning + RAG Policy Retrieval + Automatic Ticket Routing
    </p>
  </div>
  <div>
    <span class="om-badge badge-it">Multi-Agent Supervisor</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual AI Robot Hero Banner
render_banner_picture("ai_assistant_robot.png", caption="🤖 OfficeMate 2.0 Universal Workplace AI Companion • Powered by Deep Learning NLP")
st.write("")

# Configuration Sidebar Controls
with st.sidebar:
    st.header("⚙️ Assistant Controls")
    model_choice = st.selectbox(
        "🧠 NLP Engine",
        ["Bidirectional LSTM (Deep Learning)", "TF-IDF + Scikit-Learn Baseline"],
        index=0
    )
    use_dl = "Bidirectional" in model_choice
    lang_choice = st.selectbox("🌐 Response Language", ["English (en)", "Hindi (hi)", "Telugu (te)", "Kannada (kn)"])
    lang_code = lang_choice.split("(")[-1].replace(")", "").strip()

    st.markdown("---")
    st.subheader("💡 Sample Inquiries")
    sample_queries = [
        "How many vacation days do I get per year?",
        "Can you explain Python decorators with an example?",
        "Draft an email to my manager for 2 days sick leave",
        "GlobalProtect VPN timeout on macOS laptop",
        "How do I submit travel meal expense per diem?",
        "Can I bring my pet chinchilla into the office workspace?" # Intentional novel/unresolved query
    ]
    for sq in sample_queries:
        if st.button(f"👉 {sq[:34]}...", key=f"sample_{sq[:10]}", width="stretch"):
            st.session_state["pending_input"] = sq

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", width="stretch"):
        st.session_state.messages = []
        st.rerun()

# Department Badge Mapping
dept_labels = {
    "HR": "🌸 **HR Department Agent**",
    "IT": "💻 **IT Department Agent**",
    "ADMIN": "🏢 **Admin Department Agent**",
    "SYSTEM": "🏢 **OfficeMate Universal AI**"
}

# Display Chat Messages using native Streamlit chat components
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**👤 You ({active_user['full_name']})**")
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            dept_key = msg.get("department", "SYSTEM")
            st.markdown(dept_labels.get(dept_key, f"**{dept_key} Agent**"))
            st.markdown(msg["content"])

            # Ticket Generation Alert Card
            if msg.get("ticket"):
                t = msg["ticket"]
                st.warning(
                    f"🎫 **Support Ticket Generated: `{t.get('ticket_code')}`**\n\n"
                    f"• **Requester:** {active_user['full_name']} &nbsp;|&nbsp; **Routed Department:** {t.get('department_code')}\n"
                    f"• **Priority:** `{t.get('priority')}` &nbsp;|&nbsp; **Status:** `{t.get('status', 'OPEN')}`\n"
                    f"• **Reason:** {t.get('title')}"
                )

            # Verified Source Citations
            if msg.get("sources"):
                st.caption(f"📌 **Verified Policy Citations:** {' • '.join(msg['sources'])}")

            # Feedback buttons
            if i > 0:
                cfb1, cfb2, _ = st.columns([1, 1, 10])
                if cfb1.button("👍", key=f"thumb_up_{i}", help="Helpful response"):
                    log_chat_feedback(active_user["id"], msg['content'][:100], 'positive')
                    st.toast("Thank you for the positive feedback!")
                if cfb2.button("👎", key=f"thumb_down_{i}", help="Needs improvement"):
                    log_chat_feedback(active_user["id"], msg['content'][:100], 'negative')
                    st.toast("Feedback logged for AI retraining.")

# User Input Form
user_query = st.chat_input("Ask me anything! Company policies, coding & tech, email drafts, support issues, or math...")
if not user_query and "pending_input" in st.session_state:
    user_query = st.session_state.pop("pending_input")

if user_query:
    # 1. Append and render user message immediately
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"**👤 You ({active_user['full_name']})**")
        st.markdown(user_query)

    # 2. Process query with supervisor agent and render assistant message immediately
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing inquiry with Deep Learning NLP & searching knowledge base..."):
            res = handle_chat_message(
                user_query,
                user_id=active_user["id"],
                language=lang_code,
                use_deep_learning=use_dl
            )
        dept_key = res.get("department", "SYSTEM")
        st.markdown(dept_labels.get(dept_key, f"**{dept_key} Agent**"))
        st.markdown(res["response"])

        if res.get("ticket"):
            t = res["ticket"]
            st.warning(
                f"🎫 **Support Ticket Generated: `{t.get('ticket_code')}`**\n\n"
                f"• **Requester:** {active_user['full_name']} &nbsp;|&nbsp; **Routed Department:** {t.get('department_code')}\n"
                f"• **Priority:** `{t.get('priority')}` &nbsp;|&nbsp; **Status:** `{t.get('status', 'OPEN')}`\n"
                f"• **Reason:** {t.get('title')}"
            )

        if res.get("sources"):
            st.caption(f"📌 **Verified Policy Citations:** {' • '.join(res['sources'])}")

    # 3. Save assistant message to session state and refresh
    st.session_state.messages.append({
        "role": "assistant",
        "content": res["response"],
        "department": res.get("department"),
        "intent": res.get("intent"),
        "sources": res.get("sources", []),
        "ticket": res.get("ticket")
    })
    st.rerun()
