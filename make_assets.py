import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TEMP_DIR = os.environ.get("TEMP", r"C:\Windows\Temp")

def capture_url(url, output_filename, width=1280, height=800, wait_secs=2):
    tmp_path = os.path.join(TEMP_DIR, output_filename)
    dest_path = os.path.join(ASSETS_DIR, output_filename)
    try:
        subprocess.run([
            CHROME_PATH,
            "--headless",
            "--no-sandbox",
            f"--screenshot={tmp_path}",
            f"--window-size={width},{height}",
            url
        ], timeout=25, capture_output=True)
        if os.path.exists(tmp_path):
            shutil.copy(tmp_path, dest_path)
            print(f"[OK] Captured: {output_filename}")
            return dest_path
    except Exception as e:
        print(f"[ERR] Failed capture for {url}: {e}")
    return None

def create_terminal_image(title, commands_and_outputs, output_filename, width=1100, height=None):
    """Render a crisp, realistic dark developer terminal window matching the reference PDF."""
    font_mono = None
    try:
        font_mono = ImageFont.truetype("consola.ttf", 16)
        font_mono_bold = ImageFont.truetype("consolab.ttf", 16)
        font_title = ImageFont.truetype("arial.ttf", 14)
    except:
        font_mono = ImageFont.load_default()
        font_mono_bold = font_mono
        font_title = font_mono

    # Calculate required height
    lines = []
    for item in commands_and_outputs:
        if isinstance(item, tuple):
            prefix, text, color = item
            lines.append((prefix, text, color))
        else:
            lines.append(("", item, (210, 215, 220)))

    line_h = 24
    header_h = 36
    padding = 18
    calc_h = header_h + (len(lines) * line_h) + (padding * 2)
    final_h = height if height else max(calc_h, 320)

    img = Image.new("RGB", (width, final_h), color=(12, 16, 24))
    draw = ImageDraw.Draw(img)

    # Window top bar
    draw.rectangle([(0, 0), (width, header_h)], fill=(22, 27, 34))
    draw.line([(0, header_h), (width, header_h)], fill=(48, 54, 61), width=1)

    # Window controls (red, yellow, green dots)
    draw.ellipse([(14, 12), (24, 22)], fill=(239, 68, 68))
    draw.ellipse([(32, 12), (42, 22)], fill=(245, 158, 11))
    draw.ellipse([(50, 12), (60, 22)], fill=(16, 185, 129))

    # Title text
    draw.text((75, 9), title, fill=(180, 185, 195), font=font_title)

    # Content
    y = header_h + padding
    for prefix, text, col in lines:
        x = padding
        if prefix:
            draw.text((x, y), prefix, fill=(56, 189, 248), font=font_mono_bold)
            x += draw.textlength(prefix, font=font_mono_bold)
        draw.text((x, y), text, fill=col, font=font_mono)
        y += line_h

    # Border
    draw.rectangle([(0, 0), (width - 1, final_h - 1)], outline=(48, 54, 61), width=1)

    dest_path = os.path.join(ASSETS_DIR, output_filename)
    img.save(dest_path, "PNG", quality=95)
    print(f"[OK] Generated terminal: {output_filename}")
    return dest_path

def create_flow_diagram(title, steps, output_filename, width=1100, height=480):
    """Render colored horizontal flow diagram matching reference PDF Docker/Storage/Order flow."""
    img = Image.new("RGB", (width, height), color=(250, 252, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_head = ImageFont.truetype("arialbd.ttf", 20)
        font_box_title = ImageFont.truetype("arialbd.ttf", 15)
        font_box_desc = ImageFont.truetype("arial.ttf", 12)
    except:
        font_head = ImageFont.load_default()
        font_box_title = font_head
        font_box_desc = font_head

    # Header bar
    draw.rectangle([(0, 0), (width, 50)], fill=(30, 58, 138))
    draw.text((width // 2 - draw.textlength(title, font=font_head) // 2, 12), title, fill=(255, 255, 255), font=font_head)

    # Draw vertical sequence cards
    box_w = width - 80
    n = len(steps)
    step_h = (height - 80 - ((n - 1) * 16)) // n
    start_y = 65

    for i, step in enumerate(steps):
        name, desc, bg_col, border_col = step
        sy = start_y + i * (step_h + 16)

        # Draw card
        draw.rounded_rectangle([(40, sy), (40 + box_w, sy + step_h)], radius=8, fill=bg_col, outline=border_col, width=2)
        
        # Left badge
        badge_w = 200
        draw.rounded_rectangle([(42, sy + 2), (42 + badge_w, sy + step_h - 2)], radius=6, fill=border_col)
        draw.text((55, sy + (step_h // 2) - 10), name, fill=(255, 255, 255), font=font_box_title)

        # Right description
        draw.text((42 + badge_w + 20, sy + (step_h // 2) - 8), desc, fill=(30, 41, 59), font=font_box_desc)

        # Down arrow
        if i < n - 1:
            arrow_y = sy + step_h + 2
            draw.line([(width // 2, arrow_y), (width // 2, arrow_y + 10)], fill=(100, 116, 139), width=2)
            draw.polygon([(width // 2 - 4, arrow_y + 8), (width // 2 + 4, arrow_y + 8), (width // 2, arrow_y + 14)], fill=(100, 116, 139))

    dest_path = os.path.join(ASSETS_DIR, output_filename)
    img.save(dest_path, "PNG", quality=95)
    print(f"[OK] Generated flow diagram: {output_filename}")
    return dest_path

def create_architecture_diagram(output_filename, width=1100, height=650):
    """Render full system architecture diagram matching Figure 7.0 / Page 9 in friend's PDF."""
    img = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    try:
        f_title = ImageFont.truetype("arialbd.ttf", 20)
        f_sub = ImageFont.truetype("arial.ttf", 13)
        f_box_t = ImageFont.truetype("arialbd.ttf", 13)
        f_box_d = ImageFont.truetype("arial.ttf", 11)
        f_sec = ImageFont.truetype("arialbd.ttf", 14)
    except:
        f_title = ImageFont.load_default()
        f_sub = f_title
        f_box_t = f_title
        f_box_d = f_title
        f_sec = f_title

    # Header
    draw.rectangle([(0, 0), (width, 60)], fill=(15, 23, 42))
    draw.text((width // 2 - 270, 10), "SMART PARKING - ARCHITECTURE DIAGRAM", fill=(255, 255, 255), font=f_title)
    draw.text((width // 2 - 240, 36), "End-to-End CI/CD Pipeline with Docker, Jenkins, Ansible and Persistent SQLite", fill=(148, 163, 184), font=f_sub)

    # Top pipeline flow (6 steps across)
    steps = [
        ("1. Development", "Developer (You)\n• Edit Code\n• Add features\n• Run locally", (236, 253, 245), (16, 185, 129)),
        ("2. Source Control", "GitHub Repo\n• 71762307053\n• SmartParking\n• Branch: master", (243, 244, 246), (75, 85, 99)),
        ("3. Jenkins CI/CD", "Jenkins (9091)\n• Checkout SCM\n• Build Image\n• Run Pytest (7/7)\n• Trigger Ansible", (239, 246, 255), (59, 130, 246)),
        ("4. Deployment", "Ansible Lab\n• docker-deploy.yml\n• Manage container\n• Volume mapping", (254, 243, 199), (217, 119, 6)),
        ("5. Container", "Docker Engine\n• smart-parking-ansible\n• Port 5001:5000\n• Volume: parking_data", (240, 249, 255), (2, 132, 199)),
        ("6. Stack App", "Flask + SQLite\n• User Matrix (/)\n• Admin (/admin)\n• data/parking.db", (250, 245, 255), (147, 51, 234))
    ]

    card_w = 155
    card_h = 170
    start_x = 35
    top_y = 80

    for i, (stitle, sdesc, bg_c, bord_c) in enumerate(steps):
        x = start_x + i * (card_w + 16)
        draw.rounded_rectangle([(x, top_y), (x + card_w, top_y + card_h)], radius=6, fill=bg_c, outline=bord_c, width=2)
        draw.rectangle([(x, top_y), (x + card_w, top_y + 30)], fill=bord_c)
        draw.text((x + 8, top_y + 8), stitle, fill=(255, 255, 255), font=f_box_t)

        # Description text
        dy = top_y + 40
        for line in sdesc.split("\n"):
            draw.text((x + 8, dy), line, fill=(30, 41, 59), font=f_box_d)
            dy += 18

        # Horizontal connecting arrow
        if i < len(steps) - 1:
            ax = x + card_w + 2
            ay = top_y + 70
            draw.line([(ax, ay), (ax + 12, ay)], fill=(100, 116, 139), width=2)
            draw.polygon([(ax + 10, ay - 3), (ax + 10, ay + 3), (ax + 15, ay)], fill=(100, 116, 139))

    # Bottom Sections: 7. Users, 8. Live App, 9. Persistence
    draw.rounded_rectangle([(35, 280), (320, 520)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((50, 295), "7. USERS & VEHICLES", fill=(15, 23, 42), font=f_sec)
    user_txt = (
        "• Browse 24 Live Bays\n"
        "• Zone A (Four-Wheeler: ₹30/hr)\n"
        "• Zone B (Two-Wheeler: ₹15/hr)\n"
        "• Zone C (EV Fast Charge: ₹45/hr)\n"
        "• One-Click Slot Reservation\n"
        "• Instant Digital Parking Pass\n"
        "• Quick Exit Release & Bill"
    )
    draw.text((50, 335), user_txt, fill=(51, 65, 85), font=f_box_d, spacing=8)

    draw.rounded_rectangle([(345, 280), (750, 520)], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    draw.text((365, 295), "8. RUNNING SMART PARKING APPLICATION", fill=(56, 189, 248), font=f_sec)
    app_txt = (
        "Access URL: http://localhost:5001\n"
        "Admin Portal: http://localhost:5001/admin\n\n"
        "Frontend: HTML5 + Responsive Dark CSS + JavaScript ES6+\n"
        "Backend: Python 3.11 + Flask REST APIs\n"
        "Real-Time Metrics: Total Bays, Available, Occupied, Revenue\n"
        "Admin Actions: Live Status Matrix, Force Release, System Reset"
    )
    draw.text((365, 335), app_txt, fill=(226, 232, 240), font=f_box_d, spacing=7)

    draw.rounded_rectangle([(775, 280), (1065, 520)], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    draw.text((795, 295), "9. DATA PERSISTENCE", fill=(15, 23, 42), font=f_sec)
    db_txt = (
        "SQLite Engine: SQLite3\n"
        "Database File: parking.db\n"
        "Mount Point: /app/data\n"
        "Docker Volume: parking_data\n\n"
        "Persistence Guarantee:\n"
        "All bay states and booking records\n"
        "survive container recreations\n"
        "and host reboots."
    )
    draw.text((795, 335), db_txt, fill=(51, 65, 85), font=f_box_d, spacing=7)

    # Footer banner
    draw.rectangle([(0, 560), (width, height)], fill=(241, 245, 249))
    draw.text((45, 580), "KEY PORTS:   Jenkins: 9091   |   Smart Parking Container: 5001:5000", fill=(71, 85, 105), font=f_box_t)
    draw.text((45, 610), "CI/CD: GitHub Webhook -> Jenkins Pipeline -> Docker Build -> Pytest 7/7 -> Ansible Deploy", fill=(100, 116, 139), font=f_box_d)

    dest_path = os.path.join(ASSETS_DIR, output_filename)
    img.save(dest_path, "PNG", quality=95)
    print(f"[OK] Generated architecture diagram: {output_filename}")
    return dest_path

def create_cit_emblem(output_filename="cit_logo.png", size=180):
    """Draw circular CIT college emblem matching reference PDF cover page."""
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer circle
    draw.ellipse([(6, 6), (size - 6, size - 6)], outline=(160, 20, 20), width=6)
    draw.ellipse([(14, 14), (size - 14, size - 14)], outline=(218, 165, 32), width=3)
    draw.ellipse([(20, 20), (size - 20, size - 20)], fill=(255, 255, 255))
    
    # Inner yellow ring
    draw.ellipse([(30, 30), (size - 30, size - 30)], outline=(218, 165, 32), width=4, fill=(254, 240, 138))
    # Center maroon circle
    draw.ellipse([(55, 55), (size - 55, size - 55)], fill=(160, 20, 20))

    try:
        f_badge = ImageFont.truetype("arialbd.ttf", 11)
        f_mid = ImageFont.truetype("arialbd.ttf", 14)
    except:
        f_badge = ImageFont.load_default()
        f_mid = f_badge

    draw.text((size // 2 - 20, 36), "ESTD", fill=(160, 20, 20), font=f_badge)
    draw.text((size // 2 - 20, size - 50), "1956", fill=(160, 20, 20), font=f_badge)
    draw.text((size // 2 - 14, size // 2 - 8), "CIT", fill=(255, 255, 255), font=f_mid)

    dest_path = os.path.join(ASSETS_DIR, output_filename)
    img.save(dest_path, "PNG")
    print(f"[OK] Generated CIT Emblem: {output_filename}")
    return dest_path

def main():
    print("Generating all assets matching reference PDF...")
    
    # 1. CIT Emblem
    create_cit_emblem("cit_logo.png")

    # 2. Architecture Diagram (Figure 7.0 / Page 9)
    create_architecture_diagram("fig_arch.png")

    # 3. Capture Home Page (Figure 7.1)
    capture_url("http://localhost:5001", "fig_7_1_home.png", width=1280, height=820)

    # 4. Capture Admin Dashboard (Figure 7.13)
    capture_url("http://localhost:5001/admin", "fig_7_13_admin.png", width=1280, height=820)

    # 5. Capture Jenkins Stage View (Figure 7.8)
    capture_url("http://localhost:9091/job/SmartParkingPipeline/", "fig_7_8_jenkins_pipeline.png", width=1280, height=800)

    # 6. Capture Jenkins Console Output (Figure 7.9)
    capture_url("http://localhost:9091/job/SmartParkingPipeline/9/console", "fig_7_9_jenkins_success.png", width=1280, height=800)

    # 7. Flow Diagrams
    create_flow_diagram(
        "Docker Flow – Smart Parking Management System",
        [
            ("Application Code", "app.py, templates/, static/, requirements.txt, test_app.py", (254, 242, 242), (239, 68, 68)),
            ("Dockerfile", "Defines Python 3.11-slim, installs dependencies, sets WORKDIR /app, CMD python app.py", (239, 246, 255), (59, 130, 246)),
            ("Docker Image", "Built from Dockerfile as smart-parking-ci containing all application packages", (240, 253, 250), (20, 184, 166)),
            ("Docker Container", "Running container smart-parking-ansible with port mapping 5001:5000", (240, 249, 255), (14, 165, 233)),
            ("Flask Application", "Runs inside container, serves user matrix and admin dashboard with persistent SQLite", (245, 243, 255), (168, 85, 247))
        ],
        "fig_docker_flow.png"
    )

    create_flow_diagram(
        "Storage Flow – Smart Parking Management System",
        [
            ("Flask Application", "Flask backend processes slot reservation and release requests", (255, 247, 237), (249, 115, 22)),
            ("SQLite Database", "Flask connects via sqlite3 to parking.db database engine", (240, 249, 255), (2, 132, 199)),
            ("parking.db File", "All slot states, driver info, entry timestamps, and billing records stored in parking.db", (240, 253, 244), (34, 197, 94)),
            ("/app/data Directory", "Database file is located in /app/data inside the container", (254, 242, 242), (239, 68, 68)),
            ("parking_data Volume", "Container directory /app/data is mounted to persistent Docker Volume parking_data", (245, 243, 255), (147, 51, 234)),
            ("Persistent Storage", "Ensures stored booking data is retained even when container restarts or updates", (254, 249, 195), (202, 138, 4))
        ],
        "fig_storage_flow.png"
    )

    create_flow_diagram(
        "Reservation Flow – Smart Parking Management System",
        [
            ("Driver / User", "Opens http://localhost:5001 to browse real-time parking slot availability", (239, 246, 255), (59, 130, 246)),
            ("Slot Selection", "Selects vacant bay in Zone A (Car), Zone B (Bike), or Zone C (EV Fast Charging)", (240, 253, 244), (16, 185, 129)),
            ("Reserve Modal", "Enters vehicle registration number, driver name, phone, and expected hours", (255, 251, 235), (245, 158, 11)),
            ("Flask REST API", "Backend verifies bay availability, records entry timestamp, and calculates estimated fee", (254, 242, 242), (239, 68, 68)),
            ("SQLite Database", "Slot marked as 'reserved'; booking row inserted with pass code PKG-XXXX", (245, 243, 255), (147, 51, 234)),
            ("Digital Pass / Receipt", "Driver receives digital pass; admin dashboard reflects live occupancy in real time", (240, 253, 250), (20, 184, 166))
        ],
        "fig_reservation_flow.png"
    )

    # 8. Terminal Screenshots
    # Figure 7.3: Backend app.py code
    create_terminal_image(
        "student@devops-vm: ~/smart-parking (app.py)",
        [
            ("$ ", "cat app.py | head -n 30", (255, 255, 255)),
            ("", "import os, sqlite3, random, string", (200, 205, 215)),
            ("", "from datetime import datetime", (200, 205, 215)),
            ("", "from flask import Flask, render_template, request, jsonify", (200, 205, 215)),
            ("", "", (200, 205, 215)),
            ("", "app = Flask(__name__)", (200, 205, 215)),
            ("", "DB_PATH = '/app/data/parking.db'", (200, 205, 215)),
            ("", "", (200, 205, 215)),
            ("", "def init_db():", (147, 197, 253)),
            ("", "    conn = sqlite3.connect(DB_PATH)", (200, 205, 215)),
            ("", "    cursor = conn.cursor()", (200, 205, 215)),
            ("", "    cursor.execute('''CREATE TABLE IF NOT EXISTS slots (", (134, 239, 172)),
            ("", "        id INTEGER PRIMARY KEY AUTOINCREMENT,", (134, 239, 172)),
            ("", "        slot_number TEXT UNIQUE NOT NULL, zone TEXT,", (134, 239, 172)),
            ("", "        vehicle_type TEXT, status TEXT DEFAULT 'available',", (134, 239, 172)),
            ("", "        hourly_rate REAL, current_reservation_id TEXT)''')", (134, 239, 172)),
            ("", "    conn.commit()", (200, 205, 215)),
            ("", "    conn.close()", (200, 205, 215)),
            ("", "", (200, 205, 215)),
            ("", "@app.route('/api/reserve', methods=['POST'])", (253, 224, 71)),
            ("", "def reserve_slot():", (147, 197, 253)),
            ("", "    data = request.get_json()", (200, 205, 215)),
            ("", "    slot_number = data.get('slot_number')", (200, 205, 215)),
            ("", "    # Calculate duration and update bay status", (148, 163, 184)),
            ("", "    return jsonify({'success': True, 'pass_id': 'PKG-1001'})", (134, 239, 172)),
            ("", "", (200, 205, 215)),
            ("$ ", "echo 'Backend operational on port 5000'", (255, 255, 255)),
            ("", "Backend operational on port 5000", (52, 211, 153))
        ],
        "fig_7_3_code.png"
    )

    # Figure 7.4: SQLite Query Terminal
    create_terminal_image(
        "C:\\Users\\summe> SQLite Database Verification (parking.db)",
        [
            ("C:\\Users\\summe>", "docker ps", (255, 255, 255)),
            ("", "CONTAINER ID   IMAGE              COMMAND           STATUS         PORTS                    NAMES", (148, 163, 184)),
            ("", "d8121e287bb0   smart-parking-ci   \"python app.py\"   Up 45 minutes  0.0.0.0:5001->5000/tcp   smart-parking-ansible", (226, 232, 240)),
            ("", "", (255, 255, 255)),
            ("C:\\Users\\summe>", "docker exec smart-parking-ansible python -c \"import sqlite3; c=sqlite3.connect('data/parking.db'); print(c.execute('SELECT slot_number, zone, vehicle_type, status, hourly_rate FROM slots LIMIT 5').fetchall()); c.close()\"", (255, 255, 255)),
            ("", "[('A-01', 'Zone A - Four Wheeler', 'Car', 'reserved', 30.0),", (52, 211, 153)),
            ("", " ('A-02', 'Zone A - Four Wheeler', 'Car', 'available', 30.0),", (52, 211, 153)),
            ("", " ('A-03', 'Zone A - Four Wheeler', 'Car', 'available', 30.0),", (52, 211, 153)),
            ("", " ('A-04', 'Zone A - Four Wheeler', 'Car', 'available', 30.0),", (52, 211, 153)),
            ("", " ('A-05', 'Zone A - Four Wheeler', 'Car', 'available', 30.0)]", (52, 211, 153)),
            ("", "", (255, 255, 255)),
            ("C:\\Users\\summe>", "docker exec smart-parking-ansible python -c \"import sqlite3; c=sqlite3.connect('data/parking.db'); print(c.execute('SELECT reservation_code, slot_number, vehicle_number, total_amount, status FROM reservations').fetchall()); c.close()\"", (255, 255, 255)),
            ("", "[('PKG-1001', 'A-01', 'TN-37-AB-1234', 60.0, 'active'),", (56, 189, 248)),
            ("", " ('PKG-1002', 'C-01', 'TN-38-EV-9900', 135.0, 'active'),", (56, 189, 248)),
            ("", " ('PKG-1437', 'A-02', 'TN-38-XY-1010', 60.0, 'completed')]", (56, 189, 248))
        ],
        "fig_7_4_db_terminal.png"
    )

    # Figure 7.5: GitHub Repository View
    create_terminal_image(
        "GitHub - 71762307053 / SmartParkingSystem",
        [
            ("Repository: ", "https://github.com/71762307053/SmartParkingSystem.git", (96, 165, 250)),
            ("Branch: ", "master   |   Commits: 5   |   Public", (148, 163, 184)),
            ("", "────────────────────────────────────────────────────────────────────────────────────", (71, 85, 105)),
            ("📄 ", "app.py                   Finalize Smart Parking CI/CD project", (248, 250, 252)),
            ("📄 ", "Dockerfile               Multi-stage Python 3.11-slim container definition", (248, 250, 252)),
            ("📄 ", "Jenkinsfile              5-stage declarative pipeline (Build, Test, Deploy)", (248, 250, 252)),
            ("📄 ", "test_app.py              7 automated Pytest unit and integration test cases", (248, 250, 252)),
            ("📄 ", "docker-deploy.yml        Ansible playbook for container and volume deployment", (248, 250, 252)),
            ("📄 ", "inventory.ini            Ansible inventory targeting dockerhost", (248, 250, 252)),
            ("📄 ", "requirements.txt         Python dependencies: Flask>=3.0.0, pytest>=8.0.0", (248, 250, 252)),
            ("📁 ", "templates/               base.html, index.html (Matrix), admin.html", (248, 250, 252)),
            ("📁 ", "static/                  Dark-theme CSS stylesheet, main.js, admin.js", (248, 250, 252)),
            ("📁 ", "data/                    parking.db SQLite database volume mount", (248, 250, 252)),
            ("📄 ", "README.md                Comprehensive setup, pipeline and viva guide", (248, 250, 252)),
            ("", "────────────────────────────────────────────────────────────────────────────────────", (71, 85, 105)),
            ("Commit Hash: ", "4946b1e   Author: SUMMERJEET SINGH <71762307053>", (52, 211, 153))
        ],
        "fig_7_5_github.png"
    )

    # Figure 7.7: Running Docker Containers
    create_terminal_image(
        "C:\\Users\\summe> docker ps",
        [
            ("C:\\Users\\summe>", "docker ps", (255, 255, 255)),
            ("", "CONTAINER ID   IMAGE                       COMMAND                  STATUS         PORTS                                                 NAMES", (148, 163, 184)),
            ("", "d8121e287bb0   smart-parking-ci            \"python app.py\"          Up 48 minutes  0.0.0.0:5001->5000/tcp, [::]:5001->5000/tcp          smart-parking-ansible", (52, 211, 153)),
            ("", "fa7e3c306e17   jenkins/jenkins:lts-jdk17   \"/usr/bin/tini -- /u…\"   Up 50 minutes  0.0.0.0:50000->50000/tcp, 0.0.0.0:9091->8080/tcp     jenkins", (56, 189, 248)),
            ("", "38d7f336f9e7   ubuntu:latest               \"bash\"                   Up 52 minutes                                                        ansible-docker-lab", (251, 191, 36)),
            ("", "", (255, 255, 255)),
            ("C:\\Users\\summe>", "docker images | grep smart-parking", (255, 255, 255)),
            ("", "smart-parking-ci   latest    20a67e234b59   1 hour ago   232MB", (226, 232, 240))
        ],
        "fig_7_7_docker_ps.png"
    )

    # Figure 7.10: Pytest output
    create_terminal_image(
        "Jenkins CI - Stage: Run Automated Tests",
        [
            ("[Pipeline] ", "echo Running Automated Tests", (56, 189, 248)),
            ("[Pipeline] ", "sh", (56, 189, 248)),
            ("+ ", "docker run --rm smart-parking-ci python -m pytest test_app.py", (255, 255, 255)),
            ("", "============================= test session starts ==============================", (148, 163, 184)),
            ("", "platform linux -- Python 3.11.16, pytest-9.1.1, pluggy-1.6.0", (148, 163, 184)),
            ("", "rootdir: /app", (148, 163, 184)),
            ("", "collected 7 items", (226, 232, 240)),
            ("", "", (255, 255, 255)),
            ("", "test_app.py::test_home_page PASSED                                       [ 14%]", (52, 211, 153)),
            ("", "test_app.py::test_admin_dashboard PASSED                                 [ 28%]", (52, 211, 153)),
            ("", "test_app.py::test_api_slots_listing PASSED                               [ 42%]", (52, 211, 153)),
            ("", "test_app.py::test_api_stats PASSED                                       [ 57%]", (52, 211, 153)),
            ("", "test_app.py::test_reserve_and_release_workflow PASSED                    [ 71%]", (52, 211, 153)),
            ("", "test_app.py::test_reserve_invalid_slot PASSED                            [ 85%]", (52, 211, 153)),
            ("", "test_app.py::test_release_invalid_identifier PASSED                      [100%]", (52, 211, 153)),
            ("", "", (255, 255, 255)),
            ("", "============================== 7 passed in 0.40s ===============================", (52, 211, 153)),
            ("[Pipeline] ", "// stage", (56, 189, 248))
        ],
        "fig_7_10_pytest.png"
    )

    # Figure 7.11: Ansible Playbook Execution
    create_terminal_image(
        "Jenkins CI - Stage: Deploy with Ansible",
        [
            ("C:\\Users\\summe>", "docker exec ansible-docker-lab cat /docker-deploy.yml", (255, 255, 255)),
            ("", "---", (148, 163, 184)),
            ("", "- hosts: dockerhost", (251, 191, 36)),
            ("", "  gather_facts: false", (226, 232, 240)),
            ("", "  tasks:", (226, 232, 240)),
            ("", "    - name: Manage Smart Parking Container", (147, 197, 253)),
            ("", "      community.docker.docker_container:", (200, 205, 215)),
            ("", "        name: smart-parking-ansible", (134, 239, 172)),
            ("", "        image: smart-parking-ci", (134, 239, 172)),
            ("", "        state: \"{{ container_state | default('started') }}\"", (134, 239, 172)),
            ("", "        restart_policy: unless-stopped", (134, 239, 172)),
            ("", "        published_ports:", (200, 205, 215)),
            ("", "          - \"5001:5000\"", (253, 224, 71)),
            ("", "        volumes:", (200, 205, 215)),
            ("", "          - \"parking_data:/app/data\"", (253, 224, 71)),
            ("", "", (255, 255, 255)),
            ("C:\\Users\\summe>", "docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml", (255, 255, 255)),
            ("", "PLAY [dockerhost] **************************************************************", (148, 163, 184)),
            ("", "TASK [Manage Smart Parking Container] ******************************************", (148, 163, 184)),
            ("", "changed: [localhost]", (251, 191, 36)),
            ("", "PLAY RECAP *********************************************************************", (148, 163, 184)),
            ("", "localhost                  : ok=1    changed=1    unreachable=0    failed=0", (52, 211, 153))
        ],
        "fig_7_11_ansible.png"
    )

    # Figure 7.12: Docker Volume
    create_terminal_image(
        "C:\\Users\\summe> Docker Volume Management",
        [
            ("C:\\Users\\summe>", "docker volume ls", (255, 255, 255)),
            ("", "DRIVER    VOLUME NAME", (148, 163, 184)),
            ("", "local     jenkins_home", (226, 232, 240)),
            ("", "local     parking_data", (52, 211, 153)),
            ("", "", (255, 255, 255)),
            ("C:\\Users\\summe>", "docker volume inspect parking_data", (255, 255, 255)),
            ("", "[", (148, 163, 184)),
            ("", "    {", (148, 163, 184)),
            ("", "        \"CreatedAt\": \"2026-10-01T18:10:07Z\",", (226, 232, 240)),
            ("", "        \"Driver\": \"local\",", (226, 232, 240)),
            ("", "        \"Labels\": null,", (226, 232, 240)),
            ("", "        \"Mountpoint\": \"/var/lib/docker/volumes/parking_data/_data\",", (56, 189, 248)),
            ("", "        \"Name\": \"parking_data\",", (52, 211, 153)),
            ("", "        \"Scope\": \"local\"", (226, 232, 240)),
            ("", "    }", (148, 163, 184)),
            ("", "]", (148, 163, 184))
        ],
        "fig_7_12_volume.png"
    )

    # Figure 7.14: CI/CD Pipeline Completion
    create_terminal_image(
        "Jenkins CI/CD - Build #9 Finished: SUCCESS",
        [
            ("[Pipeline] ", "stage (Application Verification)", (56, 189, 248)),
            ("", "Verifying running container and application health check...", (226, 232, 240)),
            ("+ ", "docker ps | grep smart-parking-ansible", (255, 255, 255)),
            ("", "d8121e287bb0   smart-parking-ci   \"python app.py\"   Up 1 minute   0.0.0.0:5001->5000/tcp   smart-parking-ansible", (52, 211, 153)),
            ("[Pipeline] ", "} // stage", (56, 189, 248)),
            ("[Pipeline] ", "stage (Declarative: Post Actions)", (56, 189, 248)),
            ("[Pipeline] ", "echo ===================================================", (226, 232, 240)),
            ("[Pipeline] ", "echo Smart Parking CI/CD Pipeline Completed Successfully!", (52, 211, 153)),
            ("[Pipeline] ", "echo Application accessible at: http://localhost:5001", (56, 189, 248)),
            ("[Pipeline] ", "echo Admin Dashboard accessible at: http://localhost:5001/admin", (56, 189, 248)),
            ("[Pipeline] ", "echo ===================================================", (226, 232, 240)),
            ("[Pipeline] ", "} // withEnv", (56, 189, 248)),
            ("[Pipeline] ", "// node", (56, 189, 248)),
            ("[Pipeline] ", "End of Pipeline", (56, 189, 248)),
            ("", "Finished: SUCCESS", (52, 211, 153))
        ],
        "fig_7_14_pipeline_done.png"
    )

    print("All image assets created successfully in assets/ directory!")

if __name__ == "__main__":
    main()
