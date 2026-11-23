"""
OfficeMate 2.0 – The Intelligent Virtual Workplace
Main Application Entry Point (Streamlit Multi-Page Headquarters)
Combines Interactive Cartoon Virtual Office, NLP Intent Classification,
Multi-Agent Workplace Assistant, and Enterprise Digital Twin.
"""

import streamlit as st
import os
from frontend.components.virtual_office_svg import render_virtual_office_map
from frontend.components.illustrations import render_banner_picture
from frontend.components.avatars import get_avatar_svg, render_employee_badge
from db.database import get_active_announcements, query_all, get_tickets
from simulation.digital_twin import get_department_telemetry

st.set_page_config(
    page_title="OfficeMate 2.0 | Intelligent Virtual Workplace",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS Theme
css_path = os.path.join(os.path.dirname(__file__), "frontend", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from frontend.components.user_context import render_user_profile_sidebar

# Sidebar Identity & Navigation Guide
render_user_profile_sidebar()

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🧭 Core Hubs")
    st.markdown("""
    - **🏢 Virtual Office**: Illustrated interactive HQ
    - **🤖 AI Assistant**: Bi-LSTM + RAG Chat
    - **🌸 HR Office**: Leave & Benefits
    - **💻 IT Command**: VPN & Diagnostics
    - **🏢 Admin Desk**: Travel & Facilities
    - **💼 My Workspace**: Personal Cockpit
    - **📚 Knowledge Base**: Policies & Docs
    - **🎫 Tickets**: Kanban Board
    - **📅 Meeting Rooms**: Booking Calendar
    - **🌐 Digital Twin**: Real-Time Telemetry
    - **🔮 What-If Simulator**: SimPy Queues
    - **💡 Impact Intel**: Friction Diagnostics
    - **📈 Predictive**: 14-Day Surge Forecaster
    - **🕸️ Knowledge Graph**: Entity Network
    - **🧪 Model Evaluation**: CSE472 Deep Learning
    - **⚙️ Admin Centre**: HITL Triage
    """)

    st.markdown("---")
    st.caption("CSE472 Deep Learning for NLP • Project No. 20")

# Main Header
st.markdown("""
<div class="om-header">
  <div>
    <h1 style="margin:0; font-size: 2.2rem; font-weight: 800;">🏢 OfficeMate 2.0</h1>
    <p style="margin: 0.35rem 0 0 0; opacity: 0.95; font-size: 1.1rem;">
      Step into your virtual office! Visit departments, ask your AI assistant, book rooms, and simulate organizational workflows.
    </p>
  </div>
  <div style="text-align: right;">
    <span class="om-badge badge-success" style="font-size: 0.85rem; padding: 6px 14px;">🟢 Enterprise Twin Online</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Live Operational Telemetry
telem = get_department_telemetry()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{telem['overall_health_score']}%</div>
      <div class="stat-label">Overall Workplace Health</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{telem['total_active_backlog']}</div>
      <div class="stat-label">Active Open Tickets</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{telem['total_critical_items']}</div>
      <div class="stat-label">Critical Incidents</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{telem['room_utilization_pct']}%</div>
      <div class="stat-label">Meeting Room Utilization</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Interactive Virtual Office Map
st.subheader("🗺️ Illustrated Virtual Office Headquarters")
st.caption("Click any department or room button below to navigate directly into that office space.")
render_banner_picture("virtual_office_hq.png", caption="🏢 OfficeMate 2.0 Virtual Workplace Headquarters • Visual 3D Floorplan")

st.write("")
st.markdown("### 🚪 Quick Department Teleport")
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

with c1:
    if st.button("🌸 HR Office", key="home_btn_hr", use_container_width=True):
        st.switch_page("pages/03_HR_Department.py")
with c2:
    if st.button("💻 IT Command", key="home_btn_it", use_container_width=True):
        st.switch_page("pages/04_IT_Department.py")
with c3:
    if st.button("🏢 Admin Desk", key="home_btn_admin", use_container_width=True):
        st.switch_page("pages/05_Admin_Department.py")
with c4:
    if st.button("📅 Boardroom", key="home_btn_rooms", use_container_width=True):
        st.switch_page("pages/09_Meeting_Room_Booking.py")
with c5:
    if st.button("☕ Cafeteria", key="home_btn_cafe", use_container_width=True):
        st.switch_page("pages/17_Cafeteria_and_Lounge.py")
with c6:
    if st.button("🤖 AI Assistant", key="home_btn_ai", use_container_width=True):
        st.switch_page("pages/02_AI_Workplace_Assistant.py")
with c7:
    if st.button("💼 Workspace", key="home_btn_work", use_container_width=True):
        st.switch_page("pages/06_Employee_Workspace.py")

st.markdown("---")

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📢 Official Noticeboard & Announcements")
    announcements = get_active_announcements()
    for ann in announcements:
        cat_badge = {
            "Company": "badge-hr",
            "IT": "badge-it",
            "Cafeteria": "badge-admin"
        }.get(ann["category"], "badge-open")
        st.markdown(f"""
        <div class="om-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span class="om-badge {cat_badge}">{ann['category']}</span>
            <span style="font-size: 0.8rem; color: #64748B;">{ann['created_at']}</span>
          </div>
          <h4 style="margin: 0 0 6px 0; color: #1E293B;">{ann['title']}</h4>
          <p style="margin: 0; color: #475569; font-size: 0.95rem;">{ann['body']}</p>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.subheader("👥 Online Colleague Roster")
    users = query_all("SELECT * FROM users ORDER BY department_id, id")
    for u in users:
        role_label = f"{u['role'].replace('_', ' ').title()} • Dept {u['department_id']}"
        st.markdown(render_employee_badge(u["full_name"], role_label, u["status"]), unsafe_allow_html=True)
        st.write("")
