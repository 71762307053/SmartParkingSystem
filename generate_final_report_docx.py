import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'''
        <w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
            <w:top w:val="{top}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{left}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{bottom}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{right}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tcBorders>
    '''.format(
        top=kwargs.get('top', 'single'),
        left=kwargs.get('left', 'single'),
        bottom=kwargs.get('bottom', 'single'),
        right=kwargs.get('right', 'single'),
        sz=kwargs.get('sz', '4'),
        color=kwargs.get('color', '888888')
    ))
    tcPr.append(tcBorders)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def generate_report():
    doc = Document()

    # Page Margins 1 inch
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

        # Header: Arial 9pt, gray, right-aligned
        hp = s.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("23IT723 – DevOps Laboratory | Final Project")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(9)
        hrun.font.color.rgb = RGBColor(128, 128, 128)

        # Footer: Arial 9pt, gray, right-aligned
        fp = s.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun = fp.add_run("23IT723 – DevOps Laboratory | Final Project")
        frun.font.name = "Arial"
        frun.font.size = Pt(9)
        frun.font.color.rgb = RGBColor(128, 128, 128)

    # Styling helpers using Arial font
    def add_p(text, font_size=11, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(font_size)
        run.bold = bold
        run.italic = italic
        return p

    def add_bullet(text, space_after=4):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(11)
        return p

    def add_sec_heading(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(title)
        run.font.name = "Arial"
        run.font.size = Pt(13)
        run.bold = True
        return p

    def add_mod_heading(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(title)
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.bold = True
        return p

    def add_img(img_name, caption, width=Inches(5.6)):
        img_path = os.path.join(ASSETS_DIR, img_name)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(img_path, width=width)

            if caption:
                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p_cap.paragraph_format.space_before = Pt(4)
                p_cap.paragraph_format.space_after = Pt(12)
                crun = p_cap.add_run(caption)
                crun.font.name = "Arial"
                crun.font.size = Pt(10)
                crun.bold = False

    # ================= PAGE 1: COVER PAGE =================
    add_p("COIMBATORE INSTITUTE OF TECHNOLOGY", font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=40, space_after=4)
    add_p("(Government Aided Autonomous Institution Affiliated to Anna University)", font_size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=35)
    
    add_p("23IT723 - DEVOPS LABORATORY", font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_p("PROJECT", font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_p("SMART PARKING MANAGEMENT SYSTEM", font_size=15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=35)

    # Center Emblem
    add_img("cit_logo.png", caption="", width=Inches(1.8))

    add_p("OCTOBER 2026", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=25, space_after=70)
    
    add_p("Submitted by", font_size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_p("71762307053   SUMMERJEET SINGH", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=0)
    doc.add_page_break()

    # ================= PAGE 2: BONAFIDE CERTIFICATE =================
    add_p("COIMBATOREINSTITUTEOFTECHNOLOGY", font_size=15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=4)
    add_p("(Government Aided Autonomous Institution Affiliated to Anna University)", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    add_p("BONAFIDE CERTIFICATE", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=32)

    cert_msg = (
        "Certified that this project report titled “SMART PARKING MANAGEMENT SYSTEM” is the "
        "bonafide work of 71762307053- SUMMERJEET SINGH completed during the academic year "
        "2025-2026-Semester VII for the project presentation of 23IT723 - DEVOPS LABORATORY under our supervision."
    )
    add_p(cert_msg, font_size=11.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=28, line_spacing=1.25)
    add_p("Certified that the candidate was examined by using the project work examination.", font_size=12, bold=True, italic=True, space_after=36)
    
    add_p("Review Members:", font_size=12, bold=True, space_after=12)
    add_p("1.   Dr.M.Sangeetha", font_size=12, bold=True, space_after=8)
    add_p("2.   Dr.E.Arul", font_size=12, bold=True, space_after=0)
    doc.add_page_break()

    # ================= PAGE 3: EVALUATION SCHEME =================
    add_p("23IT723 – DEVOPS LABORATORY", font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=2)
    add_p("FINAL MINI PROJECT – EVALUATION SCHEME", font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_p("Final Mini Project Assessment", font_size=11, bold=True, space_after=3)
    add_p(
        "The final mini project shall require students to integrate the major DevOps practices covered in the laboratory. "
        "The project should demonstrate practical implementation of version control, collaborative development, Continuous "
        "Integration, containerization and/or automated configuration/provisioning, with proper execution evidence.",
        font_size=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8
    )

    eval_rows = [
        ("S.No.", "Evaluation Component", "Key Verification Points", "Marks"),
        ("1", "Problem Definition &\nProject Planning", "Problem statement, objectives, requirements, scope, module identification, technology selection and workflow planning.", "10"),
        ("2", "Git Repository &\nVersion Control", "Repository creation, meaningful commits, README, .gitignore, remote repository, push/pull/fetch operations and commit history.", "15"),
        ("3", "Branching, Merging &\nCollaboration", "Feature branches, parallel development, merging, conflict handling, branch organization and collaborative workflow.", "10"),
        ("4", "Application\nDevelopment & Build", "Working application/source code, project structure, dependency management, build configuration and successful execution.", "15"),
        ("5", "Jenkins Continuous\nIntegration", "Jenkins configuration, source-code integration, automated checkout, build job/pipeline, build execution and console verification.", "15"),
        ("6", "Docker /\nContainerization", "Dockerfile, image creation, container execution, port/configuration handling, application deployment and container verification.", "10"),
        ("7", "Automation /\nConfiguration Management", "Ansible/Chef/Puppet/SaltStack or equivalent automation where applicable; repeatable configuration/provisioning and successful execution.", "5"),
        ("8", "Testing & Verification", "Functional testing, build verification, error identification, test evidence and corrective action.", "5"),
        ("9", "Documentation &\nTechnical Presentation", "Architecture/workflow diagram, commands/configuration, screenshots, results, troubleshooting, conclusion and repository details.", "5"),
        ("10", "Final Demonstration &\nViva-Voce", "Live demonstration, explanation of implementation, troubleshooting responses and technical understanding.", "10"),
        ("", "TOTAL", "", "100")
    ]
    t_ev = doc.add_table(rows=len(eval_rows), cols=4)
    t_ev.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_w = [Inches(0.6), Inches(1.8), Inches(3.2), Inches(0.8)]
    for r_idx, r_data in enumerate(eval_rows):
        for c_idx, val in enumerate(r_data):
            cell = t_ev.cell(r_idx, c_idx)
            cell.width = c_w[c_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(2.5)
            cp.paragraph_format.space_after = Pt(2.5)
            cp.paragraph_format.line_spacing = 1.05
            run = cp.add_run(val)
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            if r_idx == 0 or r_idx == len(eval_rows) - 1:
                run.bold = True
                set_cell_background(cell, "F2F2F2")
            if c_idx in [0, 3]:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    doc.add_page_break()

    # ================= PAGE 4: DEMO MARK DISTRIBUTION =================
    add_p("Recommended Mark Distribution within the Final Demonstration", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=4)
    add_p("For uniform evaluation, the examiner may use the following internal split for the implementation and demonstration components.", font_size=10, space_after=6)

    demo_rows = [
        ("Assessment Area", "Marks", "Awarded Marks", "Remarks"),
        ("Working implementation and correctness", "30", "", ""),
        ("DevOps tool integration and automation", "20", "", ""),
        ("Version control and collaborative workflow", "15", "", ""),
        ("Build / deployment / container verification", "15", "", ""),
        ("Testing and troubleshooting", "5", "", ""),
        ("Documentation and technical presentation", "5", "", ""),
        ("Live demonstration and viva-voce", "10", "", ""),
        ("TOTAL", "100", "", "")
    ]
    t_dm = doc.add_table(rows=len(demo_rows), cols=4)
    t_dm.alignment = WD_TABLE_ALIGNMENT.CENTER
    dm_w = [Inches(2.6), Inches(0.8), Inches(1.3), Inches(1.7)]
    for r_idx, r_data in enumerate(demo_rows):
        for c_idx, val in enumerate(r_data):
            cell = t_dm.cell(r_idx, c_idx)
            cell.width = dm_w[c_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(2)
            cp.paragraph_format.space_after = Pt(2)
            run = cp.add_run(val)
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            if r_idx == 0 or r_idx == len(demo_rows) - 1:
                run.bold = True
                set_cell_background(cell, "F2F2F2")
            if c_idx in [1, 2]:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    add_p("Minimum Evidence to be Submitted", font_size=11, bold=True, space_before=8, space_after=3)
    add_bullet("Project repository URL and project README.")
    add_bullet("Git commit history and branch/merge evidence.")
    add_bullet("Jenkins job/pipeline configuration and successful build evidence.")
    add_bullet("Dockerfile, image and running container evidence where Docker is used.")
    add_bullet("Automation/configuration scripts where applicable.")
    add_bullet("Application execution and testing evidence.")
    add_bullet("Architecture/workflow diagram.")
    add_bullet("Short technical report containing implementation steps, results and troubleshooting.")
    add_bullet("Live demonstration of the complete DevOps workflow.")

    add_p("Evaluation Guidelines", font_size=11, bold=True, space_before=6, space_after=3)
    add_bullet("Marks shall be awarded primarily for a working implementation and demonstrable output.")
    add_bullet("Copied source code without functional understanding shall not receive full marks.")
    add_bullet("Screenshots may support the evaluation, but critical components should be demonstrated live wherever possible.")
    add_bullet("Students should use meaningful repository names, branch names and commit messages.")
    add_bullet("If a component is not applicable to the selected project, the student shall obtain faculty approval and demonstrate an equivalent DevOps automation component.")
    add_bullet("The final viva shall focus on the student's own implementation, commands used, tool configuration and troubleshooting.")

    add_p("Faculty Evaluation Record", font_size=11, bold=True, space_before=8, space_after=3)
    t_fc = doc.add_table(rows=4, cols=4)
    t_fc.alignment = WD_TABLE_ALIGNMENT.CENTER
    fc_w = [Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.6)]
    fc_vals = [
        [("Student Name", True), ("SUMMERJEET SINGH", False), ("Register No.", True), ("71762307053", False)],
        [("Project Title", True), ("Smart Parking System", False), ("Date", True), ("02-10-2026", False)],
        [("Final Mark", True), ("", False), ("", False), ("", False)],
        [("Faculty Evaluator I", True), ("", False), ("Signature", True), ("", False)]
    ]
    for r_idx, row in enumerate(fc_vals):
        for c_idx, (txt, is_b) in enumerate(row):
            cell = t_fc.cell(r_idx, c_idx)
            cell.width = fc_w[c_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(2.5)
            cp.paragraph_format.space_after = Pt(2.5)
            run = cp.add_run(txt)
            run.font.name = "Arial"
            run.font.size = Pt(9.5)
            run.bold = is_b
            if is_b:
                set_cell_background(cell, "F9F9F9")
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    doc.add_page_break()

    # ================= PAGES 5-6: TABLE OF CONTENTS =================
    add_p("TABLE OF CONTENTS", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=14)

    toc_items = [
        ("S. NO.", "CONTENT", "PAGE NO."),
        ("1", "INTRODUCTION", "05"),
        ("2", "OBJECTIVES", "05"),
        ("3", "ABSTRACT", "06"),
        ("4", "TECHOLOGY STACK", "06"),
        ("5", "SYSTEM ARCHITECTURE", "07"),
        ("6", "MODULE 1 — USER INTERFACE & PARKING SLOT DISPLAY", "08"),
        ("7", "MODULE 2 — FLASK BACKEND & RESERVATION MANAGEMENT", "09"),
        ("8", "MODULE 3 — SQLITE DATABASE MANAGEMENT", "10"),
        ("9", "MODULE 4 — GIT & GITHUB SOURCE CONTROL", "11"),
        ("10", "MODULE 5 — DOCKER CONTAINERIZATION", "12"),
        ("11", "MODULE 6 — JENKINS CI/CD PIPELINE", "14"),
        ("12", "MODULE 7 — AUTOMATED TESTING", "15"),
        ("13", "MODULE 8 — ANSIBLE DEPLOYMENT", "17"),
        ("14", "MODULE 9 — PERSISTENT STORAGE", "18"),
        ("15", "MODULE 10 — ADMIN & OCCUPANCY MANAGEMENT", "19"),
        ("16", "MODULE 11 — CI/CD INTEGRATION", "20"),
        ("17", "MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION", "21"),
        ("18", "RESULTS AND OUTPUT", "23"),
        ("19", "COMMANDS USED", "23"),
        ("20", "ADVANTAGES", "28"),
        ("21", "LIMITATIONS", "28"),
        ("22", "FUTURE ENHANCEMENTS", "29"),
        ("23", "CONCLUSION", "29")
    ]
    t_tc = doc.add_table(rows=len(toc_items), cols=3)
    t_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
    tc_w = [Inches(0.8), Inches(4.5), Inches(1.1)]
    for r_idx, r_data in enumerate(toc_items):
        for c_idx, val in enumerate(r_data):
            cell = t_tc.cell(r_idx, c_idx)
            cell.width = tc_w[c_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(3)
            cp.paragraph_format.space_after = Pt(3)
            run = cp.add_run(val)
            run.font.name = "Arial"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.bold = True
                set_cell_background(cell, "F2F2F2")
            if c_idx in [0, 2]:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    doc.add_page_break()

    # ================= PAGE 7: INTRODUCTION & OBJECTIVES =================
    add_sec_heading("1. INTRODUCTION")
    intro_txt = (
        "The Smart Parking Management System is a web-based vehicle parking space reservation and management system "
        "developed to simplify the process of locating, reserving, and tracking parking slots in crowded campus, commercial, "
        "or municipal environments. The system allows users to browse available parking slots across different vehicle zones "
        "(Cars, Bikes, and Electric Vehicles), check hourly tariffs, select a vacant bay, and instantly place reservations "
        "through an intuitive digital interface. An admin dashboard is also provided to view and manage placed orders and "
        "parking slot occupancy. The application is developed using HTML, CSS, JavaScript, Python, Flask, and SQLite, with "
        "Flask handling backend operations and SQLite storing slot states and reservation information. The project also incorporates "
        "DevOps practices to automate the development, testing, and deployment process. Git and GitHub are used for source code "
        "management, while Jenkins automates the CI/CD pipeline. Docker provides application containerization, Pytest performs "
        "automated testing, and Ansible automates deployment and container configuration. A Docker Volume is used to provide "
        "persistent storage for the SQLite database. The project combines a functional parking reservation system with DevOps "
        "automation to provide a structured and reliable approach to application development and deployment."
    )
    add_p(intro_txt, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14, line_spacing=1.2)

    add_sec_heading("2.OBJECTIVES")
    add_bullet("To develop a digital parking management system that enables users to browse, search, select parking bays, and place reservations conveniently.")
    add_bullet("To implement an admin dashboard for viewing placed reservations and maintaining parking slot occupancy using SQLite.")
    add_bullet("To organize parking data systematically by zones (Cars, Bikes, EV) and provide quick access to stored records through the admin dashboard.")
    add_bullet("To implement DevOps practices throughout the application development and deployment process using Git, GitHub, and Jenkins.")
    add_bullet("To automate the CI/CD workflow using Jenkins for building, testing, and deploying the application.")
    add_bullet("To containerize the application using Docker to provide a consistent and portable execution environment.")
    add_bullet("To integrate Pytest for automated testing to verify application functionality and reduce errors before deployment.")
    add_bullet("To automate application deployment and container configuration using Ansible.")
    add_bullet("To implement Docker Volume for persistent storage of the SQLite database and ensure that booking data is retained even when the application container is recreated.")
    doc.add_page_break()

    # ================= PAGE 8: ABSTRACT & TECH STACK =================
    add_sec_heading("3. ABSTRACT")
    abs_txt = (
        "The Smart Parking Management System is a web-based parking reservation and management system designed to simplify "
        "the process of finding and reserving parking spaces in a facility environment. Traditional parking operations may involve "
        "long queues, manual ticket processing, difficulty in tracking bay occupancy, and challenges in maintaining reservation records. "
        "The proposed system provides a digital platform where users can browse available parking bays, check hourly tariffs, select "
        "slots, and reserve spots conveniently. An administrative dashboard is also provided for viewing and managing parking lot occupancy. "
        "The application is developed using HTML, CSS, JavaScript, Python, Flask, and SQLite, with Flask handling backend operations and SQLite "
        "storing reservation information. The project also implements DevOps practices to automate the software development, testing, "
        "and deployment process. Git and GitHub are used for version control and source code management, while Jenkins automates the CI/CD "
        "pipeline. Docker is used to containerize the application and provide a consistent execution environment, Pytest performs automated "
        "testing, and Ansible automates application deployment and container configuration. A Docker Volume named parking_data is used "
        "to provide persistent storage for the SQLite database, ensuring that stored booking information is retained even when the application "
        "container is recreated. The complete workflow follows GitHub → Jenkins → Docker Build → Pytest → Ansible → Docker Container → "
        "Flask → SQLite, demonstrating the integration of a functional web application with modern DevOps practices and persistent data management."
    )
    add_p(abs_txt, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14, line_spacing=1.2)

    add_sec_heading("4.TECHNOLOGY STACK")
    tech_s = [
        ("Technology", "Version", "Purpose"),
        ("HTML", "HTML5", "Web page structure"),
        ("CSS", "CSS3", "User interface styling"),
        ("JavaScript", "ES6+", "Frontend interaction"),
        ("Python", "3.11", "Backend programming"),
        ("Flask", "3.0.0", "Backend web framework"),
        ("SQLite", "3.x", "Database management"),
        ("Git", "2.x", "Version control"),
        ("GitHub", "—", "Source code repository"),
        ("Jenkins", "2.541.3 / LTS", "CI/CD automation"),
        ("Docker", "26.x+ / 28.x+", "Application containerization"),
        ("Pytest", "8.3.5", "Automated testing"),
        ("Ansible", "2.10.8+", "Deployment automation"),
        ("Docker SDK / Community Docker", "community.docker 1.2.2+", "Docker management through Ansible"),
        ("Docker Volume", "parking_data", "Persistent storage mounted to /app/data")
    ]
    t_ts = doc.add_table(rows=len(tech_s), cols=3)
    t_ts.alignment = WD_TABLE_ALIGNMENT.CENTER
    ts_w = [Inches(2.3), Inches(1.7), Inches(2.4)]
    for r_idx, r_data in enumerate(tech_s):
        for c_idx, val in enumerate(r_data):
            cell = t_ts.cell(r_idx, c_idx)
            cell.width = ts_w[c_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(3)
            cp.paragraph_format.space_after = Pt(3)
            run = cp.add_run(val)
            run.font.name = "Arial"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.bold = True
                set_cell_background(cell, "F2F2F2")
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    doc.add_page_break()

    # ================= PAGE 9: SYSTEM ARCHITECTURE =================
    add_sec_heading("5.SYSTEM ARCHITECTURE")
    add_img("fig_arch.png", caption="")

    arch_list = [
        "1. Development: Developer creates and updates the Smart Parking application.",
        "2. Source Code Management: The application source code and configuration files are maintained using Git.",
        "3. GitHub Repository: The updated code is pushed to the GitHub repository for centralized source code management.",
        "4. Jenkins Trigger: Jenkins retrieves the latest source code from the GitHub repository and starts the CI/CD pipeline.",
        "5. Docker Build: Jenkins builds the application into a Docker image containing the Flask application and required dependencies.",
        "6. Automated Testing: Jenkins runs Pytest to verify the application before deployment.",
        "7. Deployment Automation: After successful testing, Jenkins invokes Ansible to automate the deployment process.",
        "8. Container Configuration: Ansible creates and configures the Docker container with the required image, port mapping, restart policy, and volume configuration.",
        "9. Application Execution: The Docker container runs the Flask backend, HTML/CSS/JavaScript frontend, and SQLite database.",
        "10. User Interaction: Drivers can browse parking slots, check availability, select bays, and reserve or release spots.",
        "11. Admin Management: The admin dashboard allows administrators to view and monitor parking occupancy stored in the database."
    ]
    for s_txt in arch_list:
        add_p(s_txt, font_size=10.5, space_after=4, line_spacing=1.15)

    doc.add_page_break()

    # ================= MODULE 1 =================
    add_mod_heading("MODULE 1 — USER INTERFACE & PARKING SLOT RESERVATION")
    add_p(
        "This module provides the user-facing interface of the Smart Parking application. It is designed to make "
        "parking slot browsing and reservation simple and convenient for drivers.",
        font_size=11, space_after=8
    )
    add_p("Main Features", font_size=11, bold=True, space_after=4)
    add_bullet("Displays available parking slots with relevant details.")
    add_bullet("Provides a search option to find parking slots quickly.")
    add_bullet("Organizes parking bays into different categories (Cars, Bikes, EV Charging).")
    add_bullet("Allows users to select individual parking bays.")
    add_bullet("Allows selected bays to be added to the reservation form.")
    add_bullet("Provides duration management and live cost estimation for selected slots.")
    add_bullet("Displays the selected bay and booking details before confirmation.")
    add_bullet("Allows users to place the final reservation.")
    add_bullet("Provides booking confirmation and token code after successful submission.")
    add_bullet("Provides a simple and user-friendly interface for accessing parking services.")
    add_bullet("Uses responsive interface elements for better usability.")
    add_bullet("Connects the user interface with the Flask backend for processing requests.")
    add_p("Technologies: HTML, CSS, JavaScript.", font_size=10.5, italic=True, space_before=4, space_after=8)

    add_img("fig_7_1_home.png", caption="Figure 7.1: Smart Parking Home Page")
    add_img("fig_7_2_modal.png", caption="Figure 7.2: Parking Slot Selection and Reservation")

    doc.add_page_break()

    # ================= MODULE 2 =================
    add_mod_heading("MODULE 2 — FLASK BACKEND & RESERVATION MANAGEMENT")
    add_p(
        "This module handles the application logic and acts as the communication layer between the frontend and "
        "the SQLite database. Flask processes user requests and manages the complete reservation submission process.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Receives requests from the frontend.")
    add_bullet("Processes slot selection and reservation requests.")
    add_bullet("Handles duration calculation and billing processing.")
    add_bullet("Processes reservation submissions.")
    add_bullet("Generates and manages reservation information.")
    add_bullet("Communicates with the SQLite database.")
    add_bullet("Stores submitted reservation information.")
    add_bullet("Retrieves stored parking records.")
    add_bullet("Handles requests related to the admin dashboard.")
    add_bullet("Connects the frontend interface with backend services.")
    add_bullet("Processes application routes and requests.")
    add_bullet("Runs the Flask application inside the Docker container.")
    add_bullet("Provides the backend services required by the Smart Parking application.")
    add_p("Technology: Python with Flask.", font_size=10.5, italic=True, space_before=4, space_after=8)

    add_img("fig_7_3_code.png", caption="Figure 7.3: Flask Backend Implementation")

    doc.add_page_break()

    # ================= MODULE 3 =================
    add_mod_heading("MODULE 3 — SQLITE DATABASE MANAGEMENT")
    add_p(
        "This module manages the storage and retrieval of parking bay and reservation information using SQLite. "
        "The database provides persistent application data that can be accessed by the Flask backend.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Stores placed reservations.")
    add_bullet("Maintains parking records.")
    add_bullet("Stores reservation-related information.")
    add_bullet("Provides database access to the Flask backend.")
    add_bullet("Allows stored reservations to be retrieved.")
    add_bullet("Makes stored reservations available to the admin dashboard.")
    add_bullet("Maintains the parking.db database file.")
    add_bullet("Stores the database under the application data directory.")
    add_bullet("Works with the Docker Volume for persistent storage.")
    add_bullet("Provides structured storage for reservation information.")
    add_bullet("Maintains reservation data even when the application container is recreated, through the configured Docker Volume.")
    add_p("Database Location:\ndata/parking.db\nInside the Docker container:\n/app/data/parking.db", font_size=10.5, space_before=4, space_after=4)
    add_p("Technology: SQLite.", font_size=10.5, italic=True, space_after=8)

    add_img("fig_7_4_db_terminal.png", caption="Figure 7.4: SQLite Database Containing Parking Information")

    doc.add_page_break()

    # ================= MODULE 4 =================
    add_mod_heading("MODULE 4 — GIT & GITHUB SOURCE CONTROL")
    add_p(
        "This module manages the source code and maintains the development history of the Smart Parking "
        "project. Git is used locally for version control, while GitHub provides the remote repository.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Initializes the project as a Git repository.")
    add_bullet("Tracks changes made to project files.")
    add_bullet("Creates commits for project updates.")
    add_bullet("Maintains the history of project development.")
    add_bullet("Allows changes to be reviewed through Git history.")
    add_bullet("Pushes project code to GitHub.")
    add_bullet("Provides a centralized remote repository.")
    add_bullet("Allows Jenkins to retrieve the latest source code.")
    add_bullet("Maintains the important project files in one repository.")
    add_bullet("Supports integration between source control and the Jenkins pipeline.")
    add_bullet("Helps maintain different versions of the project.")
    add_p("Main Project Files:\napp.py\nDockerfile\nJenkinsfile\ntest_app.py\nrequirements.txt\n.gitignore", font_size=10.5, space_before=4, space_after=4)
    add_p("Technologies: Git and GitHub.", font_size=10.5, italic=True, space_after=8)

    add_img("fig_7_5_github.png", caption="Figure 7.5: Smart Parking GitHub Repository")

    doc.add_page_break()

    # ================= MODULE 5 =================
    add_mod_heading("MODULE 5 — DOCKER CONTAINERIZATION")
    add_p(
        "Docker is used to package and run the Smart Parking application in an isolated and consistent "
        "environment. The application and its required dependencies are packaged into a Docker image.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Creates a Docker image from the application.")
    add_bullet("Packages the application and required dependencies.")
    add_bullet("Provides an isolated execution environment.")
    add_bullet("Creates the application container from the Docker image.")
    add_bullet("Runs the Flask application inside the container.")
    add_bullet("Provides port mapping for application access.")
    add_bullet("Provides a consistent environment for testing and deployment.")
    add_bullet("Allows the application to run independently of the host environment.")
    add_bullet("Works with Jenkins for automated image creation.")
    add_bullet("Works with Ansible for automated deployment.")
    add_bullet("Provides a repeatable application deployment environment.")
    add_p("Docker Configuration:\nDocker Image:\nsmart-parking-ci\nDocker Container:\nsmart-parking-ansible\nPort Mapping:\n5001 → 5000\nThe application can be accessed through:\nhttp://localhost:5001", font_size=10.5, space_before=4, space_after=4)
    add_p("Technology: Docker.", font_size=10.5, italic=True, space_after=8)

    add_img("fig_docker_flow.png", caption="Docker Flow – Smart Parking")
    add_img("fig_7_6_docker_desktop.png", caption="Figure 7.6: Smart Parking Docker Image")
    add_img("fig_7_7_docker_ps.png", caption="Figure 7.7: Running Smart Parking Docker Container")

    doc.add_page_break()

    # ================= MODULE 6 =================
    add_mod_heading("MODULE 6 — JENKINS CI/CD PIPELINE")
    add_p(
        "Jenkins is used to automate the Continuous Integration and Continuous Deployment process. It connects "
        "the source code repository with the application build, testing, and deployment stages.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Retrieves the latest source code from GitHub.")
    add_bullet("Checks out the required project version.")
    add_bullet("Builds the Docker image.")
    add_bullet("Executes automated tests.")
    add_bullet("Provides a sequence of automated pipeline stages.")
    add_bullet("Prevents later stages from proceeding when an earlier stage fails.")
    add_bullet("Invokes the Ansible playbook after successful testing.")
    add_bullet("Provides pipeline execution logs.")
    add_bullet("Reports pipeline success or failure.")
    add_bullet("Automates the overall CI/CD process.")
    add_bullet("Reduces repetitive manual build and deployment activities.")

    add_img("fig_7_8_jenkins_pipeline.png", caption="Figure 7.8: Jenkins CI/CD Pipeline")
    add_img("fig_7_9_jenkins_success.png", caption="Figure 7.9: Successful Jenkins Pipeline Execution")

    doc.add_page_break()

    # ================= MODULE 7 =================
    add_mod_heading("MODULE 7 — AUTOMATED TESTING")
    add_p(
        "This module validates the application automatically before deployment. Pytest is integrated into the "
        "Jenkins pipeline so that the application is tested before the deployment stage.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Uses Pytest for automated testing.")
    add_bullet("Maintains the test file test_app.py.")
    add_bullet("Executes the test inside the Docker image.")
    add_bullet("Verifies the configured application test.")
    add_bullet("Provides automated test execution.")
    add_bullet("Prevents deployment from continuing when an earlier pipeline stage fails.")
    add_bullet("Displays test results in Jenkins.")
    add_bullet("Integrates testing directly into the CI/CD workflow.")
    add_bullet("Reduces the need for repeated manual testing.")
    add_bullet("Helps identify application issues before deployment.")
    add_p("Test File:\ntest_app.py\nTest Command:\npython -m pytest test_app.py\nTest Result:\ncollected 7 items\ntest_app.py . [100%]\n7 passed in 0.40s", font_size=10.5, space_before=4, space_after=8)

    add_img("fig_7_10_pytest.png", caption="Figure 7.10: Successful Automated Test Execution")

    doc.add_page_break()

    # ================= MODULE 8 =================
    add_mod_heading("MODULE 8 — ANSIBLE DEPLOYMENT")
    add_p(
        "Ansible is used to automate the deployment and configuration of the Smart Parking Docker container. "
        "The deployment configuration is defined in the Ansible playbook.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Executes the deployment playbook.")
    add_bullet("Specifies the Docker container name.")
    add_bullet("Specifies the Docker image.")
    add_bullet("Configures application port mapping.")
    add_bullet("Configures persistent volume mounting.")
    add_bullet("Defines the container state.")
    add_bullet("Defines the restart policy.")
    add_bullet("Uses Docker to apply the specified configuration.")
    add_bullet("Automates container deployment.")
    add_bullet("Allows deployment to be triggered through Jenkins.")
    add_bullet("Provides a repeatable deployment configuration.")
    add_p("Deployment Configuration:\nname: smart-parking-ansible\nimage: smart-parking-ci\npublished_ports:\n - \"5001:5000\"\nvolumes:\n - \"parking_data:/app/data\"", font_size=10.5, space_before=4, space_after=8)

    add_img("fig_7_11_ansible.png", caption="Figure 7.11: Ansible Deployment Playbook")

    doc.add_page_break()

    # ================= MODULE 9 =================
    add_mod_heading("MODULE 9 — PERSISTENT STORAGE")
    add_p(
        "This module ensures that database information remains available even when the application container is "
        "recreated. Docker Volume is used to separate persistent application data from the container lifecycle.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Creates persistent storage for application data.")
    add_bullet("Uses the Docker Volume parking_data.")
    add_bullet("Mounts the volume to /app/data.")
    add_bullet("Stores the SQLite database in the mounted directory.")
    add_bullet("Separates persistent data from the container lifecycle.")
    add_bullet("Allows the database to remain available after container recreation.")
    add_bullet("Preserves stored reservation information.")
    add_bullet("Provides persistent storage for the SQLite database.")
    add_bullet("Allows the application container to be recreated without losing stored booking data.")
    add_p("Storage Configuration:\nparking_data:/app/data", font_size=10.5, space_before=4, space_after=8)

    add_img("fig_storage_flow.png", caption="Storage Flow – Smart Parking")
    add_img("fig_7_12_volume.png", caption="Figure 7.12: Parking Data Docker Volume")

    doc.add_page_break()

    # ================= MODULE 10 =================
    add_mod_heading("MODULE 10 — ADMIN & OCCUPANCY MANAGEMENT")
    add_p(
        "This module provides access to the reservations placed by users. The Flask backend stores the reservation information "
        "in SQLite, while the admin dashboard provides access to the stored records.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Receives reservations placed by users.")
    add_bullet("Processes reservation information through Flask.")
    add_bullet("Stores reservation information in SQLite.")
    add_bullet("Generates a reservation ID.")
    add_bullet("Makes stored reservations available to the administrator.")
    add_bullet("Provides access to reservation information through the admin dashboard.")
    add_bullet("Allows the administrator to view stored reservations.")
    add_bullet("Connects the application workflow with database records.")
    add_bullet("Provides a centralized view of placed reservations.")
    add_p("Admin Dashboard:\nhttp://localhost:5001/admin", font_size=10.5, space_before=4, space_after=8)

    add_img("fig_reservation_flow.png", caption="Reservation Flow – Smart Parking")
    add_img("fig_7_13_admin.png", caption="Figure 7.13: Smart Parking Admin Dashboard")

    doc.add_page_break()

    # ================= MODULE 11 & 12 =================
    add_mod_heading("MODULE 11 — CI/CD INTEGRATION")
    add_p(
        "This module integrates the different DevOps tools into a single automated workflow. GitHub, Jenkins, "
        "Docker, Pytest, and Ansible work together to automate the build, testing, and deployment process.",
        font_size=11, space_after=8
    )
    add_p("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Integrates GitHub with Jenkins.")
    add_bullet("Retrieves the latest project code.")
    add_bullet("Checks out the required project version.")
    add_bullet("Builds the Docker image automatically.")
    add_bullet("Runs Pytest automatically.")
    add_bullet("Triggers Ansible deployment after successful testing.")
    add_bullet("Creates and manages the Docker container.")
    add_bullet("Provides a repeatable deployment process.")
    add_bullet("Produces execution results for each pipeline stage.")
    add_bullet("Reduces repetitive manual deployment activities.")
    add_bullet("Connects source control, testing, containerization, and deployment into one workflow.")

    add_img("fig_7_14_pipeline_done.png", caption="Figure 7.14: Complete CI/CD Pipeline Execution")

    add_mod_heading("MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION")
    add_p(
        "This module verifies that the complete Smart Parking system is functioning correctly after deployment. "
        "Verification is performed across the application, Docker container, database, storage, Ansible deployment, "
        "and Jenkins pipeline.",
        font_size=11, space_after=8
    )
    add_p("Verification Activities", font_size=11, bold=True, space_after=4)
    add_bullet("Checking the running Docker container.")
    add_bullet("Checking the application port.")
    add_bullet("Opening the Smart Parking application.")
    add_bullet("Browsing available parking bays.")
    add_bullet("Placing a parking reservation.")
    add_bullet("Checking the generated reservation information.")
    add_bullet("Checking the admin dashboard.")
    add_bullet("Checking stored SQLite reservations.")
    add_bullet("Checking the Docker Volume.")
    add_bullet("Checking Ansible execution.")
    add_bullet("Checking Jenkins pipeline results.")
    add_bullet("Confirming successful application deployment.")
    add_bullet("Verifying that reservation data remains available after container recreation.")
    add_p("Important Outputs:\nDocker Build → SUCCESS\nPytest → 7 PASSED\nAnsible → failed=0\nPipeline → SUCCESS", font_size=10.5, space_before=4, space_after=8)

    add_img("fig_7_15_receipt.png", caption="Figure 7.15: Successfully Deployed Smart Parking Application")

    doc.add_page_break()

    # ================= 19. RESULTS AND OUTPUT =================
    add_sec_heading("19. RESULTS AND OUTPUT")
    add_p("The implemented system successfully provides:", font_size=11, space_after=6)
    add_bullet("Digital parking slot browsing")
    add_bullet("Slot search")
    add_bullet("Category-based selection")
    add_bullet("Reservation management")
    add_bullet("Reservation placement")
    add_bullet("Reservation ID generation")
    add_bullet("Admin dashboard")
    add_bullet("SQLite database storage")
    add_bullet("Docker containerization")
    add_bullet("Automated Pytest testing")
    add_bullet("Jenkins CI/CD automation")
    add_bullet("Ansible deployment")
    add_bullet("Persistent Docker Volume storage")

    add_sec_heading("COMMANDS USED")
    add_p("1. Docker Environment", font_size=11, bold=True, space_after=2)
    add_p("Check running containers\ndocker ps\n\nCheck all containers\ndocker ps -a\n\nStart Ansible container\ndocker start ansible-docker-lab\n\nStart Jenkins\ndocker start jenkins", font_size=10, space_after=6)

    add_p("2. Jenkins Commands", font_size=11, bold=True, space_after=2)
    add_p("Fix Docker socket permission for Jenkins\ndocker exec -u root jenkins chmod 666 /var/run/docker.sock\n\nVerify Jenkins can access Docker\ndocker exec jenkins docker info\n\nCheck Jenkins port\ndocker port jenkins\n\nJenkins was accessed using:\nhttp://localhost:9091", font_size=10, space_after=6)

    add_p("3. Docker Image Build", font_size=11, bold=True, space_after=2)
    add_p("Jenkins executes:\ndocker build -t smart-parking-ci .\n\nThis creates the Docker image:\nsmart-parking-ci", font_size=10, space_after=6)

    add_p("4. Automated Testing", font_size=11, bold=True, space_after=2)
    add_p("Jenkins executes:\ndocker run --rm smart-parking-ci python -m pytest test_app.py\n\nExpected result:\n7 passed", font_size=10, space_after=6)

    add_p("5. Ansible Deployment", font_size=11, bold=True, space_after=2)
    add_p("Jenkins executes:\ndocker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml\n\nThis runs the Ansible playbook.\n\nRun Ansible manually\ndocker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml\n\nView Ansible playbook\ndocker exec ansible-docker-lab cat /docker-deploy.yml", font_size=10, space_after=6)

    add_p("6. Docker Container Verification", font_size=11, bold=True, space_after=2)
    add_p("Check deployed container\ndocker ps\n\nThe Smart Parking container:\nsmart-parking-ansible\n\nPort mapping:\n5001:5000\n\nApplication:\nhttp://localhost:5001", font_size=10, space_after=6)

    add_p("7. Docker Volume Commands", font_size=11, bold=True, space_after=2)
    add_p("List Docker volumes\ndocker volume ls\n\nOur volume:\nparking_data\n\nInspect the volume\ndocker volume inspect parking_data", font_size=10, space_after=6)

    add_p("8. SQLite Database Commands", font_size=11, bold=True, space_after=2)
    add_p("Display stored slots\ndocker exec smart-parking-ansible python -c \"import sqlite3; c=sqlite3.connect('data/parking.db'); [print(row) for row in c.execute('SELECT * FROM slots')]; c.close()\"\n\nDisplay database tables\ndocker exec smart-parking-ansible python -c \"import sqlite3; c=sqlite3.connect('data/parking.db'); print(c.execute(\\\"SELECT name FROM sqlite_master WHERE type='table'\\\").fetchall()); c.close()\"\n\nDisplay all reservations as a list\ndocker exec smart-parking-ansible python -c \"import sqlite3; c=sqlite3.connect('data/parking.db'); print(c.execute('SELECT * FROM reservations').fetchall()); c.close()\"", font_size=10, space_after=6)

    add_p("9. Docker Volume + Database Verification", font_size=11, bold=True, space_after=2)
    add_p("To verify that the database exists inside the running container:\ndocker exec smart-parking-ansible python -c \"import sqlite3; c=sqlite3.connect('data/parking.db'); print(c.execute('SELECT * FROM reservations').fetchall()); c.close()\"\n\nThe database location is:\ndata/parking.db\nand inside the container:\n/app/data/parking.db", font_size=10, space_after=6)

    add_p("10. Git Commands Used", font_size=11, bold=True, space_after=2)
    add_p("Initialize Git\ngit init\nCheck status\ngit status\nAdd files\ngit add .\nCommit changes\ngit commit -m \"Finalize Smart Parking CI/CD project\"\nCheck branches\ngit branch\nConnect GitHub repository\ngit remote add origin https://github.com/71762307053/SmartParkingSystem.git\nPush to GitHub\ngit push -u origin master\nPull latest code\ngit pull origin master", font_size=10, space_after=6)

    add_p("11. Useful Docker Commands Used During Implementation", font_size=11, bold=True, space_after=2)
    add_p("List Docker images\ndocker images\nStop container\ndocker stop smart-parking-ansible\nStart container\ndocker start smart-parking-ansible\nView container logs\ndocker logs smart-parking-ansible\nExecute a command inside the container\ndocker exec smart-parking-ansible ...", font_size=10, space_after=6)

    add_p("12. Main Commands for Your Report", font_size=11, bold=True, space_after=2)
    add_p(
        "If your report doesn't need every troubleshooting command, these are the most important ones to include:\n\n"
        "docker build -t smart-parking-ci .\n"
        "docker run --rm smart-parking-ci python -m pytest test_app.py\n"
        "docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml\n"
        "docker ps\n"
        "docker volume ls\n"
        "docker volume inspect parking_data\n"
        "docker exec smart-parking-ansible python -c \"import sqlite3; c=sqlite3.connect('data/parking.db'); print(c.execute('SELECT * FROM reservations').fetchall()); c.close()\"\n\n"
        "And the Git commands:\n"
        "git add .\n"
        "git commit -m \"Finalize Smart Parking CI/CD project\"\n"
        "git push -u origin master",
        font_size=10, space_after=12
    )

    doc.add_page_break()

    # ================= 21-24: ADVANTAGES, LIMITATIONS, CONCLUSION =================
    add_sec_heading("21. ADVANTAGES")
    add_bullet("Reduces manual parking reservation effort.")
    add_bullet("Provides a user-friendly reservation interface.")
    add_bullet("Provides centralized parking slot and occupancy information.")
    add_bullet("Automates application testing.")
    add_bullet("Reduces manual deployment effort.")
    add_bullet("Provides consistent application execution through Docker.")
    add_bullet("Provides persistent database storage.")
    add_bullet("Integrates source control with CI/CD.")
    add_bullet("Demonstrates automated deployment using Ansible.")

    add_sec_heading("22. LIMITATIONS")
    add_bullet("The current system uses SQLite for database storage.")
    add_bullet("Online payment functionality is not implemented.")
    add_bullet("User authentication is not currently included.")
    add_bullet("Real-time physical vehicle sensor tracking is not implemented.")
    add_bullet("The deployment is demonstrated in a local Docker environment.")
    add_bullet("Monitoring and centralized logging are not implemented.")

    add_sec_heading("23. CONCLUSION")
    conc_txt = (
        "The Smart Parking Management System successfully demonstrates the integration of a web-based parking management system with "
        "modern DevOps practices to provide an efficient and automated application environment. The system "
        "enables users to browse available parking slots, search for bays, select slots, and place reservations through "
        "a simple and user-friendly interface. The admin dashboard provides a centralized platform for viewing and "
        "managing the reservations placed by users. Flask is used to handle the backend operations, while SQLite is used to "
        "store reservation information in the parking.db database. The project also demonstrates the complete "
        "implementation of a Continuous Integration and Continuous Deployment (CI/CD) workflow. Git and "
        "GitHub are used for version control and source code management, allowing the project files to be "
        "maintained in a centralized repository. Jenkins automates the CI/CD pipeline by retrieving the latest source "
        "code, building the Docker image, executing automated tests, and initiating the deployment process. Pytest is "
        "integrated into the pipeline to verify the application before deployment, helping ensure that the application "
        "passes the defined automated tests. Docker provides containerization for the Smart Parking application, "
        "allowing the Flask application and its required dependencies to run in a consistent environment. Ansible is "
        "used to automate the deployment and configuration of the Docker container through an Ansible playbook. "
        "The playbook defines important deployment configurations such as the container name, Docker image, port "
        "mapping, and volume mounting. A Docker Volume, parking_data, is used to provide persistent storage for "
        "the SQLite database. The volume is mounted to /app/data, ensuring that reservation information remains available "
        "even when the application container is recreated or updated. Overall, the project demonstrates how "
        "application development, version control, automated testing, containerization, deployment automation, and "
        "persistent storage can be integrated into a single DevOps workflow. The successful execution of the pipeline "
        "confirms the practical implementation of GitHub → Jenkins → Docker → Pytest → Ansible → Flask → "
        "SQLite, providing a complete automated approach to deploying and maintaining the Smart Parking system."
    )
    add_p(conc_txt, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14, line_spacing=1.2)

    add_sec_heading("24. FUTURE ENHANCEMENTS")
    add_p("The system can be extended with:", font_size=11, space_after=4)
    add_bullet("1. Online payment integration.")
    add_bullet("2. Driver and user authentication.")
    add_bullet("3. Real-time physical IoT bay tracking.")
    add_bullet("4. Reservation status notifications.")
    add_bullet("5. Parking bay availability management.")
    add_bullet("6. Multiple parking lot support.")
    add_bullet("7. Cloud deployment.")
    add_bullet("8. PostgreSQL or MySQL integration.")
    add_bullet("9. GitHub webhook-based automatic triggering.")
    add_bullet("10. Application monitoring and centralized logging.")

    # Save to Word Document
    final_output = "Smart_Parking_DevOps_Report_Final.docx"
    doc.save(final_output)
    print(f"[SUCCESS] Final Word Report saved with all embedded images and matched font size to: {final_output}")

if __name__ == "__main__":
    generate_report()
