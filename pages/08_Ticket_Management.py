"""
Page 8: Ticket Management & Kanban Board
Full support ticket lifecycle: filters, interactive 1-click Kanban transitions,
SLA countdown, and resolution notes.
"""

import streamlit as st
from db.database import get_tickets, update_ticket_status, assign_ticket, query_all
from frontend.components.illustrations import render_banner_picture
from frontend.components.user_context import get_active_user, get_support_agents, render_user_profile_sidebar

st.set_page_config(page_title="Ticket Management | OfficeMate 2.0", page_icon="🎫", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render Dynamic Sidebar Profile
render_user_profile_sidebar()
active_user = get_active_user()
agents = get_support_agents()
agent_map = {None: "⚠️ Unassigned (In Queue)"}
for a in agents:
    agent_map[a["id"]] = f"{a['full_name']} ({a['dept_code']} Support)"

st.markdown("""
<div class="om-header">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">🎫 Enterprise Ticket Management &amp; Triage</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">
      Real-time queue triage, priority routing, automated SLA monitoring, and interactive Kanban transitions.
    </p>
  </div>
  <div>
    <span class="om-badge badge-success">Automated Rule-Based Routing</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Active User Perspective Banner
role_display = active_user['role'].replace('_', ' ').title()
st.info(
    f"👤 **Current User:** **{active_user['full_name']}** • **Role:** {role_display} ({active_user.get('dept_code', 'General')}) &nbsp;|&nbsp; "
    f"Use the **Sidebar dropdown** to switch between Employees and Support Specialists!"
)

# Visual Ticket Triage Hero Banner
render_banner_picture("ticket_triage.png", caption="🎫 Ticket Triage & Interactive Kanban • Real-Time Queue Routing")
st.write("")

# Perspective & Filter Bar
p_col1, p_col2 = st.columns([2, 3])
with p_col1:
    perspective = st.radio(
        "View Perspective:",
        ["🌐 All Enterprise Tickets", f"📤 Raised by Me ({active_user['full_name']})", f"📥 Assigned to Me ({active_user['full_name']})"],
        horizontal=False
    )

with p_col2:
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        dept_filter = st.selectbox("Department", ["All", "HR", "IT", "ADMIN"])
    with fc2:
        status_filter = st.selectbox("Status", ["All", "OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"])
    with fc3:
        priority_filter = st.selectbox("Priority", ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"])

# Load tickets
tickets = get_tickets(
    department=dept_filter if dept_filter != "All" else None,
    status=status_filter if status_filter != "All" else None
)

if "Raised by Me" in perspective:
    tickets = [t for t in tickets if t["created_by"] == active_user["id"]]
elif "Assigned to Me" in perspective:
    tickets = [t for t in tickets if t.get("assigned_to") == active_user["id"]]

if priority_filter != "All":
    tickets = [t for t in tickets if t["priority"] == priority_filter]

st.markdown(f"**Showing {len(tickets)} tickets** in current view")

view_mode = st.radio("Display Layout", ["📊 Interactive Kanban Board", "📋 Detailed Card / Table View"], horizontal=True)

if "Detailed" in view_mode:
    for t in tickets:
        p_color = {"CRITICAL": "#EF4444", "HIGH": "#EA580C", "MEDIUM": "#2563EB", "LOW": "#10B981"}.get(t["priority"], "#6B7280")
        stat_badge = "badge-resolved" if t["status"] in ["RESOLVED", "CLOSED"] else ("badge-high" if t["status"] == "IN_PROGRESS" else "badge-open")
        cat_badge = {"HR": "badge-hr", "IT": "badge-it", "ADMIN": "badge-admin"}.get(t["department_code"], "badge-open")

        assigned_text = t.get('assignee_name') or "⚠️ Unassigned (In Queue)"

        with st.container():
            st.markdown(f"""
            <div class="om-card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <strong style="font-size: 1.1rem; color: #4338CA;">{t['ticket_code']}</strong>
                  <span class="om-badge {cat_badge}" style="margin-left: 8px;">{t['department_name']}</span>
                </div>
                <div>
                  <span class="om-badge" style="background: {p_color}20; color: {p_color};">{t['priority']} PRIORITY</span>
                  <span class="om-badge {stat_badge}">{t['status']}</span>
                </div>
              </div>
              <h4 style="margin: 8px 0 4px 0;">{t['title']}</h4>
              <p style="color: #475569; font-size: 0.92rem; margin-bottom: 8px;">{t['description']}</p>
              <div style="display:flex; flex-wrap:wrap; gap: 14px; font-size: 0.84rem; background: #F8FAFC; padding: 8px 12px; border-radius: 8px; border: 1px solid #E2E8F0;">
                <div>👤 <strong>Requester:</strong> {t['creator_name']}</div>
                <div>🛠️ <strong>Assigned Specialist:</strong> <span style="color: {'#059669' if t.get('assignee_name') else '#DC2626'}; font-weight: 700;">{assigned_text}</span></div>
                <div>📅 <strong>Created:</strong> {t['created_at']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            col_act1, col_act2, col_act3, col_act4 = st.columns([2, 2, 3, 2])
            with col_act1:
                new_st = st.selectbox(
                    "Status",
                    ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"],
                    index=["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"].index(t["status"]),
                    key=f"status_sel_{t['id']}"
                )
            with col_act2:
                curr_assignee = t.get("assigned_to")
                assign_keys = list(agent_map.keys())
                assign_idx = assign_keys.index(curr_assignee) if curr_assignee in assign_keys else 0
                new_assignee = st.selectbox(
                    "Assign Specialist",
                    assign_keys,
                    format_func=lambda x: agent_map[x],
                    index=assign_idx,
                    key=f"assign_sel_{t['id']}"
                )
            with col_act3:
                notes = st.text_input("Resolution / Triage Note", value=t.get("resolution_notes") or "", key=f"notes_{t['id']}")
            with col_act4:
                st.write("")
                if st.button("💾 Save Update", key=f"btn_up_{t['id']}", use_container_width=True):
                    update_ticket_status(t["id"], new_st, actor_id=active_user["id"], notes=notes, assigned_to=new_assignee)
                    st.success(f"Ticket {t['ticket_code']} updated!")
                    st.rerun()

else:
    # Interactive Kanban Board View
    kb_col1, kb_col2, kb_col3 = st.columns(3)
    
    with kb_col1:
        st.markdown("### 📥 Open Backlog")
        open_tkts = [t for t in tickets if t["status"] == "OPEN"]
        for t in open_tkts:
            assigned_label = t.get('assignee_name') or "⚠️ Unassigned"
            with st.container():
                st.markdown(f"""
                <div class="om-card" style="border-top: 4px solid #3B82F6; padding: 12px; margin-bottom: 8px;">
                  <div style="display:flex; justify-content:space-between;">
                    <strong>{t['ticket_code']}</strong>
                    <span class="om-badge badge-it">{t['department_code']}</span>
                  </div>
                  <div style="font-size: 0.9rem; font-weight: 700; margin: 4px 0;">{t['title']}</div>
                  <div style="font-size: 0.78rem; color: #475569; margin: 2px 0;">👤 <strong>Requester:</strong> {t['creator_name']}</div>
                  <div style="font-size: 0.78rem; color: {'#059669' if t.get('assignee_name') else '#DC2626'};">🛠️ <strong>Assigned:</strong> {assigned_label}</div>
                  <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Priority: <strong>{t['priority']}</strong></div>
                </div>
                """, unsafe_allow_html=True)
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("⏩ Start Work", key=f"kb_start_{t['id']}", use_container_width=True):
                        # If user is support agent/admin, assign to them
                        target_assignee = active_user["id"] if active_user["role"] in ["support_agent", "admin"] else t.get("assigned_to")
                        update_ticket_status(t["id"], "IN_PROGRESS", actor_id=active_user["id"], notes=f"Claimed by {active_user['full_name']}", assigned_to=target_assignee)
                        st.rerun()
                with col_btn2:
                    if t.get("assigned_to") != active_user["id"] and active_user["role"] in ["support_agent", "admin"]:
                        if st.button("🙋 Take Ticket", key=f"kb_claim_{t['id']}", use_container_width=True):
                            assign_ticket(t["id"], active_user["id"], actor_id=active_user["id"])
                            st.rerun()

    with kb_col2:
        st.markdown("### ⚙️ In Progress")
        prog_tkts = [t for t in tickets if t["status"] == "IN_PROGRESS"]
        for t in prog_tkts:
            assigned_label = t.get('assignee_name') or "⚠️ Unassigned"
            with st.container():
                st.markdown(f"""
                <div class="om-card" style="border-top: 4px solid #F59E0B; padding: 12px; margin-bottom: 8px;">
                  <div style="display:flex; justify-content:space-between;">
                    <strong>{t['ticket_code']}</strong>
                    <span class="om-badge badge-admin">{t['department_code']}</span>
                  </div>
                  <div style="font-size: 0.9rem; font-weight: 700; margin: 4px 0;">{t['title']}</div>
                  <div style="font-size: 0.78rem; color: #475569; margin: 2px 0;">👤 <strong>Requester:</strong> {t['creator_name']}</div>
                  <div style="font-size: 0.78rem; color: {'#059669' if t.get('assignee_name') else '#DC2626'};">🛠️ <strong>Assigned:</strong> {assigned_label}</div>
                  <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Priority: <strong>{t['priority']}</strong></div>
                </div>
                """, unsafe_allow_html=True)
                col_k1, col_k2 = st.columns(2)
                with col_k1:
                    if st.button("✅ Resolve", key=f"kb_res_{t['id']}", use_container_width=True):
                        update_ticket_status(t["id"], "RESOLVED", actor_id=active_user["id"], notes="Resolved via Kanban board")
                        st.rerun()
                with col_k2:
                    if st.button("↩️ Reopen", key=f"kb_reop_{t['id']}", use_container_width=True):
                        update_ticket_status(t["id"], "OPEN", actor_id=active_user["id"], notes="Returned to open queue")
                        st.rerun()

    with kb_col3:
        st.markdown("### ✅ Resolved / Closed")
        res_tkts = [t for t in tickets if t["status"] in ["RESOLVED", "CLOSED"]]
        for t in res_tkts:
            assigned_label = t.get('assignee_name') or "Closed"
            with st.container():
                st.markdown(f"""
                <div class="om-card" style="border-top: 4px solid #10B981; padding: 12px; margin-bottom: 8px;">
                  <div style="display:flex; justify-content:space-between;">
                    <strong>{t['ticket_code']}</strong>
                    <span class="om-badge badge-success">{t['status']}</span>
                  </div>
                  <div style="font-size: 0.9rem; font-weight: 700; margin: 4px 0;">{t['title']}</div>
                  <div style="font-size: 0.78rem; color: #475569; margin: 2px 0;">👤 <strong>Requester:</strong> {t['creator_name']}</div>
                  <div style="font-size: 0.78rem; color: #065F46;">🛠️ <strong>Handled by:</strong> {assigned_label}</div>
                  <div style="font-size: 0.75rem; color: #065F46; margin-top: 4px;"><em>{t.get('resolution_notes') or 'Resolution notes recorded.'}</em></div>
                </div>
                """, unsafe_allow_html=True)
                if t["status"] != "CLOSED":
                    if st.button("🔒 Close Ticket", key=f"kb_close_{t['id']}", use_container_width=True):
                        update_ticket_status(t["id"], "CLOSED", actor_id=active_user["id"], notes="Archived and closed")
                        st.rerun()
