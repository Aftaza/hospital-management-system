from . import shared_view

def display_doctor_menu(username):
    """Menampilkan menu utama untuk dokter."""
    shared_view.clear_screen()
    shared_view.display_header(f"Menu Dokter - Selamat Datang, Dr. {username}")
    print("1. Lihat Antrean Pasien")
    print("2. Buat Resep untuk Pasien")
    print("3. Keluar")
    return input("Pilih opsi (1-3): ")

def display_patient_queue(appointments, patients_map):
    """Menampilkan daftar antrean pasien untuk dokter."""
    shared_view.clear_screen()
    shared_view.display_header("Antrean Pasien Hari Ini")
    if not appointments:
        print("Tidak ada pasien dalam antrean.")
    else:
        print(f"{'No. Antrean':<15} {'Nama Pasien':<20} {'Status':<15}")
        print("-" * 50)
        # Mengurutkan berdasarkan nomor antrean
        sorted_apps = sorted(appointments, key=lambda x: x.queue_number)
        for app in sorted_apps:
            patient_name = patients_map.get(app.patient_id, "Nama Tidak Ditemukan")
            print(f"{app.queue_number:<15} {patient_name:<20} {app.status.capitalize():<15}")
    shared_view.pause()

def prompt_create_prescription(medicines):
    """Menampilkan form interaktif untuk membuat resep."""
    shared_view.clear_screen()
    shared_view.display_header("Buat Resep Baru")
    
    patient_id = input("Masukkan ID Pasien yang diperiksa: ")
    
    selected_medicines = {}
    while True:
        print("\n--- Daftar Obat Tersedia ---")
        print(f"{'ID':<5} {'Nama Obat':<20} {'Stok':<10}")
        print("-" * 40)
        for med in medicines:
            print(f"{med.id:<5} {med.name:<20} {med.stock:<10}")
        
        med_id = input("\nMasukkan ID Obat (atau ketik 'selesai' untuk mengakhiri): ")
        if med_id.lower() == 'selesai':
            break
        
        quantity = input(f"Masukkan jumlah untuk obat ID {med_id}: ")
        
        try:
            selected_medicines[int(med_id)] = int(quantity)
            print("Obat ditambahkan.")
        except ValueError:
            print("[ERROR] ID dan jumlah harus berupa angka.")

    return patient_id, selected_medicines