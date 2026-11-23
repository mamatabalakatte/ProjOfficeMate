"""
Page 17: Cafeteria & Social Lounge
Section 2 Requirement: Office events, celebrations, workplace announcements, and relaxation area.
"""

import streamlit as st
from frontend.components.illustrations import render_banner_picture
from db.database import get_active_announcements, query_all

st.set_page_config(page_title="Cafeteria & Lounge | OfficeMate 2.0", page_icon="☕", layout="wide")

with open("frontend/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="om-header" style="background: linear-gradient(135deg, #059669 0%, #10B981 50%, #34D399 100%);">
  <div>
    <h1 style="margin:0; font-size: 1.8rem; font-weight: 800;">☕ 2nd Floor Cafeteria &amp; Social Lounge</h1>
    <p style="margin: 0.25rem 0 0 0; opacity: 0.95;">
      Workplace celebrations, artisan espresso bar, organic lunch specials, and team social relaxation.
    </p>
  </div>
  <div>
    <span class="om-badge badge-success" style="background: white; color: #059669;">Espresso Bar Open</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Visual Hero Illustration
render_banner_picture("cafeteria.png", caption="☕ 2nd Floor Cafeteria & Social Lounge • Espresso Bar & Lunch Specials")
st.write("")

tab_menu, tab_events, tab_kudos, tab_coffee = st.tabs([
    "🥗 Daily Artisan Menu",
    "🎉 Upcoming Office Celebrations",
    "⭐ Peer Kudos & Shoutouts",
    "☕ Random Coffee Chat Matcher"
])

with tab_menu:
    st.subheader("🍴 Today's Chef Specials (Organic & Fresh)")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
        <div class="om-card">
          <span class="om-badge badge-success">Organic Salad</span>
          <h4 style="margin: 8px 0 4px 0;">Mediterranean Grain Bowl</h4>
          <p style="color: #64748B; font-size: 0.88rem;">Quinoa, roasted chickpeas, organic kale, kalamata olives, tahini lemon dressing.</p>
          <strong style="color: #059669;">$8.50 (50% subsidized: $4.25)</strong>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="om-card">
          <span class="om-badge badge-hr">Chef's Hot Entrée</span>
          <h4 style="margin: 8px 0 4px 0;">Grilled Pan-Seared Salmon</h4>
          <p style="color: #64748B; font-size: 0.88rem;">Wild Alaskan salmon, asparagus risotto, dill lemon butter emulsion.</p>
          <strong style="color: #059669;">$12.00 (50% subsidized: $6.00)</strong>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="om-card">
          <span class="om-badge badge-it">Artisan Espresso</span>
          <h4 style="margin: 8px 0 4px 0;">Vanilla Bean Oat Flat White</h4>
          <p style="color: #64748B; font-size: 0.88rem;">Locally roasted single-origin Ethiopian beans, steamed organic oat milk.</p>
          <strong style="color: #059669;">Free for Employees</strong>
        </div>
        """, unsafe_allow_html=True)

with tab_events:
    st.subheader("🎈 Upcoming Workplace Social Celebrations")
    events = [
        {"title": "Annual Company Town Hall & Hackathon Kickoff", "date": "Thursday, 3:00 PM", "loc": "Synergy Boardroom & Virtual Stream", "type": "Company Wide"},
        {"title": "Welcome Coffee Social for New Hires", "date": "Friday, 10:30 AM", "loc": "Cafeteria Espresso Lounge", "type": "Culture"},
        {"title": "Friday Team Happy Hour & Trivia Quiz", "date": "Friday, 5:00 PM", "loc": "Outdoor Rooftop Terrace", "type": "Social"}
    ]
    for ev in events:
        st.markdown(f"""
        <div class="om-card" style="border-left: 5px solid #10B981;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong>{ev['title']}</strong>
            <span class="om-badge badge-success">{ev['type']}</span>
          </div>
          <div style="font-size: 0.88rem; color: #475569; margin-top: 6px;">
            📅 <strong>{ev['date']}</strong> • 📍 Location: <em>{ev['loc']}</em>
          </div>
        </div>
        """, unsafe_allow_html=True)

with tab_kudos:
    st.subheader("⭐ Send Peer Kudos & Appreciation")
    with st.form("kudos_form"):
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            recipient = st.selectbox("Colleague", ["Sarah Jenkins (HR)", "David Kim (IT)", "Marcus Vance (Admin)", "Priya Sharma (Eng)", "Elena Rostova (Facilities)"])
        with col_k2:
            badge_type = st.selectbox("Award Badge", ["🏆 Problem Solver", "🚀 Team Player", "🌟 Innovation Champion", "❤️ Helpful Mentor"])
        message = st.text_area("Appreciation Message", placeholder="Thank you for helping me resolve the VPN issue so quickly today!")
        kudos_submit = st.form_submit_button("🌟 Post Kudos on Noticeboard", use_container_width=True)
        if kudos_submit:
            if not message.strip():
                st.error("Please enter a short appreciation note.")
            else:
                st.success(f"🎉 Kudos '{badge_type}' sent to {recipient}! Posted on the office noticeboard.")

with tab_coffee:
    st.subheader("🤝 Coffee Roulette & Cross-Team Networking")
    st.caption("Get paired with a colleague from another department for an informal 15-minute coffee chat.")
    if st.button("🎲 Match Me for Coffee Roulette!", use_container_width=True):
        st.success("🎉 You've been paired with **Priya Sharma (HR / Engineering)** for a 15-min coffee catchup this Wednesday at 3:15 PM in the 2nd Floor Espresso Lounge!")
