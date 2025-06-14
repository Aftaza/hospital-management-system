from . import shared_view

def display_patient_menu(username):
    """Menampilkan menu utama untuk pasien."""
    shared_view.clear_screen()
    shared_view.display_header(f"Menu Pasien - Selamat Datang, {username}")
    print("1. Lihat Jadwal Dokter")
    print("2. Daftar Periksa Dokter")
    print("3. Lihat Antrean Saya")
    print("4. Lihat Resep Saya")
    print("5. Keluar")
    return input("Pilih opsi (1-5): ")

def display_doctor_schedules(doctors):
    """Menampilkan daftar jadwal dokter dalam format tabel."""
    shared_view.clear_screen()
    shared_view.display_header("Jadwal Dokter Tersedia")
    if not doctors:
        print("Saat ini tidak ada dokter yang tersedia.")
    else:
        print(f"{'ID':<5} {'Nama':<15} {'Spesialis':<15} {'Jadwal':<40}")
        print("-" * 80)
        for doc in doctors:
            print(f"{doc.id:<5} {doc.username:<15} {doc.specialty:<15} {doc.schedule:<40}")
    shared_view.pause()

def prompt_for_doctor_id():
    """Meminta input ID dokter dari pasien."""
    return input("Masukkan ID dokter pilihan Anda: ")

def display_queue_info(appointment, doctor):
    """Menampilkan informasi antrean setelah pendaftaran berhasil."""
    shared_view.clear_screen()
    shared_view.display_header("Informasi Pendaftaran")
    print("Pendaftaran Anda telah berhasil!")
    print(f"  Dokter      : Dr. {doctor.username}")
    print(f"  Nomor Antrean : {appointment.queue_number}")
    print(f"  Status        : {appointment.status.capitalize()}")
    shared_view.pause()

def display_no_active_queue():
    """Pesan jika pasien tidak memiliki antrean aktif."""
    print("\nAnda tidak memiliki antrean yang sedang aktif.")
    shared_view.pause()

def display_my_prescriptions(prescriptions, doctors_map, medicines_map):
    """Menampilkan daftar resep milik pasien dengan detail lengkap."""
    shared_view.clear_screen()
    shared_view.display_header("Riwayat Resep Anda")
    if not prescriptions:
        print("Anda belum memiliki resep.")
    else:
        # Urutkan dari yang terbaru
        sorted_prescriptions = sorted(prescriptions, key=lambda p: p.id, reverse=True)
        for pres in sorted_prescriptions:
            doctor_name = doctors_map.get(pres.doctor_id, "Dokter Tidak Dikenal")
            print("-" * 50)
            print(f"Resep ID: {pres.id} | Dokter: {doctor_name}")
            print(f"Status  : {pres.status.upper()}")
            print("Detail Obat:")
            for med_id, qty in pres.medicines.items():
                med_name = medicines_map.get(med_id, "Obat Tidak Dikenal")
                print(f"  - {med_name:<25} : {qty} buah")
            print("-" * 50)

def prompt_submit_prescription(new_prescriptions):
    """
    Menampilkan resep baru dan meminta pasien memilih mana yang akan diajukan.
    """
    print("\nAnda memiliki resep baru yang belum diajukan:")
    if not new_prescriptions:
        print("Tidak ada resep baru yang bisa diajukan saat ini.")
        shared_view.pause()
        return None
    
    print(f"{'ID Resep':<15} {'Dokter':<20}")
    print("-" * 35)
    # Tampilkan resep yang bisa diajukan (status 'new')
    for pres in new_prescriptions:
        # Note: Untuk view ini kita tidak perlu nama dokter, hanya ID
        print(f"{pres.id:<15}")

    choice = input("\nMasukkan ID Resep yang ingin diajukan ke apotek (atau biarkan kosong untuk kembali): ")
    return choice