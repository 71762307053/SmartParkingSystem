// ParkSmart Main Application JavaScript

// Modal open/close helpers
function openModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('hidden');
}

function closeModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
}

// Global Toast Notifications
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let icon = '<i class="fa-solid fa-circle-info"></i>';
    if (type === 'success') icon = '<i class="fa-solid fa-circle-check text-green"></i>';
    if (type === 'error') icon = '<i class="fa-solid fa-circle-exclamation text-red"></i>';
    if (type === 'warning') icon = '<i class="fa-solid fa-triangle-exclamation text-yellow"></i>';

    toast.innerHTML = `${icon} <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Slot Filter Functionality
function filterSlots(type) {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(b => b.classList.remove('active'));

    const activeBtn = document.querySelector(`.filter-btn[data-filter="${type}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    const cards = document.querySelectorAll('.slot-card');
    cards.forEach(card => {
        const slotType = card.getAttribute('data-type');
        if (type === 'all' || slotType === type) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

// Slot Search Functionality
function searchSlots() {
    const query = document.getElementById('slotSearchInput').value.trim().toLowerCase();
    const cards = document.querySelectorAll('.slot-card');

    cards.forEach(card => {
        const slotNum = card.getAttribute('data-slot').toLowerCase();
        const slotZone = card.getAttribute('data-zone').toLowerCase();
        if (slotNum.includes(query) || slotZone.includes(query)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

// Slot Card Click Handler
function handleSlotClick(slotNumber, status, vehicleType, hourlyRate) {
    if (status === 'available') {
        openReserveModal(slotNumber, vehicleType, hourlyRate);
    } else {
        quickReleasePrompt(slotNumber);
    }
}

// Open Reserve Modal
function openReserveModal(slotNumber, vehicleType, hourlyRate) {
    document.getElementById('modalSlotNumber').textContent = slotNumber;
    document.getElementById('modalHourlyRate').textContent = `₹${hourlyRate} / hr`;
    document.getElementById('formSlotNumber').value = slotNumber;
    document.getElementById('formHourlyRate').value = hourlyRate;

    // Set select option matching slot vehicle type
    const vSelect = document.getElementById('formVehicleType');
    if (vSelect) vSelect.value = vehicleType;

    // Reset fields
    document.getElementById('formHours').value = 2;
    updateCostEstimate();

    openModal('reserveModal');
}

// Live Cost Calculation
function updateCostEstimate() {
    const hours = parseInt(document.getElementById('formHours').value) || 1;
    const rate = parseFloat(document.getElementById('formHourlyRate').value) || 30;
    const durationLabel = document.getElementById('durationDisplay');
    const costTotal = document.getElementById('formEstimatedCost');

    if (durationLabel) durationLabel.textContent = `${hours} Hour${hours > 1 ? 's' : ''}`;
    if (costTotal) costTotal.textContent = `₹${hours * rate}`;
}

// Handle Reservation Form Submit (AJAX)
async function handleReserveSubmit(event) {
    event.preventDefault();
    const submitBtn = document.getElementById('btnReserveSubmit');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';

    const payload = {
        slot_number: document.getElementById('formSlotNumber').value,
        vehicle_number: document.getElementById('formVehicleNum').value.trim(),
        driver_name: document.getElementById('formDriverName').value.trim(),
        phone: document.getElementById('formPhone').value.trim(),
        vehicle_type: document.getElementById('formVehicleType').value,
        expected_hours: parseInt(document.getElementById('formHours').value)
    };

    try {
        const response = await fetch('/api/reserve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();

        if (response.ok && result.success) {
            closeModal('reserveModal');
            showToast(result.message, 'success');
            showReceipt(result.reservation, 'Booking Confirmation Pass');
        } else {
            showToast(result.message || 'Failed to reserve slot.', 'error');
        }
    } catch (err) {
        showToast('Error connecting to server. Please try again.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fa-solid fa-ticket"></i> Confirm & Book Pass';
    }
}

// Open Release Modal
function openReleaseModal(prefillIdentifier = '') {
    const input = document.getElementById('releaseIdentifier');
    if (input && prefillIdentifier) {
        input.value = prefillIdentifier;
    }
    openModal('releaseModal');
}

function quickReleasePrompt(slotNumber) {
    openReleaseModal(slotNumber);
}

// Handle Release Form Submit (AJAX)
async function handleReleaseSubmit(event) {
    event.preventDefault();
    const submitBtn = document.getElementById('btnReleaseSubmit');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';

    const identifier = document.getElementById('releaseIdentifier').value.trim();

    try {
        const response = await fetch('/api/release', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ identifier: identifier })
        });
        const result = await response.json();

        if (response.ok && result.success) {
            closeModal('releaseModal');
            showToast(result.message, 'success');
            if (result.summary) {
                showReceipt(result.summary, 'Parking Exit & Billing Receipt');
            } else {
                setTimeout(() => location.reload(), 1200);
            }
        } else {
            showToast(result.message || 'No matching active reservation found.', 'error');
        }
    } catch (err) {
        showToast('Error processing release. Please try again.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fa-solid fa-check-circle"></i> Confirm Exit & Release';
    }
}

// Display Generated Parking Pass / Receipt
function showReceipt(data, title) {
    const container = document.getElementById('receiptContent');
    if (!container) return;

    container.innerHTML = `
        <div class="receipt-ticket">
            <div class="receipt-header">
                <h4>${title}</h4>
                <span>Code: ${data.reservation_code || 'N/A'}</span>
            </div>
            <div class="receipt-row">
                <span class="r-label">Bay Number:</span>
                <span class="r-val">${data.slot_number}</span>
            </div>
            <div class="receipt-row">
                <span class="r-label">Vehicle Registration:</span>
                <span class="r-val">${data.vehicle_number}</span>
            </div>
            <div class="receipt-row">
                <span class="r-label">Driver Name:</span>
                <span class="r-val">${data.driver_name}</span>
            </div>
            <div class="receipt-row">
                <span class="r-label">Entry Timestamp:</span>
                <span class="r-val">${data.entry_time || 'Just now'}</span>
            </div>
            ${data.exit_time ? `
            <div class="receipt-row">
                <span class="r-label">Exit Timestamp:</span>
                <span class="r-val">${data.exit_time}</span>
            </div>` : ''}
            <div class="receipt-total">
                <span>Total Parking Fee:</span>
                <strong>₹${data.total_amount || 0}</strong>
            </div>
        </div>
    `;

    openModal('receiptModal');
}
