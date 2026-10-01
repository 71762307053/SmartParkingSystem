import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_border(cell, **kwargs):
    """Set cell borders: top, bottom, left, right."""
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
        color=kwargs.get('color', 'CCCCCC')
    ))
    tcPr.append(tcBorders)

def set_cell_background(cell, fill_hex):
    """Set cell background color."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_report():
    doc = Document()

    # Page setup - Margins 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("23IT723 – DevOps Laboratory | Final Project")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(9)
        hrun.font.color.rgb = RGBColor(128, 128, 128)

    # Helper styling function
    def add_para(text, font_size=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size)
        run.bold = bold
        run.italic = italic
        return p

    def add_bullet(text, bold_prefix="", space_after=4):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = "Times New Roman"
            r_bold.font.size = Pt(11)
            r_bold.bold = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        return p

    def add_heading_1(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(title)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)
        run.bold = True
        return p

    def add_module_heading(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(title)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)
        run.bold = True
        return p

    def add_figure_box(fig_title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        
        # Frame table for screenshot placeholder
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(5.8)
        set_cell_background(cell, "F8F9FA")
        set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='6', color='B0BEC5')
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(28)
        cp.paragraph_format.space_after = Pt(28)
        crun = cp.add_run(f"[ Screenshot Placeholder: {fig_title} ]\n(Insert your application / pipeline screenshot here)")
        crun.font.name = "Times New Roman"
        crun.font.size = Pt(10)
        crun.font.italic = True
        crun.font.color.rgb = RGBColor(120, 144, 156)

        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_caption.paragraph_format.space_before = Pt(6)
        p_caption.paragraph_format.space_after = Pt(14)
        cap_run = p_caption.add_run(fig_title)
        cap_run.font.name = "Times New Roman"
        cap_run.font.size = Pt(11)
        cap_run.italic = False
        cap_run.bold = False

    def add_code_box(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.2)
        set_cell_background(cell, "1E1E1E")
        set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='333333')
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(6)
        cp.paragraph_format.space_after = Pt(6)
        crun = cp.add_run(code_text)
        crun.font.name = "Courier New"
        crun.font.size = Pt(9.5)
        crun.font.color.rgb = RGBColor(220, 220, 220)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ================= PAGE 1: TITLE PAGE =================
    add_para("COIMBATORE INSTITUTE OF TECHNOLOGY", font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=50, space_after=4)
    add_para("(Government Aided Autonomous Institution Affiliated to Anna University)", font_size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)
    
    add_para("23IT723 - DEVOPS LABORATORY", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    add_para("PROJECT", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    add_para("SMART PARKING MANAGEMENT SYSTEM", font_size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=60)
    
    add_para("OCTOBER 2026", font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=100)
    
    add_para("Submitted by", font_size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    add_para("71762307053   SUMMERJEET SINGH", font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=0)
    doc.add_page_break()

    # ================= PAGE 2: BONAFIDE CERTIFICATE =================
    add_para("COIMBATORE INSTITUTE OF TECHNOLOGY", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=4)
    add_para("(Government Aided Autonomous Institution Affiliated to Anna University)", font_size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    add_para("BONAFIDE CERTIFICATE", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)
    
    cert_text = (
        "Certified that this project report titled “SMART PARKING MANAGEMENT SYSTEM” is the "
        "bonafide work of 71762307053 - SUMMERJEET SINGH completed during the academic year "
        "2025-2026-Semester VII for the project presentation of 23IT723 - DEVOPS LABORATORY under our supervision."
    )
    p_cert = add_para(cert_text, font_size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=30, line_spacing=1.3)
    
    add_para("Certified that the candidate was examined by using the project work examination.", font_size=12, italic=True, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=40)
    
    add_para("Review Members:", font_size=12, bold=True, space_after=14)
    add_para("1.   Dr.M.Sangeetha", font_size=12, bold=True, space_after=8)
    add_para("2.   Dr.E.Arul", font_size=12, bold=True, space_after=0)
    doc.add_page_break()

    # ================= PAGE 3: EVALUATION SCHEME =================
    add_para("23IT723 – DEVOPS LABORATORY", font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)
    add_para("FINAL MINI PROJECT – EVALUATION SCHEME", font_size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    add_para("Final Mini Project Assessment", font_size=11, bold=True, space_after=4)
    add_para(
        "The final mini project shall require students to integrate the major DevOps practices covered in the laboratory. "
        "The project should demonstrate practical implementation of version control, collaborative development, Continuous "
        "Integration, containerization and/or automated configuration/provisioning, with proper execution evidence.",
        font_size=10, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10
    )

    eval_data = [
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

    tbl_eval = doc.add_table(rows=len(eval_data), cols=4)
    tbl_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths = [Inches(0.6), Inches(1.8), Inches(3.2), Inches(0.8)]

    for row_idx, row_data in enumerate(eval_data):
        for col_idx, text in enumerate(row_data):
            cell = tbl_eval.cell(row_idx, col_idx)
            cell.width = col_widths[col_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(3)
            cp.paragraph_format.space_after = Pt(3)
            cp.paragraph_format.line_spacing = 1.05
            is_header = (row_idx == 0)
            is_total = (row_idx == len(eval_data) - 1)
            
            run = cp.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if is_header or is_total:
                run.bold = True
                set_cell_background(cell, "F2F2F2")
            if col_idx in [0, 3]:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    doc.add_page_break()

    # ================= PAGE 4: DEMONSTRATION & GUIDELINES =================
    add_para("Recommended Mark Distribution within the Final Demonstration", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
    add_para("For uniform evaluation, the examiner may use the following internal split for the implementation and demonstration components.", font_size=10, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=8)

    demo_data = [
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

    tbl_demo = doc.add_table(rows=len(demo_data), cols=4)
    tbl_demo.alignment = WD_TABLE_ALIGNMENT.CENTER
    demo_col_widths = [Inches(2.6), Inches(0.8), Inches(1.3), Inches(1.7)]

    for row_idx, row_data in enumerate(demo_data):
        for col_idx, text in enumerate(row_data):
            cell = tbl_demo.cell(row_idx, col_idx)
            cell.width = demo_col_widths[col_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(2.5)
            cp.paragraph_format.space_after = Pt(2.5)
            run = cp.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if row_idx == 0 or row_idx == len(demo_data) - 1:
                run.bold = True
                set_cell_background(cell, "F2F2F2")
            if col_idx in [1, 2]:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    add_para("Minimum Evidence to be Submitted", font_size=11, bold=True, space_before=10, space_after=4)
    add_bullet("Project repository URL and project README.")
    add_bullet("Git commit history and branch/merge evidence.")
    add_bullet("Jenkins job/pipeline configuration and successful build evidence.")
    add_bullet("Dockerfile, image and running container evidence where Docker is used.")
    add_bullet("Automation/configuration scripts where applicable.")
    add_bullet("Application execution and testing evidence.")
    add_bullet("Architecture/workflow diagram.")
    add_bullet("Short technical report containing implementation steps, results and troubleshooting.")
    add_bullet("Live demonstration of the complete DevOps workflow.")

    add_para("Evaluation Guidelines", font_size=11, bold=True, space_before=8, space_after=4)
    add_bullet("Marks shall be awarded primarily for a working implementation and demonstrable output.")
    add_bullet("Copied source code without functional understanding shall not receive full marks.")
    add_bullet("Screenshots may support the evaluation, but critical components should be demonstrated live wherever possible.")
    add_bullet("Students should use meaningful repository names, branch names and commit messages.")
    add_bullet("If a component is not applicable to the selected project, the student shall obtain faculty approval and demonstrate an equivalent DevOps automation component.")
    add_bullet("The final viva shall focus on the student's own implementation, commands used, tool configuration and troubleshooting.")

    add_para("Faculty Evaluation Record", font_size=11, bold=True, space_before=10, space_after=4)
    tbl_fac = doc.add_table(rows=4, cols=4)
    tbl_fac.alignment = WD_TABLE_ALIGNMENT.CENTER
    fac_widths = [Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.6)]
    fac_cells = [
        [("Student Name", True), ("SUMMERJEET SINGH", False), ("Register No.", True), ("71762307053", False)],
        [("Project Title", True), ("Smart Parking System", False), ("Date", True), ("02-10-2026", False)],
        [("Final Mark", True), ("", False), ("", False), ("", False)],
        [("Faculty Evaluator I", True), ("", False), ("Signature", True), ("", False)],
    ]
    for r_idx, row in enumerate(fac_cells):
        for c_idx, (txt, is_b) in enumerate(row):
            cell = tbl_fac.cell(r_idx, c_idx)
            cell.width = fac_widths[c_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(3)
            cp.paragraph_format.space_after = Pt(3)
            run = cp.add_run(txt)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            run.bold = is_b
            if is_b:
                set_cell_background(cell, "F9F9F9")
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    doc.add_page_break()

    # ================= PAGES 5-6: TABLE OF CONTENTS =================
    add_para("TABLE OF CONTENTS", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=14)

    toc_data = [
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

    tbl_toc = doc.add_table(rows=len(toc_data), cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_widths = [Inches(0.8), Inches(4.5), Inches(1.1)]

    for row_idx, row_data in enumerate(toc_data):
        for col_idx, text in enumerate(row_data):
            cell = tbl_toc.cell(row_idx, col_idx)
            cell.width = toc_widths[col_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(3.5)
            cp.paragraph_format.space_after = Pt(3.5)
            run = cp.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if row_idx == 0:
                run.bold = True
                set_cell_background(cell, "F2F2F2")
            if col_idx in [0, 2]:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    doc.add_page_break()

    # ================= PAGE 7: INTRODUCTION & OBJECTIVES =================
    add_heading_1("1. INTRODUCTION")
    intro_p1 = (
        "The Smart Parking Management System is a web-based vehicle parking space reservation and management system "
        "developed to simplify the process of locating, reserving, and tracking parking slots in crowded campus, commercial, "
        "or municipal environments. The system allows users to browse available parking slots across different vehicle zones "
        "(Cars, Bikes, and Electric Vehicles), check hourly tariffs, select a vacant bay, and instantly place reservations "
        "through an intuitive digital interface. An administrative dashboard is also provided to view and manage parking lot "
        "occupancy, force-release slots, and monitor booking revenue. The application is developed using HTML, CSS, JavaScript, "
        "Python, Flask, and SQLite, with Flask handling backend REST API operations and SQLite storing persistent slot states "
        "and reservation logs. The project also incorporates DevOps practices to automate the development, testing, and "
        "deployment process. Git and GitHub are used for source code management, while Jenkins automates the multi-stage CI/CD "
        "pipeline. Docker provides application containerization, Pytest performs automated testing, and Ansible automates "
        "deployment and container configuration. A Docker Volume named parking_data is used to provide persistent storage "
        "for the SQLite database. The project combines a functional parking reservation system with DevOps automation to provide "
        "a structured, repeatable, and reliable approach to application lifecycle management."
    )
    add_para(intro_p1, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14, line_spacing=1.2)

    add_heading_1("2. OBJECTIVES")
    add_bullet("To develop a smart parking reservation system that enables drivers to browse, filter, select available bays, and reserve parking spots conveniently.")
    add_bullet("To implement an admin dashboard for viewing real-time slot occupancy, total revenue, and maintaining parking logs using SQLite.")
    add_bullet("To organize slot data systematically by zones (Four Wheeler, Two Wheeler, EV Charging) and provide rapid manual override through the admin interface.")
    add_bullet("To implement DevOps practices throughout the application development and deployment lifecycle using Git, GitHub, and Jenkins.")
    add_bullet("To automate the CI/CD workflow using Jenkins for building, testing, and deploying the application.")
    add_bullet("To containerize the application using Docker to provide a consistent and portable execution environment.")
    add_bullet("To integrate Pytest for automated testing to verify slot reservation and release endpoints before deployment.")
    add_bullet("To automate application deployment and container configuration using Ansible playbooks.")
    add_bullet("To implement Docker Volume for persistent storage of the SQLite database and ensure that booking data is retained even when the container is recreated.")
    doc.add_page_break()

    # ================= PAGE 8: ABSTRACT & TECH STACK =================
    add_heading_1("3. ABSTRACT")
    abstract_text = (
        "The Smart Parking Management System is a web-based parking management system designed to eliminate manual ticketing "
        "and reduce search delays in urban parking lots. Traditional parking operations involve manual register logs, entry delays, "
        "inefficient slot tracking, and difficulties in monitoring facility occupancy. The proposed system provides a digital platform "
        "where drivers can check available bays in real time, reserve bays with contact details, and obtain digital tokens. An "
        "administrative dashboard is also provided for monitoring capacity, revenue, and active bookings. The application is developed "
        "using HTML, CSS, JavaScript, Python, Flask, and SQLite. The project implements end-to-end DevOps automation practices. "
        "Git and GitHub are used for version control, while Jenkins automates the CI/CD pipeline. Docker containerizes the application "
        "into an isolated image, Pytest performs automated functional testing, and Ansible automates container configuration and "
        "deployment. A Docker Volume named parking_data provides persistent storage for the SQLite database, ensuring that stored "
        "records remain intact across container updates. The complete workflow follows GitHub → Jenkins → Docker Build → Pytest → "
        "Ansible → Docker Container → Flask → SQLite, demonstrating the integration of a functional web application with modern DevOps practices."
    )
    add_para(abstract_text, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14, line_spacing=1.2)

    add_heading_1("4. TECHNOLOGY STACK")
    tech_data = [
        ("Technology", "Version", "Purpose"),
        ("HTML", "HTML5", "Web page structure"),
        ("CSS", "CSS3", "User interface styling & responsive layout"),
        ("JavaScript", "ES6+", "Frontend interaction & AJAX requests"),
        ("Python", "3.11", "Backend programming & API logic"),
        ("Flask", "3.0.x", "Backend web framework"),
        ("SQLite", "3.x", "Database management"),
        ("Git", "2.x", "Version control & source code management"),
        ("GitHub", "—", "Remote centralized source code repository"),
        ("Jenkins", "2.x / LTS", "Continuous Integration & Deployment automation"),
        ("Docker", "26.x+ / 28.x+", "Application containerization"),
        ("Pytest", "8.x", "Automated unit and integration testing"),
        ("Ansible", "2.10+", "Deployment & container configuration automation"),
        ("Docker SDK / Community Docker", "community.docker 1.2+", "Docker management through Ansible"),
        ("Docker Volume", "parking_data", "Persistent storage mounted to /app/data")
    ]

    tbl_tech = doc.add_table(rows=len(tech_data), cols=3)
    tbl_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_col_w = [Inches(2.2), Inches(1.8), Inches(2.4)]
    for r_idx, r_data in enumerate(tech_data):
        for c_idx, txt in enumerate(r_data):
            cell = tbl_tech.cell(r_idx, c_idx)
            cell.width = t_col_w[c_idx]
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(3)
            cp.paragraph_format.space_after = Pt(3)
            run = cp.add_run(txt)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.bold = True
                set_cell_background(cell, "F2F2F2")
            set_cell_border(cell, top='single', bottom='single', left='single', right='single', sz='4', color='444444')

    doc.add_page_break()

    # ================= PAGE 9: SYSTEM ARCHITECTURE =================
    add_heading_1("5. SYSTEM ARCHITECTURE")
    add_figure_box("Figure 7.0: Smart Parking Management System – Architecture Diagram")
    
    arch_steps = [
        "1. Development: Developer creates and updates the Smart Parking application source code and tests.",
        "2. Source Code Management: The application source code and configuration files are maintained using Git.",
        "3. GitHub Repository: The updated code is pushed to the GitHub repository for centralized source code management.",
        "4. Jenkins Trigger: Jenkins retrieves the latest source code from the GitHub repository and starts the CI/CD pipeline.",
        "5. Docker Build: Jenkins builds the application into a Docker image containing the Flask application and required dependencies.",
        "6. Automated Testing: Jenkins runs Pytest inside the container image to verify the application before deployment.",
        "7. Deployment Automation: After successful testing, Jenkins invokes Ansible to automate the deployment process.",
        "8. Container Configuration: Ansible creates and configures the Docker container with the required image, port mapping, restart policy, and volume configuration.",
        "9. Application Execution: The Docker container runs the Flask backend, HTML/CSS/JavaScript frontend, and SQLite database.",
        "10. User Interaction: Drivers can view bay availability, select preferred bays, reserve slots, and release spaces upon exit.",
        "11. Admin Management: The admin dashboard allows facility supervisors to monitor occupancy and view records stored in the database."
    ]
    for step in arch_steps:
        add_para(step, font_size=10.5, space_after=4, line_spacing=1.15)

    doc.add_page_break()

    # ================= MODULE 1 =================
    add_module_heading("MODULE 1 — USER INTERFACE & PARKING SLOT DISPLAY")
    add_para(
        "This module provides the user-facing interface of the Smart Parking application. It is designed to make "
        "parking slot discovery, reservation, and checkout intuitive, visual, and fast for vehicle drivers.",
        font_size=11, space_after=8
    )
    add_para("Main Features", font_size=11, bold=True, space_after=4)
    add_bullet("Displays available parking bays with real-time status indicators (Available, Reserved, Occupied).")
    add_bullet("Provides a search option to locate parking bays quickly by slot code.")
    add_bullet("Organizes parking bays into distinct zones: Zone A (Cars), Zone B (Bikes), Zone C (EV Fast-Charging).")
    add_bullet("Allows users to select individual vacant bays directly on an interactive matrix.")
    add_bullet("Includes a reservation modal with driver details, vehicle registration, and expected parking duration.")
    add_bullet("Dynamic cost estimation based on hourly tariffs (Car: ₹30/hr, Bike: ₹15/hr, EV: ₹45/hr).")
    add_bullet("Generates instant digital parking passes with unique codes (e.g. PKG-1001).")
    add_bullet("Provides a Quick Release modal for drivers to release slots and generate billing receipts.")
    add_bullet("Responsive dark-theme user interface elements for desktop and mobile devices.")
    add_bullet("Connects the user interface with the Flask backend via asynchronous REST API calls.")
    add_para("Technologies: HTML5, CSS3, JavaScript (ES6+).", font_size=10.5, italic=True, space_before=4, space_after=12)

    add_figure_box("Figure 7.1: Smart Parking Home Page")
    add_figure_box("Figure 7.2: Parking Slot Selection and Reservation")

    doc.add_page_break()

    # ================= MODULE 2 =================
    add_module_heading("MODULE 2 — FLASK BACKEND & RESERVATION MANAGEMENT")
    add_para(
        "This module handles the application logic and acts as the communication layer between the frontend and "
        "the SQLite database. Flask processes user requests, calculates tariffs, and manages the complete reservation lifecycle.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Receives HTTP and JSON requests from the frontend interface.")
    add_bullet("Processes slot reservation requests and validates driver input.")
    add_bullet("Computes parking fees dynamically based on duration and vehicle category.")
    add_bullet("Generates unique reservation codes (e.g. PKG-1001) and records entry timestamps.")
    add_bullet("Handles checkout requests, calculates final durations, and releases bays back to available.")
    add_bullet("Communicates with the SQLite database to store and retrieve bay states and booking records.")
    add_bullet("Supplies JSON API endpoints (/api/slots, /api/reserve, /api/release, /api/stats).")
    add_bullet("Handles administrative dashboard routes and manual override requests.")
    add_bullet("Runs the Flask WSGI application on port 5000 inside the Docker container.")
    add_para("Technology: Python with Flask.", font_size=10.5, italic=True, space_before=4, space_after=8)

    add_figure_box("Figure 7.3: Flask Backend Implementation")

    doc.add_page_break()

    # ================= MODULE 3 =================
    add_module_heading("MODULE 3 — SQLITE DATABASE MANAGEMENT")
    add_para(
        "This module manages the storage and retrieval of parking bay states and vehicle transaction history using SQLite. "
        "The database provides persistent application state accessible by the Flask backend.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Stores configured parking bays (slot_number, zone, vehicle_type, status, hourly_rate).")
    add_bullet("Maintains reservation records (reservation_code, vehicle_number, driver_name, entry_time, exit_time, total_amount).")
    add_bullet("Provides database access to the Flask backend using Python's sqlite3 library.")
    add_bullet("Allows active and completed reservations to be queried and retrieved by the admin dashboard.")
    add_bullet("Maintains the parking.db database file under the persistent data directory.")
    add_bullet("Works with the Docker Volume for persistent storage across container lifecycles.")
    add_bullet("Preserves slot occupancy and revenue records even when the application container is recreated.")
    add_para("Database Location:\ndata/parking.db\nInside the Docker container:\n/app/data/parking.db", font_size=10.5, space_before=4, space_after=6)
    add_para("Technology: SQLite.", font_size=10.5, italic=True, space_after=8)

    add_figure_box("Figure 7.4: SQLite Database Containing Slot and Reservation Information")

    doc.add_page_break()

    # ================= MODULE 4 =================
    add_module_heading("MODULE 4 — GIT & GITHUB SOURCE CONTROL")
    add_para(
        "This module manages the source code and maintains the development history of the Smart Parking project. "
        "Git is used locally for version control, while GitHub provides the remote centralized repository.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Initializes the project as a Git repository.")
    add_bullet("Tracks changes made to source code, templates, tests, and configuration files.")
    add_bullet("Creates meaningful commits tracking features, automated tests, and CI/CD pipelines.")
    add_bullet("Maintains branches (master, feature branches) for structured collaboration.")
    add_bullet("Pushes project code to GitHub repository (https://github.com/71762307053/SmartParkingSystem.git).")
    add_bullet("Allows Jenkins to automatically poll and retrieve the latest source code.")
    add_bullet("Maintains important project files in one repository.")
    add_para("Main Project Files:\napp.py, Dockerfile, Jenkinsfile, test_app.py, docker-deploy.yml, inventory.ini, requirements.txt, .gitignore", font_size=10.5, space_before=4, space_after=6)
    add_para("Technologies: Git and GitHub.", font_size=10.5, italic=True, space_after=8)

    add_figure_box("Figure 7.5: Smart Parking GitHub Repository")

    doc.add_page_break()

    # ================= MODULE 5 =================
    add_module_heading("MODULE 5 — DOCKER CONTAINERIZATION")
    add_para(
        "Docker is used to package and run the Smart Parking application in an isolated and consistent environment. "
        "The application and its required dependencies are packaged into a portable Docker image.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Creates a Docker image from the application using a standardized Dockerfile.")
    add_bullet("Packages Python 3.11-slim, Flask, Pytest, SQLite, and application dependencies.")
    add_bullet("Provides an isolated execution environment independent of host OS variations.")
    add_bullet("Creates the application container smart-parking-ansible from the image smart-parking-ci.")
    add_bullet("Configures host port mapping 5001:5000 for web access.")
    add_bullet("Integrates with Jenkins for automated image builds upon code commits.")
    add_bullet("Integrates with Ansible for automated container provisioning.")
    add_para("Docker Configuration:\nDocker Image: smart-parking-ci\nDocker Container: smart-parking-ansible\nPort Mapping: 5001 → 5000\nApplication Access: http://localhost:5001", font_size=10.5, space_before=4, space_after=8)

    add_figure_box("Figure 7.6: Smart Parking Docker Image")
    add_figure_box("Figure 7.7: Running Smart Parking Docker Container")

    doc.add_page_break()

    # ================= MODULE 6 =================
    add_module_heading("MODULE 6 — JENKINS CI/CD PIPELINE")
    add_para(
        "Jenkins is used to automate the Continuous Integration and Continuous Deployment process. It connects the "
        "source code repository with the application build, automated testing, and deployment stages.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Retrieves the latest source code from the GitHub repository automatically.")
    add_bullet("Executes the declarative multi-stage Jenkinsfile pipeline.")
    add_bullet("Builds the Docker container image smart-parking-ci.")
    add_bullet("Executes automated Pytest test suite inside the container environment.")
    add_bullet("Halts deployment immediately if any automated test fails.")
    add_bullet("Invokes Ansible playbook deployment upon successful test completion.")
    add_bullet("Provides detailed pipeline execution stage view and console verification logs.")
    add_bullet("Eliminates manual build, test, and release errors.")

    add_figure_box("Figure 7.8: Jenkins CI/CD Pipeline Stage View")
    add_figure_box("Figure 7.9: Successful Jenkins Pipeline Execution")

    doc.add_page_break()

    # ================= MODULE 7 =================
    add_module_heading("MODULE 7 — AUTOMATED TESTING")
    add_para(
        "This module validates application correctness automatically before deployment. Pytest is integrated into "
        "the Jenkins pipeline so that all functional test cases are verified before the deployment stage executes.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Uses Pytest for automated unit and integration testing.")
    add_bullet("Maintains the test suite file test_app.py covering 7 verification scenarios.")
    add_bullet("Executes tests directly inside the Docker container image (docker run --rm smart-parking-ci python -m pytest test_app.py).")
    add_bullet("Validates homepage availability, admin dashboard responses, and slots listing JSON format.")
    add_bullet("Simulates end-to-end booking, bay state transition (available → reserved → available), and fee calculation.")
    add_bullet("Verifies error handling for invalid bay reservations and non-existent ticket release requests.")
    add_bullet("Displays granular test execution logs inside Jenkins console output.")
    add_para("Test File: test_app.py\nTest Command: python -m pytest test_app.py\nTest Result: 7 passed in 0.40s [100%]", font_size=10.5, space_before=4, space_after=8)

    add_figure_box("Figure 7.10: Successful Automated Test Execution")

    doc.add_page_break()

    # ================= MODULE 8 =================
    add_module_heading("MODULE 8 — ANSIBLE DEPLOYMENT")
    add_para(
        "Ansible is used to automate the deployment and configuration of the Smart Parking Docker container. "
        "The deployment configuration is declaratively defined in the Ansible playbook.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Executes the deployment playbook docker-deploy.yml.")
    add_bullet("Specifies the Docker container name smart-parking-ansible.")
    add_bullet("Specifies the Docker image smart-parking-ci.")
    add_bullet("Configures application port publishing (5001:5000).")
    add_bullet("Configures persistent volume mounting (parking_data:/app/data).")
    add_bullet("Sets the restart policy to unless-stopped.")
    add_bullet("Uses community.docker Ansible collection to apply the desired state idempotently.")
    add_bullet("Allows automated deployment to be triggered seamlessly through Jenkins.")

    add_code_box(
        "---\n"
        "- hosts: dockerhost\n"
        "  gather_facts: false\n"
        "  tasks:\n"
        "    - name: Manage Smart Parking Container\n"
        "      community.docker.docker_container:\n"
        "        name: smart-parking-ansible\n"
        "        image: smart-parking-ci\n"
        "        state: \"{{ container_state | default('started') }}\"\n"
        "        restart_policy: unless-stopped\n"
        "        published_ports:\n"
        "          - \"5001:5000\"\n"
        "        volumes:\n"
        "          - \"parking_data:/app/data\""
    )

    add_figure_box("Figure 7.11: Ansible Deployment Playbook")

    doc.add_page_break()

    # ================= MODULE 9 =================
    add_module_heading("MODULE 9 — PERSISTENT STORAGE")
    add_para(
        "This module ensures that database records remain available even when the application container is stopped, "
        "recreated, or upgraded. A Docker Volume is used to decouple persistent database state from the container lifecycle.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Creates persistent storage for application data using Docker Volume parking_data.")
    add_bullet("Mounts the volume to /app/data inside the running container.")
    add_bullet("Stores the SQLite database parking.db in the mounted directory.")
    add_bullet("Separates persistent data storage from the container execution lifecycle.")
    add_bullet("Allows the database to remain intact after container recreation or host restart.")
    add_bullet("Preserves bay states, vehicle registration numbers, timestamps, and revenue logs.")
    add_para("Storage Configuration:\nparking_data:/app/data", font_size=10.5, space_before=4, space_after=8)

    add_figure_box("Figure 7.12: Parking Data Docker Volume")

    doc.add_page_break()

    # ================= MODULE 10 =================
    add_module_heading("MODULE 10 — ADMIN & OCCUPANCY MANAGEMENT")
    add_para(
        "This module provides parking facility supervisors with complete visibility and administrative control over lot "
        "utilization. The Flask backend stores transactions in SQLite, while the admin dashboard renders live metrics.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Renders real-time KPI cards: Total Bay Capacity, Available Bays, Occupied/Reserved Bays, Total Revenue.")
    add_bullet("Displays live Bay Status Matrix with color-coded status badges for all 24 slots.")
    add_bullet("Provides instant manual force-release buttons allowing supervisors to clear occupied bays.")
    add_bullet("Maintains a searchable transaction table listing ticket codes, vehicle plates, driver details, and timestamps.")
    add_bullet("Includes a master system reset function to restore test environments to default seeds.")
    add_bullet("Admin Dashboard URL: http://localhost:5001/admin", space_after=8)

    add_figure_box("Figure 7.13: Smart Parking Admin Dashboard")

    doc.add_page_break()

    # ================= MODULE 11 & 12 =================
    add_module_heading("MODULE 11 — CI/CD INTEGRATION")
    add_para(
        "This module integrates the different DevOps tools into a single automated pipeline. GitHub, Jenkins, Docker, "
        "Pytest, and Ansible work in unison to automate the build, test, and release process.",
        font_size=11, space_after=8
    )
    add_para("Main Functions", font_size=11, bold=True, space_after=4)
    add_bullet("Integrates GitHub webhook and SCM polling with Jenkins.")
    add_bullet("Automatically checks out source code upon new commits.")
    add_bullet("Builds the Docker container image automatically without manual terminal commands.")
    add_bullet("Runs the 7-case Pytest automated test suite inside Docker.")
    add_bullet("Triggers Ansible playbook deployment only after all tests pass.")
    add_bullet("Provides repeatable, reliable deployment execution results for each pipeline stage.")

    add_figure_box("Figure 7.14: Complete CI/CD Pipeline Execution")

    add_module_heading("MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION")
    add_para(
        "This module verifies that the complete Smart Parking system is functioning correctly after deployment. "
        "Verification is performed across the web application, Docker container, database, and CI/CD pipeline.",
        font_size=11, space_after=8
    )
    add_bullet("Checking running Docker container smart-parking-ansible via docker ps.")
    add_bullet("Checking application port availability on port 5001.")
    add_bullet("Opening the user interface at http://localhost:5001 and reserving bay A-02.")
    add_bullet("Verifying bay A-02 transitions from Available to Reserved.")
    add_bullet("Checking admin dashboard at http://localhost:5001/admin for updated occupancy count and revenue.")
    add_bullet("Releasing bay A-02 and confirming return to Available status.")
    add_bullet("Verifying persistent SQLite storage inside container using docker exec.")
    add_para("Important Outputs:\nDocker Build → SUCCESS\nPytest → 7 PASSED (100%)\nAnsible → failed=0\nPipeline → SUCCESS", font_size=10.5, space_before=4, space_after=8)

    add_figure_box("Figure 7.15: Successfully Deployed Smart Parking Application")

    doc.add_page_break()

    # ================= 19. RESULTS AND OUTPUT =================
    add_heading_1("19. RESULTS AND OUTPUT")
    add_para("The implemented Smart Parking Management System successfully provides:", font_size=11, space_after=6)
    add_bullet("Real-time visual display of parking bays across 3 vehicle categories.")
    add_bullet("Category-based filtering and instant search for bays.")
    add_bullet("Rapid parking bay reservation with vehicle details.")
    add_bullet("Automated parking pass generation (PKG-XXXX).")
    add_bullet("Interactive duration slider with live cost preview.")
    add_bullet("One-click parking bay release and exit receipt billing.")
    add_bullet("Administrative dashboard for occupancy and revenue tracking.")
    add_bullet("Persistent SQLite database storage backed by Docker Volumes.")
    add_bullet("Automated Docker containerization with Python 3.11-slim.")
    add_bullet("Automated Pytest testing (7 test cases passed with 100% pass rate).")
    add_bullet("Automated Jenkins multi-stage CI/CD pipeline.")
    add_bullet("Ansible playbook deployment with zero errors (failed=0).")

    add_heading_1("COMMANDS USED")
    add_para("1. Docker Environment", font_size=11, bold=True, space_after=2)
    add_para("Check running containers:\ndocker ps\nCheck all containers:\ndocker ps -a\nStart Ansible container:\ndocker start ansible-docker-lab\nStart Jenkins:\ndocker start jenkins", font_size=10, space_after=6)

    add_para("2. Jenkins Commands", font_size=11, bold=True, space_after=2)
    add_para("Fix Docker socket permission for Jenkins:\ndocker exec -u root jenkins chmod 666 /var/run/docker.sock\nVerify Jenkins can access Docker:\ndocker exec jenkins docker info\nJenkins URL: http://localhost:9091", font_size=10, space_after=6)

    add_para("3. Docker Image Build", font_size=11, bold=True, space_after=2)
    add_para("Jenkins executes:\ndocker build -t smart-parking-ci .\nCreates Docker image: smart-parking-ci", font_size=10, space_after=6)

    add_para("4. Automated Testing", font_size=11, bold=True, space_after=2)
    add_para("Jenkins executes:\ndocker run --rm smart-parking-ci python -m pytest test_app.py\nExpected result: 7 passed in 0.40s", font_size=10, space_after=6)

    add_para("5. Ansible Deployment", font_size=11, bold=True, space_after=2)
    add_para("Jenkins executes:\ndocker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml\nView Ansible playbook:\ndocker exec ansible-docker-lab cat /docker-deploy.yml", font_size=10, space_after=6)

    add_para("6. Docker Container Verification", font_size=11, bold=True, space_after=2)
    add_para("Check deployed container:\ndocker ps\nContainer: smart-parking-ansible\nPort mapping: 5001:5000\nApplication URL: http://localhost:5001", font_size=10, space_after=6)

    add_para("7. Docker Volume Commands", font_size=11, bold=True, space_after=2)
    add_para("List Docker volumes:\ndocker volume ls\nInspect volume:\ndocker volume inspect parking_data", font_size=10, space_after=6)

    add_para("8. SQLite Database Commands", font_size=11, bold=True, space_after=2)
    add_para("Display stored slots:\ndocker exec smart-parking-ansible python -c \"import sqlite3; c=sqlite3.connect('data/parking.db'); print(c.execute('SELECT slot_number, status, hourly_rate FROM slots LIMIT 5').fetchall()); c.close()\"", font_size=10, space_after=6)

    add_para("9. Git Commands Used", font_size=11, bold=True, space_after=2)
    add_para("git init\ngit status\ngit add .\ngit commit -m \"Finalize Smart Parking CI/CD project\"\ngit branch -M master\ngit remote add origin https://github.com/71762307053/SmartParkingSystem.git\ngit push -u origin master", font_size=10, space_after=6)

    doc.add_page_break()

    # ================= 21-24: ADVANTAGES, LIMITATIONS, CONCLUSION =================
    add_heading_1("21. ADVANTAGES")
    add_bullet("Reduces manual parking allocation effort and paperwork.")
    add_bullet("Provides real-time visibility into parking bay availability.")
    add_bullet("Minimizes driver searching time and campus traffic congestion.")
    add_bullet("Automates application testing before any release using Pytest.")
    add_bullet("Reduces manual deployment effort via Ansible playbooks.")
    add_bullet("Provides consistent application execution through Docker containers.")
    add_bullet("Ensures persistent database storage across container lifecycles via Docker Volumes.")
    add_bullet("Integrates source control, automated build, and deployment into an automated CI/CD pipeline.")

    add_heading_1("22. LIMITATIONS")
    add_bullet("The current system uses SQLite database storage optimized for single-host deployments.")
    add_bullet("Live online payment gateway integration (UPI / Credit Card) is not currently implemented.")
    add_bullet("User authentication and role-based login are not included.")
    add_bullet("Physical IoT sensor integration (ultrasonic/RFID bay hardware) is simulated via web UI.")
    add_bullet("The deployment is demonstrated within a local Docker environment rather than cloud Kubernetes.")

    add_heading_1("23. CONCLUSION")
    conclusion_text = (
        "The Smart Parking Management System successfully demonstrates the integration of a web-based vehicle parking "
        "management platform with modern DevOps practices to provide an efficient, repeatable, and automated execution "
        "environment. The system enables users to browse available parking slots across zones, reserve spaces, and receive "
        "digital receipts through a responsive interface. The admin dashboard provides a centralized platform for monitoring "
        "occupancy and revenue. Flask handles backend operations, while SQLite stores persistent data in the parking.db database. "
        "The project demonstrates the complete implementation of a Continuous Integration and Continuous Deployment (CI/CD) "
        "workflow. Git and GitHub manage source code history. Jenkins automates the pipeline by pulling code, building Docker images, "
        "executing automated Pytest test cases, and initiating Ansible deployment. Docker provides containerization for consistent "
        "runtime execution, while Ansible automates container provisioning. A Docker Volume, parking_data, guarantees data persistence. "
        "The successful execution confirms the practical realization of GitHub → Jenkins → Docker → Pytest → Ansible → Flask → SQLite, "
        "providing a comprehensive automated approach to developing and maintaining the Smart Parking system."
    )
    add_para(conclusion_text, font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14, line_spacing=1.2)

    add_heading_1("24. FUTURE ENHANCEMENTS")
    add_para("The system can be extended with:", font_size=11, space_after=4)
    add_bullet("1. Online payment gateway integration (UPI, Razorpay, Stripe).")
    add_bullet("2. Driver and security guard authentication.")
    add_bullet("3. Hardware IoT sensor integration (Ultrasonic bay sensors and RFID barrier gates).")
    add_bullet("4. Automated Number Plate Recognition (ANPR) using computer vision.")
    add_bullet("5. SMS and email booking notifications.")
    add_bullet("6. Multi-level and multi-location parking facility support.")
    add_bullet("7. Cloud deployment on AWS / Azure / GCP.")
    add_bullet("8. PostgreSQL or MySQL database migration.")
    add_bullet("9. GitHub webhook-based automated pipeline triggering.")
    add_bullet("10. Centralized application monitoring and Prometheus / Grafana logging.")

    # Save Word document
    output_path = "Smart_Parking_Management_System_DevOps_Report.docx"
    doc.save(output_path)
    print(f"Document saved successfully to {output_path}")

if __name__ == "__main__":
    create_report()
