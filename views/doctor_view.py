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
        print(f"{'No. Antrean':<15} {'ID Pasien':<15} {'Nama Pasien':<20} {'Status':<15}")
        print("-" * 65)
        # Mengurutkan berdasarkan nomor antrean
        sorted_apps = sorted(appointments, key=lambda x: x.queue_number)
        for app in sorted_apps:
            patient_name = patients_map.get(app.patient_id, "Nama Tidak Ditemukan")
            print(f"{app.queue_number:<15} {app.patient_id:<15} {patient_name:<20} {app.status.capitalize():<15}")
    shared_view.pause()

def prompt_select_patient(appointments, patients_map):
    """
    Menampilkan antrean pasien dan meminta dokter untuk memilih satu.
    Mengembalikan objek appointment yang dipilih.
    """
    shared_view.clear_screen()
    shared_view.display_header("Pilih Pasien dari Antrean")
    
    # Tampilkan antrean yang menunggu saja
    waiting_patients = [app for app in appointments if app.status == 'waiting']
    
    if not waiting_patients:
        print("Tidak ada pasien yang sedang menunggu.")
        shared_view.pause()
        return None

    print(f"{'No. Antrean':<15} {'ID Pasien':<15} {'Nama Pasien':<20}")
    print("-" * 50)
    sorted_apps = sorted(waiting_patients, key=lambda x: x.queue_number)
    for app in sorted_apps:
        patient_name = patients_map.get(app.patient_id, "Nama Tidak Ditemukan")
        print(f"{app.queue_number:<15} {app.patient_id:<15} {patient_name:<20}")
    
    try:
        queue_num_str = input("\nMasukkan Nomor Antrean pasien yang akan dibuatkan resep: ")
        if not queue_num_str: return None
        
        queue_num = int(queue_num_str)
        # Cari appointment berdasarkan nomor antrean yang dipilih
        selected_appointment = next((app for app in sorted_apps if app.queue_number == queue_num), None)
        
        if not selected_appointment:
            print("[ERROR] Nomor antrean tidak ditemukan.")
            shared_view.pause()
            return None
            
        return selected_appointment
        
    except ValueError:
        print("[ERROR] Input harus berupa angka.")
        shared_view.pause()
        return None

def prompt_for_medicines(medicines):
    """Menampilkan form interaktif untuk memilih obat dan jumlahnya."""
    shared_view.clear_screen()
    shared_view.display_header("Masukkan Detail Obat")
    
    selected_medicines = {}
    while True:
        print("\n--- Daftar Obat Tersedia ---")
        print(f"{'ID':<5} {'Nama Obat':<25} {'Stok':<10}")
        print("-" * 45)
        for med in medicines:
            print(f"{med.id:<5} {med.name:<25} {med.stock:<10}")
        
        med_id = input("\nMasukkan ID Obat (atau ketik 'selesai' untuk mengakhiri): ")
        if med_id.lower() == 'selesai':
            break
        
        quantity = input(f"Masukkan jumlah untuk obat ID {med_id}: ")
        
        try:
            # Validasi sederhana
            med_id_int = int(med_id)
            quantity_int = int(quantity)
            
            # Cek apakah obat ada
            if not any(med.id == med_id_int for med in medicines):
                print("[ERROR] ID Obat tidak ditemukan.")
                continue

            selected_medicines[med_id_int] = quantity_int
            print("=> Obat ditambahkan.")
        except ValueError:
            print("[ERROR] ID dan jumlah harus berupa angka.")

    return selected_medicines