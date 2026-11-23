"""
Page 1: Virtual Office Home
Immersive Cartoon-Style Virtual Workplace Headquarters
"""

import streamlit as st
from frontend.components.virtual_office_svg import render_virtual_office_map
from frontend.components.illustrations import render_banner_picture
from frontend.components.avatars import get_avatar_svg, render_employee_badge
from db.database import get_active_announcements, query_all, get_tickets
from simulation.digital_twin import get_department_telemetry
from frontend.components.user_context import render_user_profile_sidebar

st.set_page_config(page_title="OfficeMate 2.0 | Virtual Office", page_icon="🏢", layout="wide")

# Inject Custom CSS
with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render Dynamic Sidebar Profile
render_user_profile_sidebar()

# Top Banner
st.markdown("""
<div class="om-header">
  <div>
    <h1 style="margin:0; font-size: 2rem; font-weight: 800;">🏢 OfficeMate 2.0 – Virtual Workplace</h1>
    <p style="margin: 0.35rem 0 0 0; opacity: 0.9; font-size: 1.05rem;">
      Welcome to your interactive virtual headquarters! Explore departments, connect with colleagues, and interact with enterprise AI.
    </p>
  </div>
  <div style="text-align: right;">
    <span class="om-badge badge-success" style="font-size: 0.85rem; padding: 6px 14px;">🟢 HQ Live & Connected</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Live Metric Strip
telem = get_department_telemetry()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{telem['overall_health_score']}%</div>
      <div class="stat-label">Overall Office Health</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{telem['total_active_backlog']}</div>
      <div class="stat-label">Active Open Requests</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{telem['total_critical_items']}</div>
      <div class="stat-label">Critical Priority Items</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{telem['room_utilization_pct']}%</div>
      <div class="stat-label">Meeting Room Usage</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Main Office Visual Layout
st.subheader("🗺️ Interactive Virtual Office Map")
render_banner_picture("virtual_office_hq.png", caption="🏢 OfficeMate 2.0 Virtual Workplace Headquarters • Visual 3D Floorplan")

st.write("")
st.markdown("### 🚪 Quick Department Teleport")
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

with c1:
    if st.button("🌸 HR Office", use_container_width=True):
        st.switch_page("pages/03_HR_Department.py")
with c2:
    if st.button("💻 IT Command", use_container_width=True):
        st.switch_page("pages/04_IT_Department.py")
with c3:
    if st.button("🏢 Admin Desk", use_container_width=True):
        st.switch_page("pages/05_Admin_Department.py")
with c4:
    if st.button("📅 Boardroom", use_container_width=True):
        st.switch_page("pages/09_Meeting_Room_Booking.py")
with c5:
    if st.button("☕ Cafeteria", use_container_width=True):
        st.switch_page("pages/17_Cafeteria_and_Lounge.py")
with c6:
    if st.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/02_AI_Workplace_Assistant.py")
with c7:
    if st.button("💼 Workspace", use_container_width=True):
        st.switch_page("pages/06_Employee_Workspace.py")

st.markdown("---")

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📢 Office Noticeboard & Announcements")
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
