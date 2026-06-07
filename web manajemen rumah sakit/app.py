from flask import Flask, render_template, request, redirect, url_for, flash
import random

app = Flask(__name__, template_folder='templates')
app.secret_key = 'kuncirahasiatubesalprosemesterdua'

# ==============================================================================
# 1. OPERASI ARRAY & STRUKTUR DATA (BACKEND PYTHON)
# ==============================================================================

# [Materi: Operasi Array / List] - Menyimpan data master Poliklinik
POLI_ARRAY = ["Umum", "Gigi", "Anak", "Jantung"]

# [Materi: Enqueue & Dequeue (Queue - FIFO)] - Antrean Pasien
queue_patients = [
    {"id": "P-101", "name": "Rizky Ramadhan", "dept": "Umum"},
    {"id": "P-102", "name": "Siti Rahma", "dept": "Gigi"}
]

# [Materi: Push & Pop (Stack - LIFO)] - Tumpukan Obat Apotek
prescription_stack = [
    {"name": "Paracetamol 500mg", "qty": 10},
    {"name": "Amoxicillin 500mg", "qty": 15}
]

# [Materi: Sorting Algorithm & Array Manipulation] - Triase UGD (Makin kecil angka, makin kritis)
ugd_patients = [
    {"name": "Budi", "illness": "Asma Berat", "priority": 3},
    {"name": "Guntur", "illness": "Gagal Jantung Akut", "priority": 1},
    {"name": "Aulia", "illness": "Luka Gores", "priority": 5},
    {"name": "Hendra", "illness": "Patah Tulang", "priority": 2}
]

# [Materi: Double Linked List] - Rekam Medis Pasien dengan Pointer Memori Simulasi
class DLLNode:
    def __init__(self, mr_id, name, diagnosis, address_hex):
        self.id = mr_id
        self.name = name
        self.diagnosis = diagnosis
        self.address = address_hex
        self.prev_address = "NULL"
        self.next_address = "NULL"

# Membuat data contoh linked list secara manual menggunakan array of dictionary agar mudah dilempar ke HTML
medical_records = [
    {"addr": "0x4A12", "id": "MR-209", "name": "Aulia Rasyid", "diag": "Demam Berdarah", "prev": "NULL", "next": "0x5B3F"},
    {"addr": "0x5B3F", "id": "MR-301", "name": "Guntur Baskoro", "diag": "Gastritis Kronis", "prev": "0x4A12", "next": "0x6C7A"},
    {"addr": "0x6C7A", "id": "MR-412", "name": "Hendra Wijaya", "diag": "Cedera Ligamen", "prev": "0x5B3F", "next": "NULL"}
]

# ==============================================================================
# 2. FUNGSI REKURSIF (BACKEND LOGIC)
# ==============================================================================
# [Materi: Fungsi Rekursif] - Menghitung potongan asuransi bertingkat (Diskon 10% setiap lapisan)
def hitung_subsidi_rekursif(biaya, layer, log_list, current_layer=1):
    potongan = biaya * 0.10
    biaya_baru = biaya - potongan
    log_list.append(f"Layer {current_layer}: Rp {biaya:,.2f} -> Dipotong 10% (Rp {potongan:,.2f}) -> Sisa: Rp {biaya_baru:,.2f}")
    
    if current_layer >= layer:
        return biaya_baru
    return hitung_subsidi_rekursif(biaya_baru, layer, log_list, current_layer + 1)

# ==============================================================================
# 3. ROUTING / NAVIGASI WEB
# ==============================================================================

@app.route('/')
def index():
    # Menghitung nominal awal kalkulator jika ada di argument URL
    biaya_awal = request.args.get('biaya_awal', type=float)
    layer = request.args.get('layer', type=int)
    rekursif_logs = []
    biaya_akhir = None
    
    if biaya_awal and layer:
        biaya_akhir = hitung_subsidi_rekursif(biaya_awal, layer, rekursif_logs)

    return render_template('index.html', 
                           polis=POLI_ARRAY,
                           queue=queue_patients, 
                           stack=reversed(prescription_stack),
                           ugd=ugd_patients,
                           records=medical_records,
                           rekursif_logs=rekursif_logs,
                           biaya_akhir=biaya_akhir,
                           biaya_awal=biaya_awal,
                           layer_count=layer)

# --- Aksi Queue ---
@app.route('/enqueue', methods=['POST'])
def enqueue():
    name = request.form.get('patient_name')
    dept = request.form.get('dept_name')
    if name and dept:
        new_id = f"P-{random.randint(103, 999)}"
        queue_patients.append({"id": new_id, "name": name, "dept": dept})
        flash(f"Pasien {name} masuk antrean (Enqueue)!", "success")
    return redirect(url_for('index'))

@app.route('/dequeue')
def dequeue():
    if queue_patients:
        p = queue_patients.pop(0)
        flash(f"🔊 Panggilan Loket: Pasien {p['name']} silakan masuk ke Poli {p['dept']} (Dequeue).", "info")
    else:
        flash("Antrean kosong!", "warning")
    return redirect(url_for('index'))

# --- Aksi Stack ---
@app.route('/push', methods=['POST'])
def push():
    name = request.form.get('med_name')
    qty = request.form.get('qty')
    if name and qty.isdigit():
        prescription_stack.append({"name": name, "qty": int(qty)})
        flash(f"Resep {name} ditambahkan ke tumpukan teratas (Push)!", "success")
    return redirect(url_for('index'))

@app.route('/pop')
def pop():
    if prescription_stack:
        removed = prescription_stack.pop()
        flash(f"🗑️ Pembatalan: Obat {removed['name']} dikeluarkan dari tumpukan (Pop).", "danger")
    else:
        flash("Tumpukan obat kosong!", "warning")
    return redirect(url_for('index'))

# --- Aksi Sorting ---
@app.route('/sort_ugd')
def sort_ugd():
    # [Materi: Sorting Algorithm] - Menggunakan algoritma BUBBLE SORT untuk mengurutkan tingkat prioritas UGD
    n = len(ugd_patients)
    for i in range(n):
        for j in range(0, n-i-1):
            if ugd_patients[j]["priority"] > ugd_patients[j+1]["priority"]:
                # Tukar posisi data jika prioritasnya lebih besar (angka kecil = prioritas utama)
                ugd_patients[j], ugd_patients[j+1] = ugd_patients[j+1], ugd_patients[j]
    flash("Pasien UGD berhasil diurutkan berdasarkan tingkat kekritisan menggunakan Bubble Sort!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)