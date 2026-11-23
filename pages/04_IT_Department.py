"""
Page 4: IT Department Portal
Technical troubleshooting, VPN/login support, software licenses,
screenshot OCR diagnostics, and IT tickets.
"""

import streamlit as st
from db.database import get_tickets, create_ticket, get_knowledge_docs
from agents.specialized_tools import diagnose_screenshot_or_error
from frontend.components.illustrations import render_banner_picture
from frontend.components.user_context import get_active_user, render_user_profile_sidebar

st.set_page_config(page_title="IT Department | OfficeMate 2.0", page_icon="💻", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Render Dynamic Sidebar Profile
render_user_profile_sidebar()
active_user = get_active_user()

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">💻 IT Command Center &amp; Helpdesk</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.95;">
      Network operations, VPN tunnels, hardware provisioning, and automated system diagnostics.
    </p>
  </div>
  <div>
    <span class="om-badge badge-it" style="background: white; color: #4338CA;">Department Lead: David Kim</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual IT Command Hero Banner
render_banner_picture("it_command.png", caption="💻 IT Command Center • Infrastructure Telemetry & Helpdesk")
st.write("")

# Live System Health Strip
st.subheader("⚡ Core Enterprise Infrastructure Status")
sc1, sc2, sc3, sc4 = st.columns(4)
with sc1:
    st.markdown("""
    <div class="stat-box">
      <div style="font-size: 1.4rem; font-weight: 800; color: #10B981;">🟢 OPERATIONAL</div>
      <div class="stat-label">GlobalProtect VPN (vpn.internal)</div>
    </div>
    """, unsafe_allow_html=True)
with sc2:
    st.markdown("""
    <div class="stat-box">
      <div style="font-size: 1.4rem; font-weight: 800; color: #10B981;">🟢 99.98%</div>
      <div class="stat-label">Okta MFA / SSO Service</div>
    </div>
    """, unsafe_allow_html=True)
with sc3:
    st.markdown("""
    <div class="stat-box">
      <div style="font-size: 1.4rem; font-weight: 800; color: #F59E0B;">🟡 DEGRADED</div>
      <div class="stat-label">Docker Enterprise Hub</div>
    </div>
    """, unsafe_allow_html=True)
with sc4:
    st.markdown("""
    <div class="stat-box">
      <div style="font-size: 1.4rem; font-weight: 800; color: #10B981;">🟢 NORMAL</div>
      <div class="stat-label">Corporate WiFi (Floor 1-3)</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
tab_diag, tab_request, tab_docs, tab_tickets = st.tabs([
    "🔍 Screenshot & Log Diagnostic",
    "🛠️ Submit IT Ticket",
    "📚 IT Documentation",
    "🎫 IT Queue"
])

with tab_diag:
    st.markdown("#### 📸 Automated Screenshot & Error Log Diagnostic OCR")
    st.caption("Paste an error message or upload an error log/screenshot to run automated diagnosis against IT runbooks.")
    
    col_up, col_res = st.columns([1, 1])
    with col_up:
        err_input = st.text_area(
            "Paste Error Output or Diagnostic String",
            value="GlobalProtect VPN connection failed: Error 403 Gateway Authentication Timeout (MFA push expired)",
            height=130
        )
        run_diag = st.button("🔬 Analyze Error & Find Runbook", use_container_width=True)

    with col_res:
        if run_diag or err_input:
            diag = diagnose_screenshot_or_error(err_input)
            sev_badge = "badge-critical" if diag["severity"] == "CRITICAL" else ("badge-high" if diag["severity"] == "HIGH" else "badge-open")
            st.markdown(f"""
            <div class="om-card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="om-badge {sev_badge}">{diag['severity']} SEVERITY</span>
                <span style="font-family: monospace; font-size: 0.85rem; font-weight: 700;">{diag['matched_code']}</span>
              </div>
              <h4 style="margin: 8px 0 4px 0; color: #1E293B;">{diag['error_category']}</h4>
              <p style="color: #475569; font-size: 0.92rem; margin-bottom: 8px;"><strong>Diagnosis:</strong> {diag['diagnosis']}</p>
              <div style="background: #F1F5F9; padding: 10px; border-radius: 8px; font-size: 0.88rem; color: #0F172A; border-left: 4px solid #4F46E5;">
                <strong>Recommended Runbook Fix:</strong><br>{diag['suggested_fix']}
              </div>
            </div>
            """, unsafe_allow_html=True)

with tab_request:
    st.markdown("#### Submit Technical Request / Hardware Ticket")
    with st.form("it_request_form"):
        req_type = st.selectbox(
            "Issue Category",
            ["VPN & Network Failure", "Software / IDE License (Docker, PyCharm)", "Laptop / Hardware Malfunction", "Password & MFA Reset", "Cloud Access (AWS/GCP)"]
        )
        title = st.text_input("Summary Title", placeholder="e.g. Broken laptop trackpad or VPN timeout")
        details = st.text_area("Detailed Description & Steps to Reproduce", placeholder="Explain the error code, device model, or software version...")
        priority = st.selectbox("Priority Level", ["LOW", "MEDIUM", "HIGH", "CRITICAL"], index=2)
        
        submit_it = st.form_submit_button("🚀 Submit IT Ticket", use_container_width=True)
        if submit_it:
            if not title.strip() or not details.strip():
                st.error("Please fill in both title and detailed description.")
            else:
                ticket = create_ticket(title, details, "IT", priority, created_by=active_user["id"])
                st.success(f"✅ IT Support Ticket `{ticket['ticket_code']}` opened on behalf of **{active_user['full_name']}**! Priority: `{ticket['priority']}`. David Kim has been notified.")

with tab_docs:
    st.markdown("#### IT Runbooks & Security Standards")
    docs = get_knowledge_docs(category="IT")
    for doc in docs:
        with st.expander(f"📘 {doc['title']} (v{doc['version']})", expanded=True):
            st.write(doc["content"])
            st.caption(f"Tags: {doc['tags']}")

with tab_tickets:
    st.markdown("#### Active IT Support Tickets")
    tickets = get_tickets(department="IT")
    for t in tickets:
        p_color = {"CRITICAL": "#EF4444", "HIGH": "#EA580C", "MEDIUM": "#2563EB", "LOW": "#10B981"}.get(t["priority"], "#6B7280")
        st.markdown(f"""
        <div class="om-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 800; color: #4338CA;">{t['ticket_code']}</span>
            <div>
              <span class="om-badge" style="background: {p_color}20; color: {p_color};">{t['priority']}</span>
              <span class="om-badge badge-it">{t['status']}</span>
            </div>
          </div>
          <h4 style="margin: 8px 0 4px 0;">{t['title']}</h4>
          <p style="color: #475569; font-size: 0.9rem;">{t['description']}</p>
        </div>
        """, unsafe_allow_html=True)
