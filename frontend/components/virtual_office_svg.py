"""
Interactive Cartoon Virtual Office Isometric Map for OfficeMate 2.0
Visual identity of the application: reception, HR, IT, Admin, Meeting Room, Cafeteria, Desks.
Pure SVG vector with cartoon aesthetic, vibrant palettes, and local zero-dependency rendering.
"""

def render_virtual_office_map() -> str:
    """Generates the interactive illustrated virtual office SVG."""
    return """
    <div style="width: 100%; overflow-x: auto; background: #F8FAFC; border: 2px solid #E2E8F0; border-radius: 20px; box-shadow: 0 10px 30px rgba(79, 70, 229, 0.08); padding: 10px;">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="100%" height="auto" style="min-width: 750px; font-family: 'Plus Jakarta Sans', sans-serif;">
      <defs>
        <!-- Gradients -->
        <linearGradient id="floorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#EEF2F6"/>
          <stop offset="100%" stop-color="#E2E8F0"/>
        </linearGradient>
        <linearGradient id="hrWall" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FCE7F3"/>
          <stop offset="100%" stop-color="#FBCFE8"/>
        </linearGradient>
        <linearGradient id="itWall" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#E0E7FF"/>
          <stop offset="100%" stop-color="#C7D2FE"/>
        </linearGradient>
        <linearGradient id="adminWall" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FEF3C7"/>
          <stop offset="100%" stop-color="#FDE68A"/>
        </linearGradient>
        <linearGradient id="cafeWall" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#D1FAE5"/>
          <stop offset="100%" stop-color="#A7F3D0"/>
        </linearGradient>
        <linearGradient id="meetingWall" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#EDE9FE"/>
          <stop offset="100%" stop-color="#DDD6FE"/>
        </linearGradient>
        
        <!-- Filter for soft drop shadows -->
        <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="2" dy="5" stdDeviation="4" flood-color="#4F46E5" flood-opacity="0.12"/>
        </filter>
      </defs>

      <!-- Main Floor Base -->
      <rect x="20" y="20" width="960" height="560" rx="24" fill="url(#floorGrad)" stroke="#CBD5E1" stroke-width="3"/>
      
      <!-- Outer Hallway Walking Tile Paths -->
      <path d="M 500 40 L 500 560" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="6,6"/>
      <path d="M 40 300 L 960 300" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="6,6"/>

      <!-- ================= 1. RECEPTION & LOBBY (Bottom Center) ================= -->
      <g id="zone-reception" transform="translate(360, 340)" filter="url(#cardShadow)">
        <rect x="0" y="0" width="280" height="210" rx="16" fill="#FFFFFF" stroke="#6366F1" stroke-width="2.5"/>
        <rect x="0" y="0" width="280" height="34" rx="16" fill="#6366F1"/>
        <text x="140" y="22" fill="#FFFFFF" font-size="14" font-weight="800" text-anchor="middle">🛎️ RECEPTION &amp; WELCOME LOBBY</text>
        
        <!-- Reception Counter -->
        <path d="M 60 90 Q 140 120 220 90 L 220 115 Q 140 145 60 115 Z" fill="#818CF8"/>
        <!-- Receptionist Avatar -->
        <circle cx="140" cy="70" r="16" fill="#FCD34D"/>
        <path d="M 124 64 C 124 50, 156 50, 156 64 Z" fill="#374151"/>
        <circle cx="135" cy="70" r="2" fill="#1E293B"/>
        <circle cx="145" cy="70" r="2" fill="#1E293B"/>
        <path d="M 137 76 Q 140 79 143 76" stroke="#1E293B" stroke-width="1.5" fill="none"/>
        
        <!-- Welcome Terminal Tablet -->
        <rect x="130" y="94" width="20" height="14" rx="2" fill="#1E293B"/>
        <rect x="132" y="96" width="16" height="10" fill="#38BDF8"/>
        
        <!-- Waiting Lounge Sofa -->
        <rect x="30" y="150" width="80" height="36" rx="8" fill="#C7D2FE" stroke="#818CF8" stroke-width="1.5"/>
        <rect x="25" y="154" width="10" height="28" rx="4" fill="#818CF8"/>
        <rect x="95" y="154" width="10" height="28" rx="4" fill="#818CF8"/>
        
        <!-- Indoor Plant -->
        <circle cx="230" cy="170" r="12" fill="#10B981"/>
        <circle cx="225" cy="162" r="8" fill="#34D399"/>
        <circle cx="238" cy="165" r="9" fill="#059669"/>
        <rect x="224" y="176" width="12" height="16" rx="2" fill="#B45309"/>

        <!-- Speech Bubble Badge -->
        <rect x="65" y="42" width="150" height="20" rx="10" fill="#EEF2FF" stroke="#6366F1" stroke-width="1"/>
        <text x="140" y="56" fill="#4338CA" font-size="10" font-weight="700" text-anchor="middle">✨ Click to Check Announcements</text>
      </g>

      <!-- ================= 2. HR DEPARTMENT (Top Left) ================= -->
      <g id="zone-hr" transform="translate(40, 40)" filter="url(#cardShadow)">
        <rect x="0" y="0" width="280" height="230" rx="16" fill="url(#hrWall)" stroke="#EC4899" stroke-width="2.5"/>
        <rect x="0" y="0" width="280" height="34" rx="16" fill="#EC4899"/>
        <text x="140" y="22" fill="#FFFFFF" font-size="14" font-weight="800" text-anchor="middle">🌸 HR PEOPLE &amp; TALENT OFFICE</text>
        
        <!-- Desk & Chairs -->
        <rect x="50" y="80" width="100" height="50" rx="8" fill="#FBCFE8" stroke="#DB2777" stroke-width="1.5"/>
        <!-- Laptop on desk -->
        <rect x="80" y="90" width="26" height="18" rx="2" fill="#475569"/>
        <rect x="82" y="92" width="22" height="14" fill="#EC4899"/>
        <!-- Sarah Avatar (HR Lead) -->
        <circle cx="100" cy="62" r="14" fill="#FCD34D"/>
        <path d="M 86 56 C 86 44, 114 44, 114 56 Z" fill="#B45309"/>
        <circle cx="95" cy="62" r="1.5" fill="#1E293B"/>
        <circle cx="105" cy="62" r="1.5" fill="#1E293B"/>
        <path d="M 97 66 Q 100 69 103 66" stroke="#1E293B" stroke-width="1.5" fill="none"/>
        <text x="100" y="45" fill="#BE185D" font-size="9" font-weight="800" text-anchor="middle">Sarah (HR Lead)</text>
        
        <!-- Leave Policy Bulletin Board on Wall -->
        <rect x="180" y="60" width="80" height="90" rx="6" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.5"/>
        <text x="220" y="78" fill="#B45309" font-size="10" font-weight="700" text-anchor="middle">📌 Leave Policy</text>
        <line x1="190" y1="90" x2="250" y2="90" stroke="#FCD34D" stroke-width="3"/>
        <line x1="190" y1="102" x2="245" y2="102" stroke="#FCD34D" stroke-width="3"/>
        <line x1="190" y1="114" x2="235" y2="114" stroke="#FCD34D" stroke-width="3"/>
        <rect x="195" y="125" width="50" height="16" rx="4" fill="#EC4899"/>
        <text x="220" y="137" fill="#FFFFFF" font-size="8" font-weight="700" text-anchor="middle">20 Days PTO</text>

        <!-- Status Tag -->
        <rect x="40" y="185" width="200" height="26" rx="8" fill="#FFFFFF" stroke="#F472B6" stroke-width="1"/>
        <text x="140" y="202" fill="#BE185D" font-size="11" font-weight="700" text-anchor="middle">💬 Click to Open HR Services</text>
      </g>

      <!-- ================= 3. IT DEPARTMENT (Top Right) ================= -->
      <g id="zone-it" transform="translate(680, 40)" filter="url(#cardShadow)">
        <rect x="0" y="0" width="280" height="230" rx="16" fill="url(#itWall)" stroke="#4F46E5" stroke-width="2.5"/>
        <rect x="0" y="0" width="280" height="34" rx="16" fill="#4F46E5"/>
        <text x="140" y="22" fill="#FFFFFF" font-size="14" font-weight="800" text-anchor="middle">💻 IT COMMAND CENTER</text>
        
        <!-- Server Rack with Blinking LEDs -->
        <rect x="25" y="60" width="55" height="110" rx="6" fill="#1E293B" stroke="#0F172A" stroke-width="2"/>
        <circle cx="40" cy="75" r="3" fill="#10B981"/>
        <circle cx="55" cy="75" r="3" fill="#10B981"/>
        <line x1="32" y1="90" x2="68" y2="90" stroke="#38BDF8" stroke-width="2"/>
        <circle cx="40" cy="105" r="3" fill="#10B981"/>
        <circle cx="55" cy="105" r="3" fill="#F59E0B"/>
        <line x1="32" y1="120" x2="68" y2="120" stroke="#38BDF8" stroke-width="2"/>
        <circle cx="40" cy="135" r="3" fill="#10B981"/>
        <circle cx="55" cy="135" r="3" fill="#10B981"/>
        <line x1="32" y1="150" x2="68" y2="150" stroke="#38BDF8" stroke-width="2"/>

        <!-- Dual Monitor Workstation -->
        <rect x="100" y="90" width="145" height="48" rx="8" fill="#C7D2FE" stroke="#6366F1" stroke-width="1.5"/>
        <!-- Monitor 1 -->
        <rect x="115" y="65" width="40" height="26" rx="3" fill="#0F172A"/>
        <rect x="117" y="67" width="36" height="22" fill="#0284C7"/>
        <!-- Monitor 2 (Code) -->
        <rect x="160" y="65" width="40" height="26" rx="3" fill="#0F172A"/>
        <rect x="162" y="67" width="36" height="22" fill="#059669"/>
        <!-- David Avatar (IT Lead) -->
        <circle cx="155" cy="120" r="14" fill="#FBBF24"/>
        <path d="M 141 114 C 141 102, 169 102, 169 114 Z" fill="#1E293B"/>
        <circle cx="150" cy="120" r="1.5" fill="#1E293B"/>
        <circle cx="160" cy="120" r="1.5" fill="#1E293B"/>
        <text x="155" y="148" fill="#312E81" font-size="9" font-weight="800" text-anchor="middle">David (IT Lead)</text>

        <!-- Status Tag -->
        <rect x="40" y="185" width="200" height="26" rx="8" fill="#FFFFFF" stroke="#818CF8" stroke-width="1"/>
        <text x="140" y="202" fill="#4338CA" font-size="11" font-weight="700" text-anchor="middle">⚡ Click for VPN &amp; Tech Help</text>
      </g>

      <!-- ================= 4. ADMINISTRATION & FACILITIES (Bottom Left) ================= -->
      <g id="zone-admin" transform="translate(40, 310)" filter="url(#cardShadow)">
        <rect x="0" y="0" width="280" height="240" rx="16" fill="url(#adminWall)" stroke="#D97706" stroke-width="2.5"/>
        <rect x="0" y="0" width="280" height="34" rx="16" fill="#D97706"/>
        <text x="140" y="22" fill="#FFFFFF" font-size="14" font-weight="800" text-anchor="middle">🏢 ADMINISTRATION &amp; FACILITIES</text>

        <!-- Logistics Packages & Storage -->
        <rect x="30" y="60" width="45" height="40" rx="4" fill="#D97706" stroke="#92400E" stroke-width="1.5"/>
        <line x1="30" y1="80" x2="75" y2="80" stroke="#FDE68A" stroke-width="2"/>
        <rect x="40" y="105" width="35" height="30" rx="4" fill="#B45309" stroke="#78350F" stroke-width="1.5"/>
        
        <!-- Filing Cabinets -->
        <rect x="90" y="60" width="50" height="75" rx="4" fill="#E2E8F0" stroke="#94A3B8" stroke-width="2"/>
        <line x1="95" y1="85" x2="135" y2="85" stroke="#64748B" stroke-width="2"/>
        <line x1="95" y1="110" x2="135" y2="110" stroke="#64748B" stroke-width="2"/>

        <!-- Marcus Avatar (Admin Lead) -->
        <circle cx="195" cy="75" r="14" fill="#F59E0B"/>
        <path d="M 181 69 C 181 57, 209 57, 209 69 Z" fill="#4B5563"/>
        <circle cx="190" cy="75" r="1.5" fill="#1E293B"/>
        <circle cx="200" cy="75" r="1.5" fill="#1E293B"/>
        <text x="195" y="102" fill="#92400E" font-size="9" font-weight="800" text-anchor="middle">Marcus (Admin)</text>

        <!-- Ergonomic Chair Sample -->
        <circle cx="200" cy="130" r="12" fill="#475569"/>
        <line x1="200" y1="142" x2="200" y2="160" stroke="#1E293B" stroke-width="3"/>
        <line x1="188" y1="160" x2="212" y2="160" stroke="#1E293B" stroke-width="3"/>

        <!-- Status Tag -->
        <rect x="40" y="195" width="200" height="26" rx="8" fill="#FFFFFF" stroke="#FBBF24" stroke-width="1"/>
        <text x="140" y="212" fill="#B45309" font-size="11" font-weight="700" text-anchor="middle">📋 Click for Expenses &amp; Passes</text>
      </g>

      <!-- ================= 5. MEETING ROOM (Top Center) ================= -->
      <g id="zone-meeting" transform="translate(360, 40)" filter="url(#cardShadow)">
        <rect x="0" y="0" width="280" height="230" rx="16" fill="url(#meetingWall)" stroke="#8B5CF6" stroke-width="2.5"/>
        <rect x="0" y="0" width="280" height="34" rx="16" fill="#8B5CF6"/>
        <text x="140" y="22" fill="#FFFFFF" font-size="14" font-weight="800" text-anchor="middle">📅 SYNERGY BOARDROOM</text>
        
        <!-- Large Conference Oval Table -->
        <ellipse cx="140" cy="120" rx="90" ry="40" fill="#C4B5FD" stroke="#7C3AED" stroke-width="2"/>
        
        <!-- 6 Chairs around table -->
        <circle cx="80" cy="90" r="9" fill="#7C3AED"/>
        <circle cx="140" cy="70" r="9" fill="#7C3AED"/>
        <circle cx="200" cy="90" r="9" fill="#7C3AED"/>
        <circle cx="80" cy="150" r="9" fill="#7C3AED"/>
        <circle cx="140" cy="170" r="9" fill="#7C3AED"/>
        <circle cx="200" cy="150" r="9" fill="#7C3AED"/>

        <!-- Presentation 4K Screen on Wall -->
        <rect x="95" y="42" width="90" height="20" rx="3" fill="#1E1B4B" stroke="#4C1D95" stroke-width="1.5"/>
        <text x="140" y="56" fill="#A78BFA" font-size="8" font-weight="800" text-anchor="middle">ZOOM ROOMS ACTIVE</text>

        <!-- Status Tag -->
        <rect x="40" y="185" width="200" height="26" rx="8" fill="#FFFFFF" stroke="#A78BFA" stroke-width="1"/>
        <text x="140" y="202" fill="#6D28D9" font-size="11" font-weight="700" text-anchor="middle">🎯 Click to Book a Meeting Room</text>
      </g>

      <!-- ================= 6. CAFETERIA & RELAXATION (Bottom Right) ================= -->
      <g id="zone-cafe" transform="translate(680, 310)" filter="url(#cardShadow)">
        <rect x="0" y="0" width="280" height="240" rx="16" fill="url(#cafeWall)" stroke="#10B981" stroke-width="2.5"/>
        <rect x="0" y="0" width="280" height="34" rx="16" fill="#10B981"/>
        <text x="140" y="22" fill="#FFFFFF" font-size="14" font-weight="800" text-anchor="middle">☕ CAFETERIA &amp; SOCIAL LOUNGE</text>

        <!-- Artisan Espresso Machine Counter -->
        <rect x="35" y="60" width="120" height="45" rx="6" fill="#A7F3D0" stroke="#059669" stroke-width="1.5"/>
        <rect x="45" y="66" width="30" height="26" rx="3" fill="#047857"/>
        <circle cx="53" cy="76" r="3" fill="#FBBF24"/>
        <text x="95" y="82" fill="#065F46" font-size="10" font-weight="800">ESPRESSO</text>

        <!-- Round Bistro Cafe Table -->
        <circle cx="210" cy="115" r="28" fill="#ECFDF5" stroke="#10B981" stroke-width="2"/>
        <circle cx="170" cy="115" r="9" fill="#059669"/>
        <circle cx="250" cy="115" r="9" fill="#059669"/>
        <!-- Cupcake / Coffee cup on table -->
        <circle cx="210" cy="115" r="5" fill="#F59E0B"/>

        <!-- Water Cooler / Dispenser -->
        <rect x="40" y="125" width="22" height="40" rx="3" fill="#E2E8F0" stroke="#64748B" stroke-width="1.5"/>
        <circle cx="51" cy="120" r="10" fill="#38BDF8" opacity="0.8"/>

        <!-- Status Tag -->
        <rect x="40" y="195" width="200" height="26" rx="8" fill="#FFFFFF" stroke="#34D399" stroke-width="1"/>
        <text x="140" y="212" fill="#047857" font-size="11" font-weight="700" text-anchor="middle">🎉 Office Events &amp; Social</text>
      </g>
    </svg>
    </div>
    """
