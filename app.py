import os
import sqlite3
import random
import string
from datetime import datetime, timezone
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "smart-parking-secret-key-2026")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.environ.get("DB_PATH", os.path.join(DATA_DIR, "parking.db"))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Slots table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_number TEXT UNIQUE NOT NULL,
        zone TEXT NOT NULL,
        vehicle_type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'available',
        hourly_rate REAL NOT NULL,
        current_reservation_id TEXT
    )
    """)

    # Reservations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reservation_code TEXT UNIQUE NOT NULL,
        slot_number TEXT NOT NULL,
        vehicle_number TEXT NOT NULL,
        driver_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        vehicle_type TEXT NOT NULL,
        expected_hours INTEGER NOT NULL,
        entry_time TEXT NOT NULL,
        exit_time TEXT,
        hourly_rate REAL NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'active'
    )
    """)
    conn.commit()

    # Seed default parking slots if empty
    cursor.execute("SELECT COUNT(*) AS count FROM slots")
    count = cursor.fetchone()["count"]
    if count == 0:
        default_slots = []
        # Zone A - 8 Car Slots (₹30/hr)
        for i in range(1, 9):
            slot_id = f"A-{i:02d}"
            default_slots.append((slot_id, "Zone A - Four Wheeler", "Car", "available", 30.0, None))

        # Zone B - 8 Two-Wheeler Slots (₹15/hr)
        for i in range(1, 9):
            slot_id = f"B-{i:02d}"
            default_slots.append((slot_id, "Zone B - Two Wheeler", "Bike", "available", 15.0, None))

        # Zone C - 8 EV Charging Slots (₹45/hr)
        for i in range(1, 9):
            slot_id = f"C-{i:02d}"
            default_slots.append((slot_id, "Zone C - EV Charging", "EV", "available", 45.0, None))

        cursor.executemany("""
        INSERT INTO slots (slot_number, zone, vehicle_type, status, hourly_rate, current_reservation_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, default_slots)

        # Seed sample active reservation for live preview
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        INSERT INTO reservations 
        (reservation_code, slot_number, vehicle_number, driver_name, phone, vehicle_type, expected_hours, entry_time, hourly_rate, total_amount, status)
        VALUES ('PKG-1001', 'A-01', 'TN-37-AB-1234', 'Karthik Raja', '9876543210', 'Car', 2, ?, 30.0, 60.0, 'active')
        """, (now_str,))

        cursor.execute("""
        UPDATE slots SET status = 'reserved', current_reservation_id = 'PKG-1001' WHERE slot_number = 'A-01'
        """)

        cursor.execute("""
        INSERT INTO reservations 
        (reservation_code, slot_number, vehicle_number, driver_name, phone, vehicle_type, expected_hours, entry_time, hourly_rate, total_amount, status)
        VALUES ('PKG-1002', 'C-01', 'TN-38-EV-9900', 'Priya Sundar', '9841234567', 'EV', 3, ?, 45.0, 135.0, 'active')
        """, (now_str,))

        cursor.execute("""
        UPDATE slots SET status = 'occupied', current_reservation_id = 'PKG-1002' WHERE slot_number = 'C-01'
        """)

        conn.commit()

    conn.close()

# Initialize DB on start
init_db()

def generate_reservation_code():
    digits = ''.join(random.choices(string.digits, k=4))
    return f"PKG-{digits}"

# --- FRONTEND PAGES ---

@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM slots ORDER BY slot_number ASC")
    slots = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM slots")
    total_slots = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as available FROM slots WHERE status = 'available'")
    available_slots = cursor.fetchone()["available"]

    cursor.execute("SELECT COUNT(*) as occupied FROM slots WHERE status IN ('reserved', 'occupied')")
    occupied_slots = cursor.fetchone()["occupied"]

    conn.close()
    return render_template(
        "index.html",
        slots=slots,
        total_slots=total_slots,
        available_slots=available_slots,
        occupied_slots=occupied_slots
    )

@app.route("/admin")
def admin():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM slots ORDER BY slot_number ASC")
    slots = cursor.fetchall()

    cursor.execute("SELECT * FROM reservations ORDER BY id DESC")
    reservations = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total FROM slots")
    total_slots = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as available FROM slots WHERE status = 'available'")
    available_slots = cursor.fetchone()["available"]

    cursor.execute("SELECT COUNT(*) as reserved FROM slots WHERE status = 'reserved'")
    reserved_slots = cursor.fetchone()["reserved"]

    cursor.execute("SELECT COUNT(*) as occupied FROM slots WHERE status = 'occupied'")
    occupied_slots = cursor.fetchone()["occupied"]

    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total_rev FROM reservations")
    total_revenue = cursor.fetchone()["total_rev"]

    cursor.execute("SELECT COUNT(*) as active_count FROM reservations WHERE status = 'active'")
    active_reservations = cursor.fetchone()["active_count"]

    conn.close()
    return render_template(
        "admin.html",
        slots=slots,
        reservations=reservations,
        total_slots=total_slots,
        available_slots=available_slots,
        reserved_slots=reserved_slots,
        occupied_slots=occupied_slots,
        total_revenue=total_revenue,
        active_reservations=active_reservations
    )

# --- REST APIS ---

@app.route("/api/slots", methods=["GET"])
def api_slots():
    zone = request.args.get("zone")
    v_type = request.args.get("type")
    status = request.args.get("status")

    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM slots WHERE 1=1"
    params = []

    if zone:
        query += " AND zone LIKE ?"
        params.append(f"%{zone}%")
    if v_type:
        query += " AND vehicle_type = ?"
        params.append(v_type)
    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY slot_number ASC"
    cursor.execute(query, params)
    slots = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"success": True, "slots": slots, "count": len(slots)})

@app.route("/api/stats", methods=["GET"])
def api_stats():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM slots")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as available FROM slots WHERE status = 'available'")
    available = cursor.fetchone()["available"]

    cursor.execute("SELECT COUNT(*) as reserved FROM slots WHERE status = 'reserved'")
    reserved = cursor.fetchone()["reserved"]

    cursor.execute("SELECT COUNT(*) as occupied FROM slots WHERE status = 'occupied'")
    occupied = cursor.fetchone()["occupied"]

    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total_revenue FROM reservations")
    revenue = cursor.fetchone()["total_revenue"]

    occupancy_rate = round(((total - available) / total * 100), 1) if total > 0 else 0

    conn.close()
    return jsonify({
        "success": True,
        "total": total,
        "available": available,
        "reserved": reserved,
        "occupied": occupied,
        "revenue": revenue,
        "occupancy_rate": occupancy_rate
    })

@app.route("/api/reserve", methods=["POST"])
def api_reserve():
    data = request.get_json() or {}
    slot_number = data.get("slot_number", "").strip().upper()
    vehicle_number = data.get("vehicle_number", "").strip().upper()
    driver_name = data.get("driver_name", "").strip()
    phone = data.get("phone", "").strip()
    vehicle_type = data.get("vehicle_type", "Car").strip()
    try:
        expected_hours = int(data.get("expected_hours", 1))
        if expected_hours < 1:
            expected_hours = 1
    except (ValueError, TypeError):
        expected_hours = 1

    if not slot_number or not vehicle_number or not driver_name:
        return jsonify({"success": False, "message": "Slot number, vehicle number, and driver name are required."}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM slots WHERE slot_number = ?", (slot_number,))
    slot = cursor.fetchone()

    if not slot:
        conn.close()
        return jsonify({"success": False, "message": f"Parking slot {slot_number} does not exist."}), 404

    if slot["status"] != "available":
        conn.close()
        return jsonify({"success": False, "message": f"Slot {slot_number} is currently {slot['status']}."}), 400

    hourly_rate = slot["hourly_rate"]
    total_amount = hourly_rate * expected_hours
    reservation_code = generate_reservation_code()
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO reservations 
    (reservation_code, slot_number, vehicle_number, driver_name, phone, vehicle_type, expected_hours, entry_time, hourly_rate, total_amount, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
    """, (reservation_code, slot_number, vehicle_number, driver_name, phone, vehicle_type, expected_hours, entry_time, hourly_rate, total_amount))

    cursor.execute("""
    UPDATE slots SET status = 'reserved', current_reservation_id = ? WHERE slot_number = ?
    """, (reservation_code, slot_number))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": f"Parking slot {slot_number} successfully reserved!",
        "reservation": {
            "reservation_code": reservation_code,
            "slot_number": slot_number,
            "vehicle_number": vehicle_number,
            "driver_name": driver_name,
            "vehicle_type": vehicle_type,
            "expected_hours": expected_hours,
            "hourly_rate": hourly_rate,
            "total_amount": total_amount,
            "entry_time": entry_time
        }
    })

@app.route("/api/release", methods=["POST"])
def api_release():
    data = request.get_json() or {}
    identifier = data.get("identifier", "").strip().upper()

    if not identifier:
        return jsonify({"success": False, "message": "Reservation code, slot number, or vehicle number is required."}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Find active reservation matching identifier
    cursor.execute("""
    SELECT * FROM reservations 
    WHERE (reservation_code = ? OR slot_number = ? OR vehicle_number = ?)
      AND status = 'active'
    ORDER BY id DESC LIMIT 1
    """, (identifier, identifier, identifier))
    reservation = cursor.fetchone()

    if not reservation:
        # Fallback check if slot exists and is occupied
        cursor.execute("SELECT * FROM slots WHERE slot_number = ?", (identifier,))
        slot = cursor.fetchone()
        if slot and slot["status"] != "available":
            cursor.execute("UPDATE slots SET status = 'available', current_reservation_id = NULL WHERE slot_number = ?", (identifier,))
            conn.commit()
            conn.close()
            return jsonify({
                "success": True,
                "message": f"Slot {identifier} manually released and marked available."
            })
        conn.close()
        return jsonify({"success": False, "message": "No active reservation found for this vehicle or slot."}), 404

    exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    slot_num = reservation["slot_number"]

    cursor.execute("""
    UPDATE reservations 
    SET exit_time = ?, status = 'completed'
    WHERE id = ?
    """, (exit_time, reservation["id"]))

    cursor.execute("""
    UPDATE slots 
    SET status = 'available', current_reservation_id = NULL
    WHERE slot_number = ?
    """, (slot_num,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": f"Slot {slot_num} has been successfully released!",
        "summary": {
            "reservation_code": reservation["reservation_code"],
            "slot_number": slot_num,
            "vehicle_number": reservation["vehicle_number"],
            "driver_name": reservation["driver_name"],
            "entry_time": reservation["entry_time"],
            "exit_time": exit_time,
            "total_amount": reservation["total_amount"]
        }
    })

@app.route("/api/admin/force-release", methods=["POST"])
def api_force_release():
    data = request.get_json() or {}
    slot_number = data.get("slot_number", "").strip().upper()

    if not slot_number:
        return jsonify({"success": False, "message": "Slot number is required."}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM slots WHERE slot_number = ?", (slot_number,))
    slot = cursor.fetchone()
    if not slot:
        conn.close()
        return jsonify({"success": False, "message": "Slot not found."}), 404

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE reservations 
    SET exit_time = ?, status = 'completed'
    WHERE slot_number = ? AND status = 'active'
    """, (now_str, slot_number))

    cursor.execute("""
    UPDATE slots 
    SET status = 'available', current_reservation_id = NULL
    WHERE slot_number = ?
    """, (slot_number,))

    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"Slot {slot_number} force-released successfully."})

@app.route("/api/admin/toggle-status", methods=["POST"])
def api_toggle_status():
    data = request.get_json() or {}
    slot_number = data.get("slot_number", "").strip().upper()
    new_status = data.get("status", "available").strip().lower()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE slots SET status = ? WHERE slot_number = ?", (new_status, slot_number))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"Slot {slot_number} status updated to {new_status}."})

@app.route("/api/admin/reset", methods=["POST"])
def api_reset():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS slots")
    cursor.execute("DROP TABLE IF EXISTS reservations")
    conn.commit()
    conn.close()
    init_db()
    return jsonify({"success": True, "message": "Parking management system successfully reset to defaults."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
