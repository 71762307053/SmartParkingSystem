// ParkSmart Admin Dashboard JavaScript

// Filter Reservations Table
function filterAdminTable() {
    const query = document.getElementById('adminTableSearch').value.toLowerCase().trim();
    const rows = document.querySelectorAll('#reservationsTable tbody tr.res-row');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(query)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Admin Force Release
async function adminForceRelease(slotNumber) {
    if (!confirm(`Are you sure you want to force-release and free up slot ${slotNumber}?`)) {
        return;
    }

    try {
        const res = await fetch('/api/admin/force-release', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ slot_number: slotNumber })
        });
        const data = await res.json();

        if (res.ok && data.success) {
            showToast(data.message, 'success');
            setTimeout(() => location.reload(), 800);
        } else {
            showToast(data.message || 'Failed to release slot.', 'error');
        }
    } catch (err) {
        showToast('Server communication error.', 'error');
    }
}

// Reset Entire System to Initial Seed State
async function confirmResetSystem() {
    const confirmation = prompt('Type "RESET" to confirm resetting all slots and reservation records:');
    if (confirmation !== 'RESET') {
        if (confirmation !== null) showToast('Reset cancelled. Confirmation text did not match.', 'warning');
        return;
    }

    try {
        const res = await fetch('/api/admin/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await res.json();

        if (res.ok && data.success) {
            showToast('System reset completed successfully.', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast('Reset failed.', 'error');
        }
    } catch (err) {
        showToast('Error sending reset command.', 'error');
    }
}
