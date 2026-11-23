"""
Page 6: Employee Personal Workspace
Personal cockpit: My tickets, upcoming room bookings, persistent daily tasks, and announcements.
"""

import streamlit as st
from db.database import get_tickets, get_room_bookings, query_all, query_one, get_user_tasks, toggle_task_completion, add_user_task
from frontend.components.avatars import get_avatar_svg
from frontend.components.illustrations import render_banner_picture

st.set_page_config(page_title="My Workspace | OfficeMate 2.0", page_icon="💼", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from frontend.components.user_context import get_active_user, render_user_profile_sidebar

# Render Dynamic Sidebar Profile
render_user_profile_sidebar()
user = get_active_user()

avatar_html = get_avatar_svg(user['full_name'], user.get('role', 'Staff'), size=64)
header_html = (
    f'<div class="om-header">'
    f'<div style="display:flex; align-items:center; gap: 16px;">'
    f'{avatar_html}'
    f'<div>'
    f'<h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">💼 {user["full_name"]}\'s Personal Cockpit</h1>'
    f'<p style="margin: 0.25rem 0 0 0; opacity: 0.9;">{user.get("email")} • Role: {user.get("role", "employee").replace("_", " ").title()} ({user.get("dept_code", "General")})</p>'
    f'</div>'
    f'</div>'
    f'<div><span class="om-badge badge-success">🟢 Profile Active</span></div>'
    f'</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

# Visual Futuristic Workspace Hero Banner
render_banner_picture("workspace_cockpit.png", caption=f"💼 Personal Cockpit • {user['full_name']} Tasks & Tickets")
st.write("")

# Personal quick stats
my_tickets = get_tickets(user_id=user["id"])
open_count = sum(1 for t in my_tickets if t["status"] in ["OPEN", "IN_PROGRESS"])
resolved_count = sum(1 for t in my_tickets if t["status"] in ["RESOLVED", "CLOSED"])
my_bookings = [b for b in get_room_bookings() if b["user_id"] == user["id"]]
assigned_to_me = [t for t in get_tickets() if t.get("assigned_to") == user["id"]]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{open_count}</div>
      <div class="stat-label">Tickets Raised by Me</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{len(assigned_to_me)}</div>
      <div class="stat-label">Tickets Assigned to Me</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">{len(my_bookings)}</div>
      <div class="stat-label">Active Room Bookings</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-value">16</div>
      <div class="stat-label">Remaining PTO Days</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("🎫 My Support Tickets")
    if not my_tickets:
        st.info("You haven't submitted any tickets yet. You can submit one via the AI Assistant or Department pages!")
    else:
        for t in my_tickets:
            p_color = {"CRITICAL": "#EF4444", "HIGH": "#EA580C", "MEDIUM": "#2563EB", "LOW": "#10B981"}.get(t["priority"], "#6B7280")
            stat_badge = "badge-resolved" if t["status"] in ["RESOLVED", "CLOSED"] else "badge-open"
            res_html = ""
            if t.get("resolution_notes"):
                res_html = f"<div style='margin-top: 8px; padding: 8px; background: #ECFDF5; border-radius: 6px; font-size: 0.85rem; color: #065F46;'><strong>Resolution Note:</strong> {t['resolution_notes']}</div>"
                
            st.markdown(f"""
            <div class="om-card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight: 800; color: #4F46E5;">{t['ticket_code']}</span>
                <div>
                  <span class="om-badge" style="background: {p_color}20; color: {p_color};">{t['priority']}</span>
                  <span class="om-badge {stat_badge}">{t['status']}</span>
                </div>
              </div>
              <h4 style="margin: 6px 0;">{t['title']}</h4>
              <p style="color: #475569; font-size: 0.88rem; margin: 0;">{t['description']}</p>
              {res_html}
            </div>
            """, unsafe_allow_html=True)

with col_right:
    st.subheader("📅 My Meeting Room Bookings")
    if not my_bookings:
        st.info("No upcoming meeting room reservations.")
    else:
        for b in my_bookings:
            st.markdown(f"""
            <div class="om-card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color: #8B5CF6;">{b['room_name']} ({b['floor']})</strong>
                <span class="om-badge badge-success">{b['status']}</span>
              </div>
              <h5 style="margin: 6px 0;">{b['title']}</h5>
              <div style="font-size: 0.82rem; color: #64748B;">
                ⏰ <strong>{b['start_time']}</strong> to <strong>{b['end_time']}</strong><br>
                👥 Attendees: {b['attendees_count']}
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.subheader("✅ Daily Workplace Tasks (Persistent)")
    tasks = get_user_tasks(user_id=user["id"])
    completed_num = sum(1 for t in tasks if t["is_completed"])
    total_num = max(1, len(tasks))
    st.progress(completed_num / total_num, text=f"Task Progress: {completed_num}/{len(tasks)} completed")

    for task in tasks:
        is_chk = bool(task["is_completed"])
        new_val = st.checkbox(
            task["title"],
            value=is_chk,
            key=f"task_chk_{task['id']}"
        )
        if new_val != is_chk:
            toggle_task_completion(task["id"], new_val)
            st.rerun()

    # Add task form
    with st.form("new_task_form", clear_on_submit=True):
        new_task_txt = st.text_input("Add a personal workplace task", placeholder="e.g. Prepare deck for Friday Sprint Review")
        if st.form_submit_button("➕ Add Task", use_container_width=True):
            if new_task_txt.strip():
                add_user_task(user["id"], new_task_txt.strip())
                st.success("Task added!")
                st.rerun()
