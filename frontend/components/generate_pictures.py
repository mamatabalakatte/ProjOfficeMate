"""
Image Generation Pipeline for OfficeMate 2.0
Generates high-resolution PNG illustrations for all workplace hubs and pages.
Ensures real, crisp pictures are rendered via st.image() with zero chance of code-block rendering.
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")
os.makedirs(ASSETS_DIR, exist_ok=True)

def try_load_font(size: int):
    # Try system fonts or default
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFCompact.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

font_title = try_load_font(28)
font_subtitle = try_load_font(18)
font_badge = try_load_font(14)
font_small = try_load_font(12)

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def generate_virtual_office_hq_image():
    """Generates the Virtual Office 3D Isometric Headquarters visual floorplan (1000x520)."""
    w, h = 1000, 520
    img = Image.new("RGB", (w, h), color=(241, 245, 249))
    draw = ImageDraw.Draw(img)

    # Floor boundary
    draw_rounded_rect(draw, [15, 15, w-15, h-15], 24, fill=(248, 250, 252), outline=(203, 213, 225), width=3)

    # Header banner
    draw_rounded_rect(draw, [30, 25, w-30, 80], 14, fill=(79, 70, 229), outline=(67, 56, 202), width=2)
    draw.text((50, 38), "OFFICEMATE 2.0 - VIRTUAL WORKPLACE HEADQUARTERS", font=font_title, fill=(255, 255, 255))
    draw.text((780, 44), "LIVE DIGITAL TWIN", font=font_badge, fill=(167, 243, 208))

    # Room 1: Reception & Lobby (Bottom Center)
    rx1, ry1, rx2, ry2 = 360, 320, 640, 490
    draw_rounded_rect(draw, [rx1, ry1, rx2, ry2], 16, fill=(255, 255, 255), outline=(99, 102, 241), width=3)
    draw_rounded_rect(draw, [rx1, ry1, rx2, ry1+36], 12, fill=(99, 102, 241))
    draw.text((rx1+40, ry1+10), "RECEPTION & LOBBY", font=font_badge, fill=(255, 255, 255))
    # Counter
    draw_rounded_rect(draw, [rx1+40, ry1+60, rx2-40, ry1+90], 10, fill=(199, 210, 254), outline=(129, 140, 248), width=2)
    # Receptionist
    draw.ellipse([rx1+120, ry1+105, rx1+160, ry1+145], fill=(252, 211, 77), outline=(245, 158, 11), width=2)
    draw.text((rx1+60, ry2-30), "Welcome Center - Badges", font=font_small, fill=(100, 116, 139))

    # Room 2: HR People Lounge (Top Left)
    hx1, hy1, hx2, hy2 = 35, 95, 340, 290
    draw_rounded_rect(draw, [hx1, hy1, hx2, hy2], 16, fill=(253, 242, 248), outline=(236, 72, 153), width=3)
    draw_rounded_rect(draw, [hx1, hy1, hx2, hy1+36], 12, fill=(236, 72, 153))
    draw.text((hx1+30, hy1+10), "HR PEOPLE LOUNGE", font=font_badge, fill=(255, 255, 255))
    # Armchair & Plant
    draw_rounded_rect(draw, [hx1+30, hy1+60, hx1+100, hy1+120], 12, fill=(244, 114, 182))
    draw_rounded_rect(draw, [hx1+120, hy1+70, hx1+180, hy1+110], 8, fill=(251, 207, 232), outline=(244, 114, 182))
    draw.ellipse([hx1+220, hy1+60, hx1+270, hy1+110], fill=(16, 185, 129))
    draw.text((hx1+30, hy2-35), "Leaves - Wellness - Benefits", font=font_small, fill=(190, 24, 93))

    # Room 3: IT Command Center (Top Center)
    ix1, iy1, ix2, iy2 = 360, 95, 640, 290
    draw_rounded_rect(draw, [ix1, iy1, ix2, iy2], 16, fill=(238, 242, 255), outline=(79, 70, 229), width=3)
    draw_rounded_rect(draw, [ix1, iy1, ix2, iy1+36], 12, fill=(79, 70, 229))
    draw.text((ix1+40, iy1+10), "IT COMMAND CENTER", font=font_badge, fill=(255, 255, 255))
    # Server Racks
    for s_idx in range(3):
        sx = ix1 + 30 + s_idx * 75
        draw_rounded_rect(draw, [sx, iy1+55, sx+60, iy1+135], 6, fill=(30, 27, 75))
        # LED lights
        draw.ellipse([sx+10, iy1+70, sx+16, iy1+76], fill=(52, 211, 153))
        draw.ellipse([sx+25, iy1+70, sx+31, iy1+76], fill=(56, 189, 248))
        draw.ellipse([sx+40, iy1+70, sx+46, iy1+76], fill=(251, 146, 60))
    draw.text((ix1+30, iy2-35), "VPN - Hardware - OCR Diagnostics", font=font_small, fill=(67, 56, 202))

    # Room 4: Admin Desk & Logistics (Top Right)
    ax1, ay1, ax2, ay2 = 660, 95, 965, 290
    draw_rounded_rect(draw, [ax1, ay1, ax2, ay2], 16, fill=(254, 252, 232), outline=(245, 158, 11), width=3)
    draw_rounded_rect(draw, [ax1, ay1, ax2, ay1+36], 12, fill=(245, 158, 11))
    draw.text((ax1+40, ay1+10), "ADMIN & FACILITIES", font=font_badge, fill=(255, 255, 255))
    # Boxes & Desk
    draw_rounded_rect(draw, [ax1+30, ay1+60, ax1+120, ay1+120], 8, fill=(253, 230, 138), outline=(217, 119, 6), width=2)
    draw_rounded_rect(draw, [ax1+140, ay1+60, ax1+250, ay1+110], 8, fill=(254, 243, 199))
    draw.text((ax1+30, ay2-35), "Travel Per Diem - Supply Requisitions", font=font_small, fill=(180, 83, 9))

    # Room 5: Boardroom & Meeting Pods (Bottom Left)
    bx1, by1, bx2, by2 = 35, 320, 340, 490
    draw_rounded_rect(draw, [bx1, by1, bx2, by2], 16, fill=(245, 243, 255), outline=(139, 92, 246), width=3)
    draw_rounded_rect(draw, [bx1, by1, bx2, by1+36], 12, fill=(139, 92, 246))
    draw.text((bx1+30, by1+10), "SYNERGY BOARDROOM", font=font_badge, fill=(255, 255, 255))
    # Boardroom Oval Table
    draw.ellipse([bx1+50, by1+60, bx2-50, by1+130], fill=(221, 214, 254), outline=(124, 58, 237), width=2)
    draw.text((bx1+30, by2-35), "Conference - Conflict-Free Engine", font=font_small, fill=(109, 40, 217))

    # Room 6: Cafeteria & Lounge (Bottom Right)
    cx1, cy1, cx2, cy2 = 660, 320, 965, 490
    draw_rounded_rect(draw, [cx1, cy1, cx2, cy2], 16, fill=(236, 253, 245), outline=(16, 185, 129), width=3)
    draw_rounded_rect(draw, [cx1, cy1, cx2, cy1+36], 12, fill=(16, 185, 129))
    draw.text((cx1+40, cy1+10), "CAFETERIA & SOCIAL", font=font_badge, fill=(255, 255, 255))
    # Coffee Bar & Bistro
    draw_rounded_rect(draw, [cx1+30, cy1+60, cx1+130, cy1+110], 8, fill=(167, 243, 208), outline=(5, 150, 105), width=2)
    draw.ellipse([cx1+170, cy1+65, cx1+230, cy1+125], fill=(209, 250, 229), outline=(16, 185, 129), width=2)
    draw.text((cx1+30, cy2-35), "Espresso Bar - Kudos - Coffee Roulette", font=font_small, fill=(4, 120, 87))

    out_path = os.path.join(ASSETS_DIR, "virtual_office_hq.png")
    img.save(out_path, "PNG")
    print(f"Generated: {out_path}")

def generate_ai_assistant_robot_image():
    """Generates the AI Holo-Bot Assistant Hero Banner (900x280)."""
    w, h = 900, 280
    img = Image.new("RGB", (w, h), color=(30, 27, 75))
    draw = ImageDraw.Draw(img)

    # Background gradient
    for y in range(h):
        r = int(30 + (67 - 30) * (y / h))
        g = int(27 + (56 - 27) * (y / h))
        b = int(75 + (202 - 75) * (y / h))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Glowing decorative neural rings
    draw.ellipse([40, 30, 220, 210], outline=(56, 189, 248), width=3)
    draw.ellipse([55, 45, 205, 195], outline=(99, 102, 241), width=2)

    # Robot Head
    rx, ry = 130, 120
    draw.ellipse([rx-45, ry-45, rx+45, ry+45], fill=(238, 242, 255), outline=(56, 189, 248), width=3)
    # Antenna
    draw.line([(rx, ry-45), (rx, ry-65)], fill=(56, 189, 248), width=4)
    draw.ellipse([rx-8, ry-75, rx+8, ry-59], fill=(56, 189, 248))
    # Glowing Eyes
    draw.ellipse([rx-25, ry-15, rx-8, ry+10], fill=(2, 132, 199))
    draw.ellipse([rx+8, ry-15, rx+25, ry+10], fill=(2, 132, 199))
    draw.ellipse([rx-22, ry-12, rx-15, ry-5], fill=(255, 255, 255))
    draw.ellipse([rx+11, ry-12, rx+18, ry-5], fill=(255, 255, 255))
    # Smile
    draw.arc([rx-16, ry+5, rx+16, ry+22], start=0, end=180, fill=(2, 132, 199), width=3)

    # Speech Bubble / Card
    bx1, by1, bx2, by2 = 250, 35, 860, 245
    draw_rounded_rect(draw, [bx1, by1, bx2, by2], 16, fill=(255, 255, 255), outline=(129, 140, 248), width=2)
    # Triangle pointer
    draw.polygon([(bx1, 105), (bx1-20, 120), (bx1, 135)], fill=(255, 255, 255))

    draw.text((bx1+30, by1+20), "Universal Workplace AI Assistant", font=font_title, fill=(30, 27, 75))
    draw.text((bx1+30, by1+65), "I am your all-in-one organizational AI companion! Ask me ANY question:", font=font_subtitle, fill=(79, 70, 229))

    capabilities = [
        "- HR, IT & Admin official policies with verifiable citations",
        "- Troubleshooting, technical explanations & code generation",
        "- Email drafting, project planning & business writing",
        "- Automated support ticket creation & real-time routing"
    ]
    for c_i, cap in enumerate(capabilities):
        draw.text((bx1+30, by1+105 + c_i * 26), cap, font=font_badge, fill=(51, 65, 85))

    out_path = os.path.join(ASSETS_DIR, "ai_assistant_robot.png")
    img.save(out_path, "PNG")
    print(f"Generated: {out_path}")

def generate_department_hero(filename, title, subtitle, bg_color, accent_color, badge_text):
    """Generates a standard clean hero illustration banner (900x200)."""
    w, h = 900, 200
    img = Image.new("RGB", (w, h), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Rounded outer frame
    draw_rounded_rect(draw, [10, 10, w-10, h-10], 14, fill=bg_color, outline=accent_color, width=3)

    # Left decorative accent pillar
    draw_rounded_rect(draw, [25, 25, 40, h-25], 8, fill=accent_color)

    # Text content
    draw.text((60, 35), title, font=font_title, fill=(15, 23, 42))
    draw.text((60, 75), subtitle, font=font_subtitle, fill=(51, 65, 85))

    # Badge in bottom right
    bw = 360
    draw_rounded_rect(draw, [w-bw-35, h-60, w-35, h-25], 8, fill=accent_color)
    draw.text((w-bw-20, h-53), badge_text, font=font_badge, fill=(255, 255, 255))

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, "PNG")
    print(f"Generated: {out_path}")

def generate_all():
    generate_virtual_office_hq_image()
    generate_ai_assistant_robot_image()

    generate_department_hero(
        "hr_lounge.png",
        "HR People & Culture Lounge",
        "Manage leaves, view medical benefits, review workplace policies, and track approvals.",
        (253, 242, 248), (236, 72, 153), "HR Support - Leave Balance - Healthcare"
    )

    generate_department_hero(
        "it_command.png",
        "IT Command Center & Infrastructure",
        "Live systems telemetry, screenshot OCR diagnostics, hardware and software requisitions.",
        (238, 242, 255), (79, 70, 229), "Zero-Trust VPN - Hardware - Network Status"
    )

    generate_department_hero(
        "admin_desk.png",
        "Admin & Workplace Facilities Desk",
        "Travel expense per diem calculator, stationery requisitions, office access & logistics.",
        (254, 252, 232), (217, 119, 6), "Facilities - Travel Claims - Requisitions"
    )

    generate_department_hero(
        "boardroom.png",
        "Meeting Rooms & Synergy Boardrooms",
        "Smart conference room booking with real-time collision prevention and audio-visual setups.",
        (245, 243, 255), (124, 58, 237), "Zero Conflicts - 4 Rooms - Instant Booking"
    )

    generate_department_hero(
        "cafeteria.png",
        "Cafeteria & Social Lounge",
        "Subsidized artisan menu, office celebration board, peer kudos, and coffee roulette.",
        (236, 253, 245), (16, 185, 129), "Espresso Bar - Peer Kudos - Lunch Menu"
    )

    generate_department_hero(
        "workspace_cockpit.png",
        "Employee Cockpit & Personal Workspace",
        "Persistent daily tasks, ticket progress indicators, personal room reservations, and activity logs.",
        (241, 245, 249), (59, 130, 246), "Task Tracker - Ticket Status - Reservations"
    )

    generate_department_hero(
        "knowledge_base.png",
        "Organizational Knowledge Repository",
        "Cosine similarity semantic search over corporate policies with verified source attribution.",
        (248, 250, 252), (14, 165, 233), "Semantic Search - RAG - Policy Handbooks"
    )

    generate_department_hero(
        "ticket_triage.png",
        "Ticket Triage & Interactive Kanban",
        "Automated lifecycle management: Open, In Progress, and Resolved with 1-click stage transitions.",
        (245, 243, 255), (99, 102, 241), "Agile Kanban - Priority Routing - SLA Tracking"
    )

    generate_department_hero(
        "digital_twin.png",
        "Enterprise Digital Twin & Telemetry",
        "Real-time organizational telemetry, queue load meters, and departmental health scores.",
        (240, 253, 250), (13, 148, 136), "SimPy Queues - Capacity Gauges - Health Score"
    )

    generate_department_hero(
        "what_if_lab.png",
        "What-If Scenario Stress Testing Lab",
        "Discrete-event simulations for ticket spikes, staffing shortages, and system outages.",
        (255, 241, 242), (225, 29, 72), "SimPy Discrete-Event - Shock Simulations"
    )

    generate_department_hero(
        "impact_intelligence.png",
        "Employee Impact & Friction Intelligence",
        "Cross-department friction heatmaps, cascading root causes, and systemic bottleneck analysis.",
        (254, 243, 199), (217, 119, 6), "Friction Heatmaps - Root Cause - Analytics"
    )

    generate_department_hero(
        "predictive_forecast.png",
        "Predictive Analytics & 14-Day Forecast",
        "Statistical moving-average inflow projections with 95% confidence intervals and peak warnings.",
        (240, 253, 244), (22, 163, 74), "14-Day Inflow - Confidence Bands - Surges"
    )

    generate_department_hero(
        "knowledge_graph.png",
        "Enterprise Knowledge & Relationship Graph",
        "Multi-relational graph connecting employees, departments, tickets, and corporate policies.",
        (243, 244, 246), (75, 85, 99), "Entity Network - Relational Traversal"
    )

    generate_department_hero(
        "model_evaluation.png",
        "Deep Learning & NLP Model Evaluation",
        "CSE472 Project 20 benchmark: Bi-LSTM vs TF-IDF on held-out test splits with confusion matrices.",
        (238, 242, 255), (79, 70, 229), "Bi-LSTM 92.16% - TF-IDF 90.20% - True Metrics"
    )

    generate_department_hero(
        "admin_control.png",
        "Admin Control Centre & HITL Governance",
        "Human-in-the-loop triage queue, policy contradiction resolver, and system audit trails.",
        (255, 247, 237), (234, 88, 12), "HITL Governance - Conflict Shield - Audit Log"
    )

if __name__ == "__main__":
    generate_all()
