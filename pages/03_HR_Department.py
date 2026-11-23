"""
Page 3: HR Department Portal
Leave policies, attendance, employee benefits, and HR support tickets.
"""

import streamlit as st
from datetime import date, timedelta
from db.database import get_tickets, create_ticket, get_knowledge_docs, query_all
from frontend.components.avatars import get_avatar_svg
from frontend.components.illustrations import render_banner_picture
from frontend.components.user_context import get_active_user, render_user_profile_sidebar

st.set_page_config(page_title="HR Department | OfficeMate 2.0", page_icon="🌸", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render Dynamic Sidebar Profile
render_user_profile_sidebar()
active_user = get_active_user()

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #BE185D 0%, #EC4899 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">🌸 Human Resources Department</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.95;">
      People operations, leave management, healthcare benefits, and employee relations.
    </p>
  </div>
  <div>
    <span class="om-badge badge-hr" style="background: white; color: #BE185D;">Department Lead: Sarah Jenkins</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual HR Lounge Hero Banner
render_banner_picture("hr_lounge.png", caption="🌸 HR People Lounge • Wellness & Benefits")
st.write("")

# Personal Leave Balances
st.subheader("📊 Your 2026 Leave Balances")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="stat-box">
      <div class="stat-value" style="color: #EC4899;">16</div>
      <div class="stat-label">Vacation Days Left (of 20)</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stat-box">
      <div class="stat-value" style="color: #EC4899;">8</div>
      <div class="stat-label">Casual Leaves Left (of 10)</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stat-box">
      <div class="stat-value" style="color: #EC4899;">11</div>
      <div class="stat-label">Sick Leaves Left (of 12)</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="stat-box">
      <div class="stat-value" style="color: #10B981;">Approved</div>
      <div class="stat-label">Health Insurance Status</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
tab_req, tab_policies, tab_tickets = st.tabs(["📝 Submit HR Request", "📖 HR Policy Handbook", "🎫 Department Tickets"])

with tab_req:
    st.markdown("#### Submit a Formal Leave or HR Request")
    with st.form("hr_request_form"):
        req_type = st.selectbox("Request Category", ["Vacation Leave", "Sick Leave (Medical)", "Casual Leave", "Health Insurance Dependent Addition", "Provident Fund / Tax Inquiry"])
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            start_d = st.date_input("Start Date", value=date.today() + timedelta(days=2))
        with col_d2:
            end_d = st.date_input("End Date", value=date.today() + timedelta(days=4))
            
        reason = st.text_area("Details / Reason", placeholder="Explain the context of your request or inquiry...")
        priority = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH", "CRITICAL"], index=1)
        
        submitted = st.form_submit_button("🚀 Submit Request to HR", use_container_width=True)
        if submitted:
            if not reason.strip():
                st.error("Please provide details for your request.")
            else:
                title = f"{req_type}: {start_d} to {end_d}"
                t = create_ticket(title, reason, "HR", priority, created_by=active_user["id"])
                st.success(f"✅ HR Ticket `{t['ticket_code']}` created on behalf of **{active_user['full_name']}**! Sarah Jenkins has been notified.")

with tab_policies:
    st.markdown("#### Official HR Policy Documentation")
    hr_docs = get_knowledge_docs(category="HR")
    for doc in hr_docs:
        with st.expander(f"📘 {doc['title']} (v{doc['version']})", expanded=True):
            st.write(doc["content"])
            st.caption(f"Tags: {doc['tags']} • Last updated: {doc['updated_at']}")

with tab_tickets:
    st.markdown("#### Active HR Tickets Queue")
    hr_tickets = get_tickets(department="HR")
    if not hr_tickets:
        st.info("No active tickets in HR.")
    else:
        for t in hr_tickets:
            p_color = {"CRITICAL": "#EF4444", "HIGH": "#F59E0B", "MEDIUM": "#3B82F6", "LOW": "#10B981"}.get(t["priority"], "#6B7280")
            st.markdown(f"""
            <div class="om-card">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 800; color: #4338CA;">{t['ticket_code']}</span>
                <div>
                  <span class="om-badge" style="background: {p_color}20; color: {p_color};">{t['priority']}</span>
                  <span class="om-badge badge-open">{t['status']}</span>
                </div>
              </div>
              <h4 style="margin: 8px 0 4px 0;">{t['title']}</h4>
              <p style="color: #475569; font-size: 0.9rem; margin-bottom: 6px;">{t['description']}</p>
              <div style="font-size: 0.8rem; color: #64748B;">Created by: {t['creator_name']} • Assignee: {t.get('assignee_name') or 'Unassigned'}</div>
            </div>
            """, unsafe_allow_html=True)
