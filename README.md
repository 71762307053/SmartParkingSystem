# Smart Parking Management System (DevOps CI/CD)

An automated web-based smart parking reservation and management system containerized with **Docker**, continuously integrated via **Jenkins**, automated using **Ansible**, and verified with **Pytest** and persistent **Docker Volumes**.

Developed for **23IT723 – DevOps Laboratory**, Department of Information Technology, Coimbatore Institute of Technology.

---

## 🌟 Key Application Features

1. **Display Available Parking Slots**:
   - Interactive visual bay matrix displaying 24 slots across 3 zones:
     - **Zone A**: Four-Wheeler bays (Cars) - ₹30/hr
     - **Zone B**: Two-Wheeler bays (Motorcycles & Scooters) - ₹15/hr
     - **Zone C**: Dedicated EV Fast-Charging bays - ₹45/hr
   - Real-time slot status indicators: **Available** (Green), **Reserved** (Amber), and **Occupied** (Red).
   - Dynamic vehicle category filtering and instant slot search.

2. **User Reservation & Release Workflow**:
   - One-click slot reservation with custom expected duration and automated estimated fee computation.
   - Generates unique parking pass tokens (e.g., `PKG-1001`) with vehicle details and timestamp.
   - Quick release / exit functionality using Parking Pass Code, Vehicle Number, or Bay Number.
   - Automated checkout billing receipt generation.

3. **Admin Dashboard (`/admin`)**:
   - Live KPI overview cards: Total Bay Capacity, Available Bays, Occupied Bays, and Total Revenue collected.
   - Real-time Slot Matrix overview with single-click manual override / force-release.
   - Searchable transaction history table of all active and completed parking sessions.
   - One-click system reset control.

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend** | HTML5 / CSS3 / JavaScript | ES6+ | Responsive dark-mode user interface & admin dashboard |
| **Backend** | Python / Flask | 3.11+ / 3.0+ | REST API & parking booking business logic |
| **Database** | SQLite3 | 3.x | Lightweight SQL storage for bays and booking records |
| **Source Control** | Git & GitHub | 2.x | Distributed version control and CI trigger |
| **Continuous Integration** | Jenkins | 2.x | Automated multi-stage build, test & deployment pipeline |
| **Testing** | Pytest | 8.x | Automated API and integration unit tests |
| **Containerization** | Docker | 20.x+ | Application containerization & portable runtime |
| **Persistent Storage** | Docker Volume | `parking_data` | Persistent SQLite database mounted to `/app/data` |
| **Config / Deployment** | Ansible | 2.10+ | Automated container deployment & configuration playbook |

---

## 🏗️ System Architecture & CI/CD Workflow

```text
[Developer]
    │
    │  git push
    ▼
[GitHub Repository]
    │
    │  Webhook / Poll SCM
    ▼
[Jenkins CI/CD Pipeline]
    ├─► Stage 1: Checkout SCM
    ├─► Stage 2: Docker Build (Image: smart-parking-ci)
    ├─► Stage 3: Pytest Automated Tests (python -m pytest test_app.py)
    └─► Stage 4: Ansible Deployment (Playbook: docker-deploy.yml)
                     │
                     ▼
           [Docker Host Container]
           Container: smart-parking-ansible
           Port Mapping: 5001 -> 5000
           Volume Mount: parking_data -> /app/data
                     │
                     ▼
       ┌──────────────────────────────┐
       │   Smart Parking Web App      │
       │   - User UI (/)              │
       │   - Admin Dashboard (/admin) │
       │   - Persistent SQLite DB     │
       └──────────────────────────────┘
```

---

## 🚀 Quick Start & Execution Guide

### Option 1: Running Locally with Python

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run unit and integration tests
python -m pytest test_app.py -v

# 3. Start the Flask application
python app.py
```
Open your browser at:
- **User Portal**: [http://localhost:5000](http://localhost:5000)
- **Admin Dashboard**: [http://localhost:5000/admin](http://localhost:5000/admin)

---

### Option 2: Running with Docker (Standalone)

```bash
# 1. Build the Docker image
docker build -t smart-parking-ci .

# 2. Run automated tests inside Docker
docker run --rm smart-parking-ci python -m pytest test_app.py

# 3. Create persistent Docker volume
docker volume create parking_data

# 4. Run the container on port 5001
docker run -d --name smart-parking-ansible -p 5001:5000 -v parking_data:/app/data --restart unless-stopped smart-parking-ci

# 5. Verify running container
docker ps
```
Open your browser at:
- **User Portal**: [http://localhost:5001](http://localhost:5001)
- **Admin Dashboard**: [http://localhost:5001/admin](http://localhost:5001/admin)

---

### Option 3: Automated Deployment with Ansible

```bash
# Execute the Ansible playbook
ansible-playbook -i inventory.ini docker-deploy.yml
```

Or from inside the lab Ansible container:
```bash
docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml
```

---

## 🧪 Testing & Verification Commands

```bash
# Execute test suite
python -m pytest test_app.py

# Verify SQLite database records inside running container
docker exec smart-parking-ansible python -c "import sqlite3; c=sqlite3.connect('data/parking.db'); [print(row) for row in c.execute('SELECT slot_number, status, current_reservation_id FROM slots LIMIT 10')]; c.close()"

# Inspect Docker persistent volume
docker volume inspect parking_data
```

---

## 📁 Repository Structure

```text
├── app.py                  # Main Flask application and SQLite database handling
├── test_app.py             # Pytest automated test suite (7 test scenarios)
├── Dockerfile              # Container definition for Python 3.11-slim
├── Jenkinsfile             # Declarative Jenkins CI/CD pipeline script
├── docker-deploy.yml       # Ansible playbook for automated container provisioning
├── inventory.ini           # Ansible inventory configuration
├── ansible.cfg             # Ansible runtime parameters
├── requirements.txt        # Python package dependencies
├── .gitignore              # Files excluded from Git version control
├── data/                   # SQLite database directory (mounted as volume)
│   └── parking.db          # Auto-seeded SQLite database file
├── templates/
│   ├── base.html           # Master HTML layout with modern navbar and modals
│   ├── index.html          # User reservation portal & live visual bay matrix
│   └── admin.html          # Administrative occupancy & reservation management
├── static/
│   ├── css/style.css       # Polished dark-mode UI stylesheet
│   └── js/
│       ├── main.js         # User interactions, booking modal, AJAX requests
│       └── admin.js        # Admin table filter, force release, system reset
└── PROJECT_REPORT.md       # Comprehensive Laboratory Project Report (CIT 23IT723)
```
