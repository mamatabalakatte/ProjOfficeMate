"""
High-Resolution Cartoon SVG Vector Illustrations & PNG Pictures for OfficeMate 2.0
Provides self-contained, crisp illustrations for all workplace areas.
"""

import os
import streamlit as st

IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")

def render_banner_picture(filename: str, caption: str = ""):
    """Renders a real PNG picture in Streamlit using st.image()."""
    path = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(path):
        try:
            st.image(path, width="stretch", caption=caption if caption else None)
        except TypeError:
            st.image(path, use_container_width=True, caption=caption if caption else None)
    else:
        st.info(f"Visual banner: {filename}")


def get_hr_illustration(width: str = "100%", height: int = 180) -> str:
    """Cartoon illustration of HR People Lounge."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 12px rgba(236,72,153,0.15);">
      <defs>
        <linearGradient id="hrBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FCE7F3"/>
          <stop offset="100%" stop-color="#FBCFE8"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#hrBg)" rx="14"/>
      <!-- Window with city sunrise -->
      <rect x="30" y="25" width="110" height="90" rx="8" fill="#FEF08A" stroke="#F472B6" stroke-width="3"/>
      <line x1="85" y1="25" x2="85" y2="115" stroke="#F472B6" stroke-width="2"/>
      <line x1="30" y1="70" x2="140" y2="70" stroke="#F472B6" stroke-width="2"/>
      <circle cx="85" cy="55" r="14" fill="#F59E0B" opacity="0.6"/>
      <!-- Cozy HR Armchair -->
      <path d="M 180 140 C 180 90, 240 90, 240 140 Z" fill="#EC4899"/>
      <rect x="170" y="125" width="20" height="35" rx="6" fill="#DB2777"/>
      <rect x="230" y="125" width="20" height="35" rx="6" fill="#DB2777"/>
      <circle cx="210" cy="115" r="16" fill="#FDF2F8"/>
      <!-- Coffee table with mug & plant -->
      <rect x="270" y="130" width="70" height="30" rx="4" fill="#F472B6"/>
      <line x1="280" y1="160" x2="280" y2="175" stroke="#BE185D" stroke-width="3"/>
      <line x1="330" y1="160" x2="330" y2="175" stroke="#BE185D" stroke-width="3"/>
      <!-- Mug -->
      <rect x="285" y="120" width="12" height="12" rx="2" fill="#FFFFFF"/>
      <!-- Potted Monstera Plant -->
      <circle cx="480" cy="120" r="26" fill="#10B981"/>
      <circle cx="465" cy="105" r="16" fill="#34D399"/>
      <circle cx="495" cy="110" r="18" fill="#059669"/>
      <polygon points="465,145 495,145 490,175 470,175" fill="#D97706"/>
      <!-- Sarah (HR Lead Avatar) -->
      <circle cx="390" cy="80" r="24" fill="#FCD34D"/>
      <path d="M 366 70 C 366 50, 414 50, 414 70 Z" fill="#B45309"/>
      <circle cx="382" cy="80" r="3" fill="#1E293B"/>
      <circle cx="398" cy="80" r="3" fill="#1E293B"/>
      <path d="M 384 88 Q 390 94 396 88" stroke="#1E293B" stroke-width="2" fill="none"/>
      <!-- Speech Bubble -->
      <path d="M 425 45 Q 430 30 450 30 L 550 30 Q 570 30 570 50 L 570 70 Q 570 90 550 90 L 450 90 Q 430 90 425 75 Z" fill="#FFFFFF" stroke="#EC4899" stroke-width="2"/>
      <text x="495" y="55" fill="#BE185D" font-size="12" font-weight="800" text-anchor="middle">HR People Lounge</text>
      <text x="495" y="73" fill="#64748B" font-size="10" font-weight="600" text-anchor="middle">Leaves • Wellness • Benefits</text>
    </svg>
    """

def get_it_illustration(width: str = "100%", height: int = 180) -> str:
    """Cartoon illustration of IT Command Center."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 12px rgba(79,70,229,0.15);">
      <defs>
        <linearGradient id="itBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1E1B4B"/>
          <stop offset="50%" stop-color="#312E81"/>
          <stop offset="100%" stop-color="#4338CA"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#itBg)" rx="14"/>
      <!-- Server Rack 1 with blinking lights -->
      <rect x="40" y="30" width="60" height="140" rx="6" fill="#0F172A" stroke="#38BDF8" stroke-width="2"/>
      <circle cx="55" cy="48" r="4" fill="#10B981"/>
      <circle cx="70" cy="48" r="4" fill="#10B981"/>
      <circle cx="85" cy="48" r="4" fill="#38BDF8"/>
      <line x1="48" y1="65" x2="92" y2="65" stroke="#38BDF8" stroke-width="2"/>
      <circle cx="55" cy="80" r="4" fill="#10B981"/>
      <circle cx="70" cy="80" r="4" fill="#F59E0B"/>
      <circle cx="85" cy="80" r="4" fill="#10B981"/>
      <line x1="48" y1="95" x2="92" y2="95" stroke="#38BDF8" stroke-width="2"/>
      <circle cx="55" cy="112" r="4" fill="#10B981"/>
      <circle cx="70" cy="112" r="4" fill="#10B981"/>
      <circle cx="85" cy="112" r="4" fill="#10B981"/>
      <line x1="48" y1="130" x2="92" y2="130" stroke="#38BDF8" stroke-width="2"/>
      <!-- Dual Monitors Workstation -->
      <rect x="150" y="55" width="80" height="50" rx="4" fill="#0F172A" stroke="#818CF8" stroke-width="2"/>
      <rect x="154" y="59" width="72" height="42" fill="#0284C7"/>
      <text x="190" y="84" fill="#FFFFFF" font-size="10" font-family="monospace" font-weight="700" text-anchor="middle">&gt; VPN: OK</text>
      <rect x="240" y="55" width="80" height="50" rx="4" fill="#0F172A" stroke="#818CF8" stroke-width="2"/>
      <rect x="244" y="59" width="72" height="42" fill="#047857"/>
      <text x="280" y="84" fill="#A7F3D0" font-size="10" font-family="monospace" font-weight="700" text-anchor="middle">&gt; 0 ALERTS</text>
      <!-- Workstation Desk -->
      <rect x="135" y="110" width="200" height="15" rx="3" fill="#64748B"/>
      <!-- David (IT Lead Avatar) -->
      <circle cx="235" cy="140" r="22" fill="#FBBF24"/>
      <path d="M 213 130 C 213 112, 257 112, 257 130 Z" fill="#1E293B"/>
      <!-- Network Radar Rings on Right -->
      <circle cx="480" cy="100" r="60" stroke="#818CF8" stroke-width="1.5" stroke-dasharray="4,4" fill="none" opacity="0.4"/>
      <circle cx="480" cy="100" r="40" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="4,4" fill="none" opacity="0.6"/>
      <circle cx="480" cy="100" r="20" stroke="#34D399" stroke-width="2" fill="#10B981" opacity="0.8"/>
      <!-- Floating Hologram Text -->
      <rect x="400" y="30" width="160" height="40" rx="8" fill="#1E1B4B" stroke="#38BDF8" stroke-width="1.5"/>
      <text x="480" y="48" fill="#38BDF8" font-size="12" font-weight="800" text-anchor="middle">IT Command Center</text>
      <text x="480" y="62" fill="#93C5FD" font-size="9" font-weight="600" text-anchor="middle">VPN • Infrastructure • Triage</text>
    </svg>
    """

def get_admin_illustration(width: str = "100%", height: int = 180) -> str:
    """Cartoon illustration of Administration & Facilities."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 12px rgba(245,158,11,0.15);">
      <defs>
        <linearGradient id="adminBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FEF3C7"/>
          <stop offset="100%" stop-color="#FDE68A"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#adminBg)" rx="14"/>
      <!-- Modern Facility Wall Shelves with binders -->
      <rect x="40" y="35" width="160" height="70" rx="4" fill="#FFFFFF" stroke="#D97706" stroke-width="2"/>
      <rect x="55" y="45" width="14" height="50" rx="2" fill="#EF4444"/>
      <rect x="73" y="45" width="14" height="50" rx="2" fill="#3B82F6"/>
      <rect x="91" y="45" width="14" height="50" rx="2" fill="#10B981"/>
      <rect x="109" y="45" width="14" height="50" rx="2" fill="#F59E0B"/>
      <!-- Travel Suitcase & Delivery Boxes -->
      <rect x="230" y="90" width="65" height="50" rx="8" fill="#B45309" stroke="#78350F" stroke-width="2"/>
      <rect x="250" y="80" width="25" height="12" rx="3" fill="#4B5563"/>
      <line x1="230" y1="115" x2="295" y2="115" stroke="#FDE68A" stroke-width="2"/>
      <!-- Delivery Parcel -->
      <rect x="310" y="105" width="45" height="35" rx="3" fill="#D97706" stroke="#92400E" stroke-width="1.5"/>
      <line x1="310" y1="122" x2="355" y2="122" stroke="#FFFFFF" stroke-width="2"/>
      <!-- Ergonomic Desk Chair -->
      <circle cx="410" cy="85" r="18" fill="#374151"/>
      <rect x="402" y="105" width="16" height="35" rx="4" fill="#1E293B"/>
      <line x1="390" y1="140" x2="430" y2="140" stroke="#1E293B" stroke-width="3"/>
      <!-- Admin Officer Avatar (Marcus) -->
      <circle cx="490" cy="80" r="24" fill="#F59E0B"/>
      <path d="M 466 70 C 466 50, 514 50, 514 70 Z" fill="#4B5563"/>
      <circle cx="482" cy="80" r="3" fill="#1E293B"/>
      <circle cx="498" cy="80" r="3" fill="#1E293B"/>
      <path d="M 484 88 Q 490 94 496 88" stroke="#1E293B" stroke-width="2" fill="none"/>
      <!-- Badge Banner -->
      <rect x="40" y="130" width="170" height="34" rx="8" fill="#FFFFFF" stroke="#B45309" stroke-width="1.5"/>
      <text x="125" y="146" fill="#92400E" font-size="11" font-weight="800" text-anchor="middle">Administration &amp; Travel</text>
      <text x="125" y="158" fill="#64748B" font-size="9" font-weight="600" text-anchor="middle">Per Diem • Passes • Logistics</text>
    </svg>
    """

def get_boardroom_illustration(width: str = "100%", height: int = 180) -> str:
    """Cartoon illustration of Synergy Boardroom."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 12px rgba(139,92,246,0.15);">
      <defs>
        <linearGradient id="meetBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#EDE9FE"/>
          <stop offset="100%" stop-color="#DDD6FE"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#meetBg)" rx="14"/>
      <!-- Wall Presentation 4K Screen with Video Conference -->
      <rect x="180" y="20" width="240" height="70" rx="8" fill="#0F172A" stroke="#7C3AED" stroke-width="3"/>
      <rect x="190" y="26" width="64" height="58" rx="4" fill="#3B82F6"/>
      <circle cx="222" cy="50" r="14" fill="#FCD34D"/>
      <rect x="268" y="26" width="64" height="58" rx="4" fill="#10B981"/>
      <circle cx="300" cy="50" r="14" fill="#FBBF24"/>
      <rect x="346" y="26" width="64" height="58" rx="4" fill="#EC4899"/>
      <circle cx="378" cy="50" r="14" fill="#F472B6"/>
      <!-- Conference Oval Table -->
      <ellipse cx="300" cy="140" rx="190" ry="36" fill="#C4B5FD" stroke="#6D28D9" stroke-width="2.5"/>
      <!-- Chairs -->
      <circle cx="160" cy="115" r="14" fill="#7C3AED"/>
      <circle cx="230" cy="105" r="14" fill="#7C3AED"/>
      <circle cx="300" cy="102" r="14" fill="#7C3AED"/>
      <circle cx="370" cy="105" r="14" fill="#7C3AED"/>
      <circle cx="440" cy="115" r="14" fill="#7C3AED"/>
      <!-- Polycom Conference Speaker in Center -->
      <circle cx="300" cy="140" r="10" fill="#1E1B4B"/>
      <!-- Badge -->
      <rect x="30" y="25" width="125" height="40" rx="8" fill="#FFFFFF" stroke="#8B5CF6" stroke-width="1.5"/>
      <text x="92" y="42" fill="#6D28D9" font-size="11" font-weight="800" text-anchor="middle">Synergy Boardroom</text>
      <text x="92" y="56" fill="#64748B" font-size="9" font-weight="600" text-anchor="middle">Floor 3 • 16 Seats • Zoom</text>
    </svg>
    """

def get_cafeteria_illustration(width: str = "100%", height: int = 180) -> str:
    """Cartoon illustration of Cafeteria & Espresso Lounge."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 12px rgba(16,185,129,0.15);">
      <defs>
        <linearGradient id="cafeBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#D1FAE5"/>
          <stop offset="100%" stop-color="#A7F3D0"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#cafeBg)" rx="14"/>
      <!-- Party Bunting Celebration Flags -->
      <polygon points="40,20 60,40 80,20" fill="#EF4444"/>
      <polygon points="80,20 100,40 120,20" fill="#3B82F6"/>
      <polygon points="120,20 140,40 160,20" fill="#F59E0B"/>
      <polygon points="160,20 180,40 200,20" fill="#10B981"/>
      <polygon points="200,20 220,40 240,20" fill="#EC4899"/>
      <polygon points="240,20 260,40 280,20" fill="#8B5CF6"/>
      <!-- Espresso Bar Counter -->
      <rect x="50" y="70" width="180" height="80" rx="8" fill="#047857"/>
      <rect x="65" y="80" width="50" height="40" rx="4" fill="#064E3B"/>
      <circle cx="80" cy="95" r="4" fill="#F59E0B"/>
      <circle cx="100" cy="95" r="4" fill="#10B981"/>
      <!-- Coffee Steam -->
      <path d="M 80 75 Q 82 65 78 55" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.8"/>
      <path d="M 98 75 Q 100 65 96 55" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.8"/>
      <!-- Bistro Round Table & Chairs -->
      <circle cx="380" cy="120" r="36" fill="#FFFFFF" stroke="#059669" stroke-width="2"/>
      <circle cx="320" cy="120" r="12" fill="#059669"/>
      <circle cx="440" cy="120" r="12" fill="#059669"/>
      <!-- Cupcake on Bistro Table -->
      <circle cx="380" cy="120" r="8" fill="#EC4899"/>
      <rect x="376" y="120" width="8" height="6" fill="#D97706"/>
      <!-- Lounge Sofa -->
      <rect x="480" y="90" width="90" height="50" rx="8" fill="#34D399" stroke="#059669" stroke-width="2"/>
      <!-- Banner Badge -->
      <rect x="300" y="25" width="260" height="36" rx="8" fill="#FFFFFF" stroke="#10B981" stroke-width="1.5"/>
      <text x="430" y="42" fill="#047857" font-size="11" font-weight="800" text-anchor="middle">☕ 2nd Floor Cafeteria &amp; Social</text>
      <text x="430" y="54" fill="#64748B" font-size="9" font-weight="600" text-anchor="middle">Espresso Bar • Organic Salads • Celebrations</text>
    </svg>
    """

def get_ai_assistant_illustration(width: str = "100%", height: int = 160) -> str:
    """Cartoon illustration of AI Holo-Bot Assistant."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 160" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 12px rgba(99,102,241,0.15);">
      <defs>
        <linearGradient id="aiBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#312E81"/>
          <stop offset="50%" stop-color="#4338CA"/>
          <stop offset="100%" stop-color="#6366F1"/>
        </linearGradient>
      </defs>
      <rect width="600" height="160" fill="url(#aiBg)" rx="14"/>
      <!-- Cute Floating AI Robot -->
      <circle cx="100" cy="80" r="40" fill="#EEF2FF" stroke="#38BDF8" stroke-width="3"/>
      <!-- Antenna with glowing pulse -->
      <line x1="100" y1="40" x2="100" y2="25" stroke="#38BDF8" stroke-width="3"/>
      <circle cx="100" cy="22" r="6" fill="#38BDF8"/>
      <!-- Digital Eyes -->
      <ellipse cx="86" cy="76" rx="7" ry="10" fill="#0284C7"/>
      <ellipse cx="114" cy="76" rx="7" ry="10" fill="#0284C7"/>
      <circle cx="84" cy="73" r="2.5" fill="#FFFFFF"/>
      <circle cx="112" cy="73" r="2.5" fill="#FFFFFF"/>
      <!-- Digital Smile -->
      <path d="M 88 95 Q 100 105 112 95" stroke="#0284C7" stroke-width="3" stroke-linecap="round" fill="none"/>
      <!-- Rosy Cheeks -->
      <circle cx="78" cy="86" r="4" fill="#F472B6" opacity="0.6"/>
      <circle cx="122" cy="86" r="4" fill="#F472B6" opacity="0.6"/>
      <!-- Floating Speech Bubble -->
      <rect x="170" y="30" width="390" height="95" rx="12" fill="#FFFFFF"/>
      <polygon points="170,75 152,80 170,90" fill="#FFFFFF"/>
      <text x="195" y="58" fill="#1E1B4B" font-size="14" font-weight="800">Hi! I'm OfficeMate AI</text>
      <text x="195" y="80" fill="#475569" font-size="11" font-weight="600">Dual NLP Engine: Bidirectional LSTM Deep Learning + RAG Policy Retrieval</text>
      <text x="195" y="102" fill="#4338CA" font-size="10" font-weight="700">Ask any workplace policy, IT issue, or request automated ticket routing!</text>
    </svg>
    """

def get_workspace_illustration(width: str = "100%", height: int = 180) -> str:
    """Futuristic personal cockpit illustration for Employee Workspace."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(79,70,229,0.15);">
      <defs>
        <linearGradient id="wsBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1E1B4B"/>
          <stop offset="50%" stop-color="#312E81"/>
          <stop offset="100%" stop-color="#4F46E5"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#wsBg)" rx="14"/>
      <!-- Curved Holographic Multi-Monitor Cockpit -->
      <path d="M 50 140 Q 150 70 300 70 Q 450 70 550 140" stroke="#818CF8" stroke-width="3" fill="none" opacity="0.6"/>
      <!-- Monitor 1 (Left - Calendar/Tasks) -->
      <rect x="70" y="50" width="110" height="75" rx="6" fill="#0F172A" stroke="#38BDF8" stroke-width="2"/>
      <rect x="78" y="58" width="94" height="14" rx="2" fill="#0284C7"/>
      <text x="125" y="69" fill="#FFFFFF" font-size="9" font-weight="700" text-anchor="middle">TODAY'S AGENDA</text>
      <circle cx="88" cy="85" r="4" fill="#10B981"/><line x1="98" y1="85" x2="160" y2="85" stroke="#94A3B8" stroke-width="2"/>
      <circle cx="88" cy="102" r="4" fill="#38BDF8"/><line x1="98" y1="102" x2="150" y2="102" stroke="#94A3B8" stroke-width="2"/>
      <circle cx="88" cy="116" r="4" fill="#F59E0B"/><line x1="98" y1="116" x2="140" y2="116" stroke="#94A3B8" stroke-width="2"/>
      <!-- Monitor 2 (Center - Active Code & Analytics) -->
      <rect x="200" y="30" width="200" height="100" rx="6" fill="#0F172A" stroke="#818CF8" stroke-width="2.5"/>
      <rect x="208" y="38" width="184" height="20" rx="3" fill="#312E81"/>
      <text x="300" y="52" fill="#E0E7FF" font-size="10" font-weight="800" text-anchor="middle">EMPLOYEE INTELLIGENCE COCKPIT</text>
      <!-- Mini Chart inside Monitor -->
      <polyline points="220,110 250,90 280,98 310,75 340,82 370,68" fill="none" stroke="#34D399" stroke-width="2.5"/>
      <circle cx="370" cy="68" r="4" fill="#10B981"/>
      <!-- Monitor 3 (Right - Virtual Office Live Telemetry) -->
      <rect x="420" y="50" width="110" height="75" rx="6" fill="#0F172A" stroke="#EC4899" stroke-width="2"/>
      <rect x="428" y="58" width="94" height="14" rx="2" fill="#BE185D"/>
      <text x="475" y="69" fill="#FFFFFF" font-size="9" font-weight="700" text-anchor="middle">HQ STATUS: 94%</text>
      <circle cx="475" cy="98" r="16" fill="none" stroke="#F472B6" stroke-width="3" stroke-dasharray="6,4"/>
      <!-- Desk & Accessories -->
      <rect x="30" y="145" width="540" height="16" rx="4" fill="#334155"/>
      <!-- Glowing mechanical keyboard -->
      <rect x="240" y="135" width="120" height="22" rx="4" fill="#1E293B" stroke="#38BDF8" stroke-width="1.5"/>
      <!-- Steaming mug -->
      <rect x="180" y="130" width="16" height="18" rx="3" fill="#EEF2FF"/>
      <path d="M 188 126 Q 192 118 186 112" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.7"/>
      <!-- Avatar Alex badge -->
      <rect x="440" y="135" width="110" height="24" rx="6" fill="#1E293B" stroke="#818CF8" stroke-width="1"/>
      <text x="495" y="151" fill="#A5B4FC" font-size="10" font-weight="700" text-anchor="middle">Alex Chen • Active</text>
    </svg>
    """

def get_knowledge_base_illustration(width: str = "100%", height: int = 180) -> str:
    """Futuristic neural corporate library illustration for Knowledge Base."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(79,70,229,0.15);">
      <defs>
        <linearGradient id="kbBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#0F172A"/>
          <stop offset="50%" stop-color="#1E293B"/>
          <stop offset="100%" stop-color="#312E81"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#kbBg)" rx="14"/>
      <!-- Holographic Archive Shelves (Isometric angle) -->
      <g opacity="0.85">
        <rect x="50" y="40" width="70" height="120" rx="4" fill="#1E293B" stroke="#38BDF8" stroke-width="1.5"/>
        <line x1="50" y1="75" x2="120" y2="75" stroke="#38BDF8" stroke-width="1.5"/>
        <line x1="50" y1="115" x2="120" y2="115" stroke="#38BDF8" stroke-width="1.5"/>
        <rect x="58" y="48" width="10" height="22" rx="2" fill="#EC4899"/>
        <rect x="72" y="48" width="10" height="22" rx="2" fill="#3B82F6"/>
        <rect x="86" y="48" width="10" height="22" rx="2" fill="#10B981"/>
        <rect x="58" y="85" width="10" height="24" rx="2" fill="#F59E0B"/>
        <rect x="72" y="85" width="10" height="24" rx="2" fill="#8B5CF6"/>
      </g>
      <!-- Central Glowing Holographic Document Core -->
      <g transform="translate(240, 25)">
        <rect x="0" y="0" width="120" height="150" rx="8" fill="#1E1B4B" stroke="#6366F1" stroke-width="3"/>
        <rect x="15" y="20" width="90" height="10" rx="3" fill="#818CF8"/>
        <line x1="15" y1="45" x2="105" y2="45" stroke="#A5B4FC" stroke-width="3"/>
        <line x1="15" y1="60" x2="95" y2="60" stroke="#A5B4FC" stroke-width="3"/>
        <line x1="15" y1="75" x2="100" y2="75" stroke="#A5B4FC" stroke-width="3"/>
        <line x1="15" y1="90" x2="80" y2="90" stroke="#A5B4FC" stroke-width="3"/>
        <!-- Verified RAG Badge Icon -->
        <circle cx="60" cy="120" r="16" fill="#10B981"/>
        <polyline points="53,120 58,125 68,115" stroke="#FFFFFF" stroke-width="3" fill="none"/>
      </g>
      <!-- Neural Search Vectors & Data Particles -->
      <path d="M 120 100 Q 180 60 240 80" stroke="#38BDF8" stroke-width="2" stroke-dasharray="4,4" fill="none"/>
      <path d="M 360 80 Q 420 110 480 70" stroke="#34D399" stroke-width="2" stroke-dasharray="4,4" fill="none"/>
      <!-- Right Side Search Hologram -->
      <rect x="420" y="40" width="140" height="110" rx="8" fill="#1E293B" stroke="#34D399" stroke-width="2"/>
      <text x="490" y="65" fill="#34D399" font-size="11" font-weight="800" text-anchor="middle">SEMANTIC RAG</text>
      <text x="490" y="85" fill="#E2E8F0" font-size="9" text-anchor="middle">Cosine Vector Search</text>
      <text x="490" y="105" fill="#94A3B8" font-size="9" text-anchor="middle">Chunk Re-ranking: ON</text>
      <text x="490" y="125" fill="#38BDF8" font-size="9" font-weight="700" text-anchor="middle">Confidence: 96.8%</text>
    </svg>
    """

def get_ticket_management_illustration(width: str = "100%", height: int = 180) -> str:
    """Futuristic ticket dispatch triage center illustration."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(79,70,229,0.15);">
      <defs>
        <linearGradient id="tmBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1E1B4B"/>
          <stop offset="100%" stop-color="#312E81"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#tmBg)" rx="14"/>
      <!-- 3 Kanban Columns Preview in Perspective -->
      <g transform="translate(40, 30)">
        <rect x="0" y="0" width="150" height="140" rx="8" fill="#0F172A" stroke="#3B82F6" stroke-width="2"/>
        <text x="75" y="22" fill="#60A5FA" font-size="11" font-weight="800" text-anchor="middle">📥 OPEN (4)</text>
        <rect x="12" y="35" width="126" height="40" rx="4" fill="#1E293B"/>
        <text x="20" y="52" fill="#E2E8F0" font-size="9" font-weight="700">TKT-IT-001</text>
        <rect x="12" y="85" width="126" height="40" rx="4" fill="#1E293B"/>
        <text x="20" y="102" fill="#E2E8F0" font-size="9" font-weight="700">TKT-HR-002</text>
      </g>
      <g transform="translate(225, 30)">
        <rect x="0" y="0" width="150" height="140" rx="8" fill="#0F172A" stroke="#F59E0B" stroke-width="2"/>
        <text x="75" y="22" fill="#FBBF24" font-size="11" font-weight="800" text-anchor="middle">⚙️ IN PROGRESS (2)</text>
        <rect x="12" y="35" width="126" height="40" rx="4" fill="#1E293B"/>
        <text x="20" y="52" fill="#FDE68A" font-size="9" font-weight="700">TKT-IT-VPN-04</text>
      </g>
      <g transform="translate(410, 30)">
        <rect x="0" y="0" width="150" height="140" rx="8" fill="#0F172A" stroke="#10B981" stroke-width="2"/>
        <text x="75" y="22" fill="#34D399" font-size="11" font-weight="800" text-anchor="middle">✅ RESOLVED (18)</text>
        <rect x="12" y="35" width="126" height="40" rx="4" fill="#1E293B"/>
        <text x="20" y="52" fill="#A7F3D0" font-size="9" font-weight="700">TKT-ADMIN-001</text>
      </g>
    </svg>
    """

def get_digital_twin_illustration(width: str = "100%", height: int = 180) -> str:
    """Futuristic holographic globe & telemetry radar for Enterprise Digital Twin."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(6,182,212,0.15);">
      <defs>
        <linearGradient id="dtBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#022C22"/>
          <stop offset="50%" stop-color="#064E3B"/>
          <stop offset="100%" stop-color="#047857"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#dtBg)" rx="14"/>
      <!-- Glowing Isometric Grid Floor -->
      <g stroke="#34D399" stroke-width="1" opacity="0.3">
        <line x1="50" y1="180" x2="300" y2="80"/><line x1="150" y1="180" x2="400" y2="80"/><line x1="250" y1="180" x2="500" y2="80"/>
        <line x1="100" y1="110" x2="500" y2="110"/><line x1="70" y1="140" x2="530" y2="140"/>
      </g>
      <!-- Central Holographic Wireframe Globe -->
      <circle cx="300" cy="100" r="60" stroke="#38BDF8" stroke-width="2" fill="none" opacity="0.8"/>
      <ellipse cx="300" cy="100" rx="60" ry="24" stroke="#34D399" stroke-width="1.5" fill="none"/>
      <ellipse cx="300" cy="100" rx="24" ry="60" stroke="#34D399" stroke-width="1.5" fill="none"/>
      <circle cx="300" cy="100" r="12" fill="#10B981" opacity="0.9"/>
      <!-- Orbiting Department Hubs -->
      <circle cx="210" cy="70" r="14" fill="#EC4899"/>
      <text x="210" y="74" fill="#FFFFFF" font-size="8" font-weight="800" text-anchor="middle">HR</text>
      <circle cx="390" cy="70" r="14" fill="#3B82F6"/>
      <text x="390" y="74" fill="#FFFFFF" font-size="8" font-weight="800" text-anchor="middle">IT</text>
      <circle cx="300" cy="165" r="14" fill="#F59E0B"/>
      <text x="300" y="169" fill="#FFFFFF" font-size="8" font-weight="800" text-anchor="middle">ADM</text>
      <!-- Header Overlay Banner -->
      <rect x="40" y="25" width="170" height="40" rx="8" fill="#0F172A" stroke="#34D399" stroke-width="1.5"/>
      <text x="125" y="42" fill="#34D399" font-size="11" font-weight="800" text-anchor="middle">REAL-TIME TWIN</text>
      <text x="125" y="56" fill="#A7F3D0" font-size="9" text-anchor="middle">Live Queuing &amp; Telemetry</text>
    </svg>
    """

def get_what_if_illustration(width: str = "100%", height: int = 180) -> str:
    """Quantum scenario simulation lab illustration for What-If Simulator."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(2,132,199,0.15);">
      <defs>
        <linearGradient id="wiBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#082F49"/>
          <stop offset="50%" stop-color="#0369A1"/>
          <stop offset="100%" stop-color="#0284C7"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#wiBg)" rx="14"/>
      <!-- Shock Wave Curves Comparison -->
      <path d="M 60 140 Q 150 140 250 135 T 450 130 T 540 130" stroke="#94A3B8" stroke-width="3" fill="none"/>
      <path d="M 60 140 Q 150 140 230 70 Q 300 20 370 70 Q 450 130 540 120" stroke="#EF4444" stroke-width="3.5" fill="none"/>
      <!-- Shock Alert Pin -->
      <circle cx="300" cy="45" r="16" fill="#DC2626" stroke="#FFFFFF" stroke-width="2"/>
      <text x="300" y="50" fill="#FFFFFF" font-size="12" font-weight="800" text-anchor="middle">!</text>
      <text x="300" y="80" fill="#FEE2E2" font-size="10" font-weight="800" text-anchor="middle">+371% QUEUE SPIKE</text>
      <!-- Simulation Controls Floating HUD -->
      <rect x="40" y="25" width="160" height="50" rx="8" fill="#0F172A" stroke="#38BDF8" stroke-width="1.5"/>
      <text x="120" y="44" fill="#38BDF8" font-size="11" font-weight="800" text-anchor="middle">SimPy Engine</text>
      <text x="120" y="60" fill="#BAE6FD" font-size="9" text-anchor="middle">M/M/c Discrete Simulation</text>
    </svg>
    """

def get_impact_intelligence_illustration(width: str = "100%", height: int = 180) -> str:
    """Human-centered employee experience & friction radar illustration."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(16,185,129,0.15);">
      <defs>
        <linearGradient id="iiBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#064E3B"/>
          <stop offset="100%" stop-color="#059669"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#iiBg)" rx="14"/>
      <!-- Heart Pulse / Workplace Health Waveform -->
      <path d="M 50 100 L 180 100 L 200 60 L 220 140 L 240 80 L 255 110 L 270 100 L 550 100" stroke="#34D399" stroke-width="3.5" fill="none"/>
      <!-- Glowing Friction Shield (Zero Surveillance) -->
      <circle cx="480" cy="100" r="35" fill="#047857" stroke="#A7F3D0" stroke-width="2.5"/>
      <text x="480" y="96" fill="#A7F3D0" font-size="18" text-anchor="middle">🛡️</text>
      <text x="480" y="122" fill="#ECFDF5" font-size="9" font-weight="700" text-anchor="middle">PRIVACY SAFE</text>
      <!-- Title Badge -->
      <rect x="40" y="25" width="200" height="40" rx="8" fill="#065F46" stroke="#34D399" stroke-width="1.5"/>
      <text x="140" y="42" fill="#FFFFFF" font-size="11" font-weight="800" text-anchor="middle">EMPLOYEE EXPERIENCE</text>
      <text x="140" y="56" fill="#A7F3D0" font-size="9" text-anchor="middle">Aggregated Friction Analytics</text>
    </svg>
    """

def get_predictive_illustration(width: str = "100%", height: int = 180) -> str:
    """AI forecasting & harmonic time-series curve illustration."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(99,102,241,0.15);">
      <defs>
        <linearGradient id="prBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1E1B4B"/>
          <stop offset="50%" stop-color="#312E81"/>
          <stop offset="100%" stop-color="#4F46E5"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#prBg)" rx="14"/>
      <!-- Confidence Interval Ribbon -->
      <path d="M 60 130 Q 180 80 300 110 T 540 60 L 540 100 Q 420 140 300 130 T 60 150 Z" fill="#6366F1" opacity="0.35"/>
      <!-- Main Trend Line with Markers -->
      <polyline points="60,140 120,130 180,95 240,115 300,120 360,90 420,105 480,75 540,80" fill="none" stroke="#38BDF8" stroke-width="3.5"/>
      <circle cx="480" cy="75" r="5" fill="#F59E0B" stroke="#FFFFFF" stroke-width="2"/>
      <!-- Forecast Horizon HUD -->
      <rect x="40" y="25" width="180" height="40" rx="8" fill="#1E1B4B" stroke="#38BDF8" stroke-width="1.5"/>
      <text x="130" y="42" fill="#38BDF8" font-size="11" font-weight="800" text-anchor="middle">14-DAY INFLOW FORECAST</text>
      <text x="130" y="56" fill="#93C5FD" font-size="9" text-anchor="middle">Seasonal Decomposition</text>
    </svg>
    """

def get_knowledge_graph_illustration(width: str = "100%", height: int = 180) -> str:
    """Ontological connected neural node network illustration."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(79,70,229,0.15);">
      <defs>
        <linearGradient id="kgBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#0F172A"/>
          <stop offset="100%" stop-color="#1E1B4B"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#kgBg)" rx="14"/>
      <!-- Connected Node Graph -->
      <line x1="120" y1="100" x2="240" y2="60" stroke="#6366F1" stroke-width="2"/>
      <line x1="120" y1="100" x2="240" y2="140" stroke="#6366F1" stroke-width="2"/>
      <line x1="240" y1="60" x2="360" y2="100" stroke="#6366F1" stroke-width="2"/>
      <line x1="240" y1="140" x2="360" y2="100" stroke="#6366F1" stroke-width="2"/>
      <line x1="360" y1="100" x2="480" y2="60" stroke="#6366F1" stroke-width="2"/>
      <line x1="360" y1="100" x2="480" y2="140" stroke="#6366F1" stroke-width="2"/>
      <!-- Nodes -->
      <circle cx="120" cy="100" r="18" fill="#EC4899"/><text x="120" y="104" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">HR</text>
      <circle cx="240" cy="60" r="14" fill="#8B5CF6"/><text x="240" y="64" fill="#FFFFFF" font-size="8" font-weight="700" text-anchor="middle">Policy</text>
      <circle cx="240" cy="140" r="14" fill="#F59E0B"/><text x="240" y="144" fill="#FFFFFF" font-size="8" font-weight="700" text-anchor="middle">Ticket</text>
      <circle cx="360" cy="100" r="22" fill="#3B82F6"/><text x="360" y="104" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">Core</text>
      <circle cx="480" cy="60" r="14" fill="#10B981"/><text x="480" y="64" fill="#FFFFFF" font-size="8" font-weight="700" text-anchor="middle">Tool</text>
      <circle cx="480" cy="140" r="14" fill="#38BDF8"/><text x="480" y="144" fill="#FFFFFF" font-size="8" font-weight="700" text-anchor="middle">Room</text>
    </svg>
    """

def get_model_eval_illustration(width: str = "100%", height: int = 180) -> str:
    """CSE472 Deep Learning neural network matrix & loss lab illustration."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(79,70,229,0.15);">
      <defs>
        <linearGradient id="meBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1E1B4B"/>
          <stop offset="50%" stop-color="#2E1065"/>
          <stop offset="100%" stop-color="#4C1D95"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#meBg)" rx="14"/>
      <!-- Neural Network Layers Visualization -->
      <g transform="translate(60, 40)">
        <!-- Input Layer -->
        <circle cx="20" cy="30" r="7" fill="#38BDF8"/><circle cx="20" cy="60" r="7" fill="#38BDF8"/><circle cx="20" cy="90" r="7" fill="#38BDF8"/>
        <!-- Bi-LSTM Hidden Layer 1 -->
        <circle cx="80" cy="20" r="7" fill="#818CF8"/><circle cx="80" cy="50" r="7" fill="#818CF8"/><circle cx="80" cy="80" r="7" fill="#818CF8"/><circle cx="80" cy="110" r="7" fill="#818CF8"/>
        <!-- Output Layer -->
        <circle cx="140" cy="40" r="8" fill="#34D399"/><circle cx="140" cy="75" r="8" fill="#EC4899"/><circle cx="140" cy="110" r="8" fill="#F59E0B"/>
        <!-- Connections -->
        <line x1="27" y1="30" x2="73" y2="20" stroke="#818CF8" stroke-width="1.2" opacity="0.5"/>
        <line x1="27" y1="60" x2="73" y2="50" stroke="#818CF8" stroke-width="1.2" opacity="0.5"/>
        <line x1="27" y1="90" x2="73" y2="80" stroke="#818CF8" stroke-width="1.2" opacity="0.5"/>
        <line x1="87" y1="50" x2="132" y2="40" stroke="#818CF8" stroke-width="1.2" opacity="0.5"/>
        <line x1="87" y1="80" x2="132" y2="75" stroke="#818CF8" stroke-width="1.2" opacity="0.5"/>
      </g>
      <!-- Confusion Matrix Badge -->
      <rect x="260" y="35" width="140" height="130" rx="6" fill="#0F172A" stroke="#8B5CF6" stroke-width="2"/>
      <text x="330" y="55" fill="#DDD6FE" font-size="10" font-weight="800" text-anchor="middle">CONFUSION MATRIX</text>
      <!-- Matrix Cells -->
      <rect x="275" y="65" width="30" height="25" fill="#059669"/><text x="290" y="82" fill="#FFFFFF" font-size="10" font-weight="700" text-anchor="middle">19</text>
      <rect x="315" y="65" width="30" height="25" fill="#1E293B"/><text x="330" y="82" fill="#94A3B8" font-size="10" font-weight="700" text-anchor="middle">1</text>
      <rect x="355" y="65" width="30" height="25" fill="#1E293B"/><text x="370" y="82" fill="#94A3B8" font-size="10" font-weight="700" text-anchor="middle">0</text>
      <rect x="275" y="95" width="30" height="25" fill="#1E293B"/><text x="290" y="112" fill="#94A3B8" font-size="10" font-weight="700" text-anchor="middle">1</text>
      <rect x="315" y="95" width="30" height="25" fill="#059669"/><text x="330" y="112" fill="#FFFFFF" font-size="10" font-weight="700" text-anchor="middle">18</text>
      <rect x="355" y="95" width="30" height="25" fill="#1E293B"/><text x="370" y="112" fill="#94A3B8" font-size="10" font-weight="700" text-anchor="middle">0</text>
      <rect x="275" y="125" width="30" height="25" fill="#1E293B"/><text x="290" y="142" fill="#94A3B8" font-size="10" font-weight="700" text-anchor="middle">1</text>
      <rect x="315" y="125" width="30" height="25" fill="#1E293B"/><text x="330" y="142" fill="#94A3B8" font-size="10" font-weight="700" text-anchor="middle">1</text>
      <rect x="355" y="125" width="30" height="25" fill="#059669"/><text x="370" y="142" fill="#FFFFFF" font-size="10" font-weight="700" text-anchor="middle">10</text>
      <!-- Accuracy Pill -->
      <rect x="430" y="55" width="140" height="90" rx="8" fill="#1E1B4B" stroke="#10B981" stroke-width="2"/>
      <text x="500" y="85" fill="#A7F3D0" font-size="10" font-weight="700" text-anchor="middle">BI-LSTM ACCURACY</text>
      <text x="500" y="120" fill="#34D399" font-size="28" font-weight="800" text-anchor="middle">92.2%</text>
    </svg>
    """

def get_admin_centre_illustration(width: str = "100%", height: int = 180) -> str:
    """Mission control superuser security console illustration for Admin Control Centre."""
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 200" width="{width}" height="{height}" style="border-radius: 14px; box-shadow: 0 4px 14px rgba(17,24,39,0.2);">
      <defs>
        <linearGradient id="acBg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#111827"/>
          <stop offset="50%" stop-color="#1F2937"/>
          <stop offset="100%" stop-color="#374151"/>
        </linearGradient>
      </defs>
      <rect width="600" height="200" fill="url(#acBg)" rx="14"/>
      <!-- Security Shield with Keyhole -->
      <polygon points="120,40 160,55 160,110 120,145 80,110 80,55" fill="#DC2626" stroke="#F87171" stroke-width="2"/>
      <circle cx="120" cy="85" r="8" fill="#FFFFFF"/>
      <rect x="117" y="85" width="6" height="18" fill="#FFFFFF"/>
      <text x="120" y="165" fill="#FCA5A5" font-size="10" font-weight="800" text-anchor="middle">SUPERUSER ACCESS</text>
      <!-- Human-in-the-Loop Triage Console -->
      <rect x="220" y="35" width="340" height="130" rx="8" fill="#0F172A" stroke="#4B5563" stroke-width="2"/>
      <text x="390" y="60" fill="#F3F4F6" font-size="12" font-weight="800" text-anchor="middle">HUMAN-IN-THE-LOOP TRIAGE QUEUE</text>
      <rect x="240" y="75" width="300" height="35" rx="4" fill="#1F2937"/>
      <circle cx="260" cy="92" r="6" fill="#F59E0B"/><text x="275" y="96" fill="#F3F4F6" font-size="9">Auto-Ticket TKT-HR-002: Pending Review</text>
      <rect x="240" y="120" width="300" height="35" rx="4" fill="#1F2937"/>
      <circle cx="260" cy="137" r="6" fill="#10B981"/><text x="275" y="141" fill="#F3F4F6" font-size="9">Policy Conflict #1: WFH Cap Mismatch</text>
    </svg>
    """

def get_room_thumbnail(room_name: str) -> str:
    """Generates an embedded visual card thumbnail for specific conference rooms."""
    if "Synergy" in room_name:
        return """
        <svg viewBox="0 0 200 90" width="100%" height="80" style="border-radius: 8px;">
          <rect width="200" height="90" fill="#EDE9FE" rx="8"/>
          <ellipse cx="100" cy="50" rx="60" ry="20" fill="#C4B5FD" stroke="#7C3AED" stroke-width="2"/>
          <rect x="70" y="12" width="60" height="15" rx="2" fill="#1E1B4B"/>
          <text x="100" y="23" fill="#A78BFA" font-size="7" font-weight="800" text-anchor="middle">DUAL 4K ZOOM</text>
        </svg>
        """
    elif "Innovate" in room_name:
        return """
        <svg viewBox="0 0 200 90" width="100%" height="80" style="border-radius: 8px;">
          <rect width="200" height="90" fill="#E0E7FF" rx="8"/>
          <rect x="50" y="35" width="100" height="35" rx="4" fill="#C7D2FE" stroke="#4F46E5" stroke-width="2"/>
          <rect x="60" y="10" width="80" height="16" rx="2" fill="#FFFFFF" stroke="#818CF8" stroke-width="1.5"/>
          <text x="100" y="21" fill="#4338CA" font-size="7" font-weight="800" text-anchor="middle">SMART WHITEBOARD</text>
        </svg>
        """
    elif "Focus" in room_name:
        return """
        <svg viewBox="0 0 200 90" width="100%" height="80" style="border-radius: 8px;">
          <rect width="200" height="90" fill="#FCE7F3" rx="8"/>
          <circle cx="80" cy="50" r="16" fill="#FBCFE8" stroke="#DB2777" stroke-width="2"/>
          <circle cx="120" cy="50" r="16" fill="#FBCFE8" stroke="#DB2777" stroke-width="2"/>
          <text x="100" y="22" fill="#BE185D" font-size="7" font-weight="800" text-anchor="middle">ACOUSTIC POD</text>
        </svg>
        """
    else:
        return """
        <svg viewBox="0 0 200 90" width="100%" height="80" style="border-radius: 8px;">
          <rect width="200" height="90" fill="#FEF3C7" rx="8"/>
          <rect x="50" y="35" width="100" height="35" rx="4" fill="#FDE68A" stroke="#D97706" stroke-width="2"/>
          <text x="100" y="22" fill="#92400E" font-size="7" font-weight="800" text-anchor="middle">CREATIVE DEN</text>
        </svg>
        """
