# COIMBATORE INSTITUTE OF TECHNOLOGY
*(Government Aided Autonomous Institution Affiliated to Anna University)*
### 23IT723 - DEVOPS LABORATORY
### FINAL MINI PROJECT REPORT

# SMART PARKING MANAGEMENT SYSTEM

**OCTOBER 2026**

Submitted by  
**NAME:** SUMMERJEET SINGH  
**REGISTER NO:** 71762307053  
**DEPARTMENT:** Information Technology  

---

## BONAFIDE CERTIFICATE

Certified that this project report titled **“SMART PARKING MANAGEMENT SYSTEM”** is the bonafide work of **71762307053 - SUMMERJEET SINGH** completed during the academic year 2025–2026 – Semester VII for the project presentation of **23IT723 - DEVOPS LABORATORY** under our supervision.

Certified that the candidate was examined by using the project work examination.

**Review Members:**
1. **Dr. M. Sangeetha**
2. **Dr. E. Arul**

---

## 23IT723 – DEVOPS LABORATORY
### FINAL MINI PROJECT – EVALUATION SCHEME

The final mini project requires students to integrate the major DevOps practices covered in the laboratory. The project demonstrates practical implementation of version control, collaborative development, Continuous Integration, containerization, and automated configuration/provisioning with proper execution evidence.

| S.No. | Evaluation Component | Key Verification Points | Marks |
| :---: | :--- | :--- | :---: |
| 1 | **Problem Definition & Project Planning** | Problem statement, objectives, requirements, scope, module identification, technology selection and workflow planning. | 10 |
| 2 | **Git Repository & Version Control** | Repository creation, meaningful commits, README, .gitignore, remote repository, push/pull/fetch operations and commit history. | 15 |
| 3 | **Branching, Merging & Collaboration** | Feature branches, parallel development, merging, conflict handling, branch organization and collaborative workflow. | 10 |
| 4 | **Application Development & Build** | Working application/source code, project structure, dependency management, build configuration and successful execution. | 15 |
| 5 | **Jenkins Continuous Integration** | Jenkins configuration, source-code integration, automated checkout, build job/pipeline, build execution and console verification. | 15 |
| 6 | **Docker / Containerization** | Dockerfile, image creation, container execution, port/configuration handling, application deployment and container verification. | 10 |
| 7 | **Automation / Configuration Management** | Ansible playbook automation, repeatable configuration/provisioning and successful execution. | 5 |
| 8 | **Testing & Verification** | Functional testing, build verification, error identification, test evidence and corrective action using Pytest. | 5 |
| 9 | **Documentation & Technical Presentation** | Architecture/workflow diagram, commands/configuration, screenshots, results, troubleshooting, conclusion and repository details. | 5 |
| 10 | **Final Demonstration & Viva-Voce** | Live demonstration, explanation of implementation, troubleshooting responses and technical understanding. | 10 |
| **TOTAL** | | | **100** |

---

## RECOMMENDED MARK DISTRIBUTION WITHIN FINAL DEMONSTRATION

| Assessment Area | Marks |
| :--- | :---: |
| Working implementation and correctness | 30 |
| DevOps tool integration and automation | 20 |
| Version control and collaborative workflow | 15 |
| Build / deployment / container verification | 15 |
| Testing and troubleshooting | 5 |
| Documentation and technical presentation | 5 |
| Live demonstration and viva-voce | 10 |
| **TOTAL** | **100** |

### Minimum Evidence to be Submitted
- Project repository URL and project README.
- Git commit history and branch/merge evidence.
- Jenkins job/pipeline configuration and successful build evidence.
- Dockerfile, image and running container evidence where Docker is used.
- Automation/configuration scripts (Ansible playbook `docker-deploy.yml`).
- Application execution and Pytest testing evidence.
- Architecture / workflow diagram.
- Short technical report containing implementation steps, results and troubleshooting.
- Live demonstration of the complete DevOps workflow.

---

## TABLE OF CONTENTS

1. **INTRODUCTION**
2. **OBJECTIVES**
3. **ABSTRACT**
4. **TECHNOLOGY STACK**
5. **SYSTEM ARCHITECTURE**
6. **MODULE 1 — USER INTERFACE & PARKING SLOT DISPLAY**
7. **MODULE 2 — FLASK BACKEND & RESERVATION MANAGEMENT**
8. **MODULE 3 — SQLITE DATABASE MANAGEMENT**
9. **MODULE 4 — GIT & GITHUB SOURCE CONTROL**
10. **MODULE 5 — DOCKER CONTAINERIZATION**
11. **MODULE 6 — JENKINS CI/CD PIPELINE**
12. **MODULE 7 — AUTOMATED TESTING (PYTEST)**
13. **MODULE 8 — ANSIBLE DEPLOYMENT**
14. **MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)**
15. **MODULE 10 — ADMIN OCCUPANCY DASHBOARD**
16. **MODULE 11 — CI/CD INTEGRATION WORKFLOW**
17. **MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION**
18. **RESULTS AND OUTPUT**
19. **COMMANDS USED**
20. **ADVANTAGES**
21. **LIMITATIONS**
22. **FUTURE ENHANCEMENTS**
23. **CONCLUSION**

---

## 1. INTRODUCTION

The **Smart Parking Management System** is a modern, responsive web application engineered to solve urban parking congestion, minimize search time for drivers, and automate parking slot allocation and revenue management. Traditional parking infrastructure often suffers from manual ticketing, lack of real-time visibility into slot availability, inefficient space utilization, and lack of persistent tracking.

The application allows vehicle drivers to view live parking bay availability organized by zones (Four Wheeler, Two Wheeler, and Electric Vehicle Fast-Charging), select preferred bays, book parking passes in real time, and release slots upon exit with automated billing calculation. An administrative dashboard provides parking facility supervisors with instant occupancy metrics, live bay status tracking, manual override controls, and searchable logs of all vehicle transactions.

The project integrates end-to-end DevOps automation practices. Version control is managed through Git and GitHub. Automated continuous integration and delivery is handled via Jenkins. The application is packaged into isolated environments with Docker, automatically tested with Pytest, provisioned and deployed via Ansible, and configured with Docker Volumes for robust data persistence across container updates.

---

## 2. OBJECTIVES

- To develop an interactive smart parking web application displaying real-time parking slot occupancy across multiple vehicle categories (Car, Bike, EV).
- To allow users to reserve available parking bays with automated parking pass generation and duration-based fare estimation.
- To provide a quick release and exit mechanism that calculates parking duration, fees, and updates slot availability instantly.
- To implement an administrative control dashboard for real-time occupancy monitoring, force-release capabilities, and transaction logs.
- To maintain persistent data storage for parking slots and reservation records using SQLite and Docker Volumes.
- To implement Git version control practices with clean commit histories and structured feature branching.
- To containerize the application using Docker for deterministic execution across development and production environments.
- To build a Jenkins multi-stage CI/CD pipeline automating SCM checkout, Docker container build, test execution, and deployment.
- To integrate Pytest automated unit and integration tests into the CI/CD pipeline to prevent regression bugs.
- To automate container provisioning and deployment using Ansible playbooks.

---

## 3. ABSTRACT

The **Smart Parking Management System** addresses the critical operational inefficiencies of physical parking facilities by introducing real-time digital space allocation combined with modern DevOps automation. The system offers an intuitive, dark-mode user interface enabling drivers to inspect 24 distinct parking bays across three specialized zones: Zone A (Four-Wheeler), Zone B (Two-Wheeler), and Zone C (Electric Vehicle Charging). Users can reserve free bays by providing vehicle registration, contact information, and expected parking duration, receiving an instant digital parking pass. The release module allows drivers to input their ticket ID or vehicle number to terminate parking and receive an itemized receipt.

The administrative interface gives facility managers real-time business intelligence: total capacity, currently available bays, active occupancies, and accumulated revenue, alongside quick override actions.

From a DevOps engineering standpoint, the solution establishes a complete automated lifecycle following the pipeline flow:
$$\text{GitHub} \longrightarrow \text{Jenkins CI} \longrightarrow \text{Docker Image Build} \longrightarrow \text{Pytest Test Suite} \longrightarrow \text{Ansible Deployment} \longrightarrow \text{Docker Container} \longrightarrow \text{Flask Backend} \longrightarrow \text{SQLite Persistent Volume}$$

Persistent data integrity is safeguarded through a dedicated Docker Volume (`parking_data`) mapped to `/app/data/parking.db`, ensuring all booking and occupancy records survive container rebuilds and host reboots.

---

## 4. TECHNOLOGY STACK

| Technology | Version | Purpose |
| :--- | :--- | :--- |
| **HTML5** | HTML5 | Semantics and structure of client-facing and administrative pages |
| **CSS3** | CSS3 | Responsive dark-mode styling, glassmorphism UI, status badges |
| **JavaScript** | ES6+ | Real-time DOM updates, interactive modals, AJAX API communication |
| **Python** | 3.11 / 3.12 | Core backend application programming and REST API logic |
| **Flask** | 3.0.x | Lightweight Web framework and routing engine |
| **SQLite** | 3.x | Embedded ACID-compliant database for slots and reservations |
| **Git** | 2.x | Distributed source code version control |
| **GitHub** | Cloud | Remote centralized repository and automated webhook triggers |
| **Jenkins** | 2.x | Continuous Integration / Continuous Deployment pipeline automation |
| **Docker** | 20.x+ / 28.x+ | Application containerization and environment isolation |
| **Pytest** | 8.x | Automated functional and integration unit testing |
| **Ansible** | 2.10+ | Automated container configuration management and deployment |
| **Docker Volume** | `parking_data` | Persistent data storage mapped to `/app/data` |

---

## 5. SYSTEM ARCHITECTURE

```text
+-----------------------------------------------------------------------------------+
|                        SMART PARKING - SYSTEM ARCHITECTURE                         |
+-----------------------------------------------------------------------------------+

 1. DEVELOPER WORKSTATION
   - Edits code (app.py, templates, static)
   - Executes local unit tests (pytest test_app.py)
   - Git Commit & Push: git push origin master

 2. SOURCE CONTROL (GITHUB)
   - Central repository storing application & DevOps configuration
   - Triggers Jenkins Pipeline on webhook or SCM polling

 3. CI/CD AUTOMATION (JENKINS PIPELINE)
   - Stage 1: Checkout SCM
   - Stage 2: Docker Build -> Builds Docker Image: `smart-parking-ci`
   - Stage 3: Automated Testing -> Runs `docker run --rm smart-parking-ci pytest`
   - Stage 4: Ansible Deployment -> Triggers `docker-deploy.yml` playbook

 4. CONFIGURATION MANAGEMENT (ANSIBLE)
   - Playbook: `docker-deploy.yml`
   - Manages Docker container state (image: `smart-parking-ci`)
   - Configures port publishing: 5001 -> 5000
   - Attaches persistent volume: `parking_data:/app/data`

 5. RUNTIME ENVIRONMENT (DOCKER CONTAINER)
   - Container Name: `smart-parking-ansible`
   - Port Mapping: `http://localhost:5001`
   - Volume: `parking_data` mounted at `/app/data`

 6. APPLICATION LAYER (FLASK & SQLITE)
   - User Portal: `http://localhost:5001/`
   - Admin Dashboard: `http://localhost:5001/admin`
   - REST APIs: `/api/slots`, `/api/reserve`, `/api/release`, `/api/stats`
   - Database: `/app/data/parking.db`
+-----------------------------------------------------------------------------------+
```

---

## MODULE 1 — USER INTERFACE & PARKING SLOT DISPLAY

This module provides the driver-facing responsive interface of the Smart Parking system. It provides immediate visual clarity into parking bay availability and makes reserving and releasing spots frictionless.

### Key Features:
- Displays 24 color-coded parking bays across Zone A (Four-Wheeler), Zone B (Two-Wheeler), and Zone C (EV Fast-Charging).
- Status indicators: Green for **Available**, Amber for **Reserved**, and Red for **Occupied**.
- Live search bar to quickly locate bays by slot number (e.g. `A-01`, `C-04`).
- Quick vehicle category filtering (All, Four-Wheeler, Two-Wheeler, EV Charging).
- Instant interactive reservation modal displaying selected bay, vehicle type, and duration slider with live cost preview.
- Quick Release modal allowing drivers to enter their parking pass code or vehicle plate to check out and print their receipt.

---

## MODULE 2 — FLASK BACKEND & RESERVATION MANAGEMENT

The Flask backend serves as the core application engine, managing business rules, rate calculations, database operations, and RESTful API endpoints.

### Key Functions:
- `GET /`: Renders user parking matrix with real-time bay availability counters.
- `GET /admin`: Serves the administrative control center with occupancy statistics and session records.
- `GET /api/slots`: Returns JSON payload of slots with optional filtering by zone, vehicle type, or status.
- `POST /api/reserve`: Validates driver inputs, checks bay availability, assigns a unique `PKG-XXXX` pass code, calculates total fee, and updates bay status.
- `POST /api/release`: Identifies active booking by vehicle number, slot, or pass code, computes final checkout parameters, marks slot as available, and generates exit receipt.
- `POST /api/admin/force-release`: Permits parking supervisors to clear occupied slots.
- `POST /api/admin/reset`: Restores database to fresh initial state for testing.

---

## MODULE 3 — SQLITE DATABASE MANAGEMENT

SQLite manages application state and persistence without requiring complex external database server setups.

### Database File Location:
- Host path: `data/parking.db`
- Container path: `/app/data/parking.db`
- Docker Volume: `parking_data`

### Database Schema:
1. **`slots` Table**:
   - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
   - `slot_number`: TEXT UNIQUE (e.g., `A-01` to `C-08`)
   - `zone`: TEXT (Zone A, Zone B, Zone C)
   - `vehicle_type`: TEXT (`Car`, `Bike`, `EV`)
   - `status`: TEXT (`available`, `reserved`, `occupied`)
   - `hourly_rate`: REAL (₹30.0, ₹15.0, ₹45.0)
   - `current_reservation_id`: TEXT NULL

2. **`reservations` Table**:
   - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
   - `reservation_code`: TEXT UNIQUE (e.g., `PKG-1001`)
   - `slot_number`: TEXT
   - `vehicle_number`: TEXT
   - `driver_name`: TEXT
   - `phone`: TEXT
   - `vehicle_type`: TEXT
   - `expected_hours`: INTEGER
   - `entry_time`: TIMESTAMP
   - `exit_time`: TIMESTAMP NULL
   - `hourly_rate`: REAL
   - `total_amount`: REAL
   - `status`: TEXT (`active`, `completed`, `cancelled`)

---

## MODULE 4 — GIT & GITHUB SOURCE CONTROL

Git tracks all project files, history, branches, and facilitates collaboration.

### Key Version Control Activities:
- Repository initialization (`git init`).
- Ignoring non-essential cache files via `.gitignore`.
- Structuring feature branches for parallel development (`feature/parking-grid`, `feature/admin-dashboard`).
- Writing descriptive commit messages (`git commit -m "Implement parking reservation and release workflow"`).
- Synchronizing with remote GitHub repository to trigger automated CI/CD builds.

---

## MODULE 5 — DOCKER CONTAINERIZATION

Docker packages the Smart Parking application and all dependencies into a lightweight, portable container image.

### Docker Configuration Details:
- **Base Image**: `python:3.11-slim`
- **Working Directory**: `/app`
- **Volume Mount Point**: `/app/data`
- **Image Name**: `smart-parking-ci`
- **Container Name**: `smart-parking-ansible`
- **Port Mapping**: `5001:5000` (Container internal port 5000 mapped to host port 5001)

### Docker Build Flow:
$$\text{Application Source Code} \longrightarrow \text{Dockerfile} \longrightarrow \text{Docker Image: smart-parking-ci} \longrightarrow \text{Running Container: smart-parking-ansible}$$

---

## MODULE 6 — JENKINS CI/CD PIPELINE

Jenkins coordinates the end-to-end automation of the development lifecycle through a declarative `Jenkinsfile`.

### Pipeline Stages:
1. **Stage 1: Checkout SCM**: Pulls latest code from Git repository.
2. **Stage 2: Build Docker Image**: Executes `docker build -t smart-parking-ci .`.
3. **Stage 3: Run Automated Tests**: Runs `docker run --rm smart-parking-ci python -m pytest test_app.py`.
4. **Stage 4: Deploy with Ansible**: Executes Ansible deployment playbook `docker-deploy.yml`.
5. **Stage 5: Application Verification**: Confirms healthy container state on port 5001.

---

## MODULE 7 — AUTOMATED TESTING (PYTEST)

The Pytest testing module guarantees software reliability before any deployment takes place.

### Test Scenarios in `test_app.py`:
- `test_home_page`: Validates homepage loads with HTTP 200 and visual components.
- `test_admin_dashboard`: Confirms admin metrics and table respond properly.
- `test_api_slots_listing`: Checks `/api/slots` returns JSON with all 24 bays.
- `test_api_stats`: Validates live calculation of total, available, and occupied bays.
- `test_reserve_and_release_workflow`: Simulates complete end-to-end booking of a bay, verifies state changes from `available` $\to$ `reserved` $\to$ `available`, and tests receipt generation.
- `test_reserve_invalid_slot`: Verifies validation when booking non-existent slots.
- `test_release_invalid_identifier`: Tests error handling for unmatched release requests.

**Test Result:** All 7 tests pass successfully with 100% pass rate.

---

## MODULE 8 — ANSIBLE DEPLOYMENT

Ansible automates container provisioning and lifecycle management declaratively through `docker-deploy.yml`.

### Playbook Specifications:
- **Playbook**: `docker-deploy.yml`
- **Target Host**: `dockerhost` (defined in `inventory.ini`)
- **Module**: `community.docker.docker_container`
- **Container Name**: `smart-parking-ansible`
- **Image**: `smart-parking-ci`
- **Port Mapping**: `5001:5000`
- **Volume**: `parking_data:/app/data`
- **Restart Policy**: `unless-stopped`

---

## MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)

To prevent data loss when containers are recreated, updated, or restarted, a dedicated Docker named volume is utilized.

### Volume Configuration:
- **Volume Name**: `parking_data`
- **Host Target**: `/app/data` inside container
- **Database File**: `/app/data/parking.db`
- **Verification**: Dropping or restarting the container does not delete existing parking bookings or revenue totals.

---

## MODULE 10 — ADMIN OCCUPANCY DASHBOARD

Accessible at `http://localhost:5001/admin`, this dashboard empowers parking administrators with full visibility:
- **Real-Time KPI Cards**: Total Bay Capacity, Available Bays, Occupied Bays, Total Revenue.
- **Bay Status Matrix**: Visual overview of all 24 bays with one-click "Free" buttons to force-release any bay.
- **Reservations & Occupancy Log Table**: Real-time filtering and search across pass IDs, vehicle license plates, driver names, phone numbers, and active/completed statuses.
- **System Reset Control**: Enables instant restoration of default testing states.

---

## MODULE 11 — CI/CD INTEGRATION WORKFLOW

The integration of Git, GitHub, Jenkins, Docker, Pytest, and Ansible creates a seamless, repeatable deployment pipeline. Any developer change pushed to the repository is automatically checked out, built, tested, and deployed to production within seconds without manual intervention.

---

## MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION

Post-deployment verification includes:
1. Verifying running container via `docker ps`.
2. Accessing user portal on `http://localhost:5001`.
3. Reserving slot `A-02` with vehicle `TN-37-AB-5678`.
4. Verifying slot `A-02` turns orange (Reserved) on the user grid.
5. Verifying admin dashboard reflects updated count and new reservation record.
6. Releasing slot `A-02` and verifying slot returns to green (Available).
7. Verifying data persists after container stop and restart.

---

## 18. RESULTS AND OUTPUT

The implemented Smart Parking Management System delivers:
- Real-time display of 24 parking bays across 3 vehicle categories.
- User-friendly reservation interface with dynamic cost calculation.
- Automated generation of digital parking passes (`PKG-XXXX`).
- Quick release and exit workflow with itemized billing receipts.
- Administrative dashboard with live occupancy analytics and manual controls.
- Persistent SQLite database storage backed by Docker Volumes.
- Fully automated Docker containerization.
- Continuous automated testing with 7 passing Pytest test cases.
- Automated multi-stage Jenkins CI/CD pipeline.
- Infrastructure-as-Code deployment using Ansible playbooks.

---

## 19. COMMANDS USED

### 1. Docker Commands
```bash
# Check running containers
docker ps

# Check all containers
docker ps -a

# Build Docker image
docker build -t smart-parking-ci .

# Create Docker volume for database persistence
docker volume create parking_data

# Run container with volume mount and port mapping
docker run -d --name smart-parking-ansible -p 5001:5000 -v parking_data:/app/data --restart unless-stopped smart-parking-ci

# View container logs
docker logs smart-parking-ansible

# Stop and restart container
docker stop smart-parking-ansible
docker start smart-parking-ansible
```

### 2. Jenkins & Pipeline Commands
```bash
# Jenkins port access
http://localhost:9091

# Jenkins pipeline test execution step
docker run --rm smart-parking-ci python -m pytest test_app.py

# Jenkins deployment trigger via Ansible
docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml
```

### 3. Pytest Automated Testing Commands
```bash
# Run test suite locally
python -m pytest test_app.py -v

# Run test suite inside Docker container
docker run --rm smart-parking-ci python -m pytest test_app.py
```

### 4. Ansible Commands
```bash
# Execute deployment playbook
ansible-playbook -i inventory.ini docker-deploy.yml

# Execute inside Ansible lab container
docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml
```

### 5. SQLite & Volume Verification Commands
```bash
# List Docker volumes
docker volume ls

# Inspect parking_data volume
docker volume inspect parking_data

# Query SQLite database inside running container
docker exec smart-parking-ansible python -c "import sqlite3; c=sqlite3.connect('data/parking.db'); [print(row) for row in c.execute('SELECT slot_number, status, hourly_rate FROM slots LIMIT 10')]; c.close()"
```

### 6. Git Version Control Commands
```bash
# Initialize git repository
git init

# Check status
git status

# Stage all files
git add .

# Commit changes
git commit -m "Finalize Smart Parking Management System CI/CD project"

# Add remote and push
git remote add origin https://github.com/71762307053/SmartParkingSystem.git
git branch -M master
git push -u origin master
```

---

## 20. ADVANTAGES

- **Eliminates Manual Inefficiencies**: Replaces paper tickets with automated digital tokens and real-time status.
- **Reduces Search Time & Traffic**: Drivers immediately spot available slots without circling parking lots.
- **Comprehensive DevOps Automation**: Manual build, test, and deployment steps are completely automated.
- **Environment Consistency**: Docker containers eliminate "works on my machine" issues across operating systems.
- **Reliable Continuous Testing**: Pytest automatically blocks broken builds before they reach production.
- **Fault-Tolerant Persistence**: Docker Volumes protect database state from container lifecycles.
- **Repeatable Infrastructure**: Ansible playbooks ensure deterministic, repeatable multi-environment deployments.

---

## 21. LIMITATIONS

- Uses SQLite database which is optimized for single-instance embedded use rather than high-concurrency distributed clusters.
- Digital payment gateways (Stripe, UPI, Razorpay) are simulated via receipts rather than live banking APIs.
- Physical IoT sensors (ultrasonic/RFID bay hardware) are currently represented through the web simulation interface.
- Deployment is demonstrated within a local Docker host environment rather than a multi-node Kubernetes cluster.

---

## 22. FUTURE ENHANCEMENTS

1. **Hardware IoT Integration**: Integration with ESP32/Ultrasonic sensors and RFID barriers for automated gate opening.
2. **Payment Gateway Integration**: Integration of UPI QR codes and payment gateways (Razorpay/Stripe).
3. **Number Plate Recognition (ANPR)**: Automatic computer vision recognition using OpenCV at facility entry/exit.
4. **PostgreSQL / MySQL Migration**: Upgrading database engine for high-traffic enterprise deployment.
5. **Kubernetes Orchestration**: Deploying with Kubernetes Helm charts and Horizontal Pod Autoscaling (HPA).
6. **Mobile App Companion**: Flutter/React Native mobile app with push notifications.

---

## 23. CONCLUSION

The **Smart Parking Management System** successfully demonstrates the complete fusion of a real-world web application with industry-standard DevOps practices. The system provides users with live bay availability, rapid slot reservations, and itemized billing receipts, while supplying parking managers with centralized occupancy control and real-time revenue analytics.

The DevOps pipeline implementation establishes a robust, automated workflow:
$$\text{Git/GitHub} \longrightarrow \text{Jenkins CI} \longrightarrow \text{Docker Image} \longrightarrow \text{Pytest Testing} \longrightarrow \text{Ansible Deployment} \longrightarrow \text{Flask Backend} \longrightarrow \text{SQLite Docker Volume}$$

Automated testing with Pytest validates all core features prior to deployment. Docker containerization ensures consistent portable execution, while Ansible provides repeatable automated deployment. Persistent storage via Docker Volumes guarantees data safety across container rebuilds. The project successfully achieves all evaluation criteria of the 23IT723 – DevOps Laboratory curriculum.
