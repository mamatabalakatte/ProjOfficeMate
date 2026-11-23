"""
Page 16: Admin Control Centre & Human-in-the-Loop (HITL)
Administrative controls, policy conflict review queue, audit logs, and system configuration.
"""

import streamlit as st
from db.database import query_all, execute_update, log_audit, resolve_policy_conflict
from frontend.components.illustrations import render_banner_picture
from agents.specialized_tools import detect_policy_conflicts

st.set_page_config(page_title="Admin Control Centre | OfficeMate 2.0", page_icon="⚙️", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #111827 0%, #1F2937 50%, #374151 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">⚙️ Admin Control Centre &amp; HITL Triage</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.9;">
      Human-in-the-loop review queue, policy conflict resolution, user permissions, and persistent audit logs.
    </p>
  </div>
  <div>
    <span class="om-badge badge-critical" style="background: white; color: #DC2626;">Superuser Access</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Mission Control Superuser Hero Banner
render_banner_picture("admin_control.png", caption="⚙️ Admin Control Centre & HITL Governance • System Audit Trails")
st.write("")

tab_hitl, tab_conflicts, tab_audit, tab_users = st.tabs([
    "🤝 Human-in-the-Loop Review Queue",
    "⚠️ Policy Conflict Detector",
    "📜 Immutable Audit Logs",
    "👥 User & Role Management"
])

with tab_hitl:
    st.markdown("#### Human Review for Automated Ticket Triage")
    st.caption("Review tickets created automatically by the AI Assistant to confirm or override routing.")
    
    auto_tickets = query_all("SELECT t.*, d.name as dept_name, d.code as dept_code FROM tickets t JOIN departments d ON t.department_id = d.id WHERE t.description LIKE '%Automatic Ticket Routing%' OR t.description LIKE '%Auto-generated%' ORDER BY t.created_at DESC")
    
    if not auto_tickets:
        st.info("No tickets currently pending human-in-the-loop review.")
    else:
        for t in auto_tickets:
            with st.container():
                st.markdown(f"""
                <div class="om-card">
                  <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color: #4F46E5;">{t['ticket_code']}</strong>
                    <span class="om-badge badge-high">Status: {t['status']}</span>
                  </div>
                  <h4 style="margin: 6px 0;">{t['title']}</h4>
                  <p style="color: #475569; font-size: 0.9rem;">{t['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_ov1, col_ov2 = st.columns([2, 1])
                with col_ov1:
                    new_dept = st.selectbox(
                        "Override Routing Department",
                        ["HR", "IT", "ADMIN"],
                        index=["HR", "IT", "ADMIN"].index(t["dept_code"]) if t["dept_code"] in ["HR", "IT", "ADMIN"] else 0,
                        key=f"hitl_dept_{t['id']}"
                    )
                with col_ov2:
                    st.write("")
                    if st.button("✅ Confirm & Approve Routing", key=f"btn_hitl_{t['id']}", use_container_width=True):
                        dept_id = {"HR": 1, "IT": 2, "ADMIN": 3}.get(new_dept, 1)
                        execute_update("UPDATE tickets SET department_id = ? WHERE id = ?", (dept_id, t["id"]))
                        log_audit(4, "HITL_APPROVE_ROUTING", f"tickets:{t['id']}", f"Admin confirmed routing to {new_dept}")
                        st.success(f"Routing confirmed for {t['ticket_code']} to {new_dept}!")
                        st.rerun()

with tab_conflicts:
    st.markdown("#### Detected Policy Contradictions & Outdated Clauses")
    conflicts = detect_policy_conflicts()
    if not conflicts:
        st.success("Zero policy contradictions detected across official documentation.")
    else:
        for c in conflicts:
            st.markdown(f"""
            <div class="om-card" style="border-left: 6px solid #F59E0B;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color: #B45309;">Conflict: {c['conflict_type']}</strong>
                <span class="om-badge badge-high">{c.get('status', 'DETECTED')}</span>
              </div>
              <div style="font-size: 0.9rem; color: #1E293B; margin: 8px 0;">
                <strong>Source Documents:</strong> <em>{c.get('doc1_title', 'Handbook A')}</em> ⚡ <em>{c.get('doc2_title', 'Handbook B')}</em>
              </div>
              <p style="color: #475569; font-size: 0.88rem; margin: 0;">{c['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            if c.get('status') != 'RESOLVED':
                if st.button("⚖️ Mark Conflict Resolved & Synchronized", key=f"btn_conf_{c['id']}", use_container_width=True):
                    resolve_policy_conflict(c['id'])
                    st.success("Policy contradiction marked as resolved and logged in audit trail!")
                    st.rerun()

with tab_audit:
    st.markdown("#### System Security & Operation Audit Trail")
    logs = query_all("SELECT a.*, u.full_name as actor_name FROM audit_logs a LEFT JOIN users u ON a.user_id = u.id ORDER BY a.created_at DESC LIMIT 20")
    for lg in logs:
        st.markdown(f"""
        <div style="padding: 10px 14px; background: white; border: 1px solid #E2E8F0; border-radius: 8px; margin-bottom: 8px; font-size: 0.88rem;">
          <div style="display:flex; justify-content:space-between; color: #64748B;">
            <span>📅 {lg['created_at']} • Actor: <strong>{lg.get('actor_name') or 'System Engine'}</strong></span>
            <code>{lg['ip_address']}</code>
          </div>
          <div style="margin-top: 4px;">
            <strong style="color: #4338CA;">[{lg['action']}]</strong> {lg['details']} (Target: <code>{lg['target_entity']}</code>)
          </div>
        </div>
        """, unsafe_allow_html=True)

with tab_users:
    st.markdown("#### Enterprise User Roster & Permissions")
    users = query_all("SELECT u.*, d.name as dept_name FROM users u LEFT JOIN departments d ON u.department_id = d.id")
    for u in users:
        st.markdown(f"""
        <div class="om-card" style="padding: 12px 18px; margin-bottom: 8px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong>{u['full_name']}</strong> ({u['username']})
            <span class="om-badge badge-it">{u['role'].upper()}</span>
          </div>
          <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">
            Email: {u['email']} • Department: {u.get('dept_name') or 'General'}
          </div>
        </div>
        """, unsafe_allow_html=True)
