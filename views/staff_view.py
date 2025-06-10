from . import shared_view

def display_staff_menu(username):
    """Menampilkan menu utama untuk staff."""
    shared_view.clear_screen()
    shared_view.display_header(f"Menu Staff - Selamat Datang, {username}")
    print("1. Lihat Permintaan Resep")
    print("2. Kelola Stok Obat")
    print("3. Keluar")
    return input("Pilih opsi (1-3): ")

def display_prescription_requests(prescriptions, patients_map, medicines_map):
    """Menampilkan daftar resep yang perlu diproses."""
    shared_view.clear_screen()
    shared_view.display_header("Permintaan Resep Pasien")
    
    # Filter hanya resep yang diajukan (status 'new')
    pending_prescriptions = [p for p in prescriptions if p.status == 'submitted']

    if not pending_prescriptions:
        print("Tidak ada permintaan resep baru.")
    else:
        for pres in pending_prescriptions:
            patient_name = patients_map.get(pres.patient_id, "Nama Tidak Dikenal")
            print(f"\n--- Resep ID: {pres.id} | Pasien: {patient_name} ---")
            for med_id, qty in pres.medicines.items():
                med_name = medicines_map.get(med_id, "Obat Tidak Dikenal")
                print(f"  - {med_name}: {qty} buah")
    shared_view.pause()

def prompt_process_prescription():
    """Meminta ID resep yang akan diproses oleh staff."""
    return input("\nMasukkan ID Resep yang akan diproses: ")

def display_medicine_stock(medicines):
    """Menampilkan stok semua obat."""
    shared_view.clear_screen()
    shared_view.display_header("Manajemen Stok Obat")
    print(f"{'ID':<5} {'Nama Obat':<25} {'Stok Saat Ini':<15}")
    print("-" * 50)
    for med in medicines:
        print(f"{med.id:<5} {med.name:<25} {med.stock:<15}")
    print("-" * 50)

def prompt_update_stock():
    """Meminta input untuk memperbarui stok obat."""
    medicine_id = input("Masukkan ID Obat yang akan diupdate: ")
    new_stock = input(f"Masukkan jumlah stok baru untuk obat ID {medicine_id}: ")
    return medicine_id, new_stock