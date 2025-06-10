import views.staff_view as sv
import views.shared_view as shared_view

class StaffController:
    def __init__(self, user, prescriptions, medicines, all_users):
        """
        Inisialisasi StaffController.

        Args:
            user (Staff): Objek staff yang sedang login.
            prescriptions (list): Daftar semua objek resep.
            medicines (list): Daftar semua objek obat.
            all_users (list): Daftar semua objek pengguna.
        """
        self.current_user = user
        self.prescriptions = prescriptions
        self.medicines = medicines
        # Membuat 'map' untuk pencarian data yang efisien
        self.patients_map = {u.id: u.username for u in all_users if u.role == 'pasien'}
        self.medicines_map = {m.id: m.name for m in self.medicines}
        self.medicine_objects = {m.id: m for m in self.medicines}

    def run(self):
        """Menjalankan loop utama untuk menu staff."""
        while True:
            choice = sv.display_staff_menu(self.current_user.username)
            if choice == '1':
                self._process_prescription_requests()
            elif choice == '2':
                self._manage_stock()
            elif choice == '3':
                break
            else:
                shared_view.display_error("Pilihan tidak valid.")

    def _process_prescription_requests(self):
        """Menampilkan dan memproses permintaan resep."""
        # Menampilkan semua resep yang berstatus 'submitted'
        sv.display_prescription_requests(self.prescriptions, self.patients_map, self.medicines_map)
        
        pres_id_str = sv.prompt_process_prescription()
        if not pres_id_str:
            return # Kembali ke menu jika tidak ada input

        try:
            pres_id = int(pres_id_str)
        except ValueError:
            shared_view.display_error("ID Resep harus berupa angka.")
            return

        # Cari resep yang akan diproses
        prescription = next((p for p in self.prescriptions if p.id == pres_id), None)
        if not prescription:
            shared_view.display_error("Resep tidak ditemukan.")
            return
        
        if prescription.status != 'submitted':
            shared_view.display_error(f"Resep ini tidak bisa diproses (Status saat ini: {prescription.status.upper()}).")
            return
            
        # Logika Pengecekan Stok
        can_fulfill = True
        for med_id, required_qty in prescription.medicines.items():
            medicine_obj = self.medicine_objects.get(med_id)
            if not medicine_obj or medicine_obj.stock < required_qty:
                can_fulfill = False
                shared_view.display_error(f"Stok untuk {self.medicines_map.get(med_id, 'N/A')} tidak mencukupi.")
                break
        
        # Update status dan stok jika memungkinkan
        if can_fulfill:
            for med_id, required_qty in prescription.medicines.items():
                self.medicine_objects[med_id].stock -= required_qty
            prescription.status = 'fulfilled'
            shared_view.display_success("Resep berhasil dipenuhi dan stok telah dikurangi.")
        else:
            prescription.status = 'pending'
            shared_view.display_success("Stok tidak cukup. Status resep diubah menjadi 'pending'.")

    def _manage_stock(self):
        """Menampilkan sub-menu untuk melihat dan memperbarui stok obat."""
        while True:
            sv.display_medicine_stock(self.medicines)
            choice = input("\nKetik 'update' untuk mengubah stok, atau 'kembali' untuk ke menu utama: ").lower()

            if choice == 'kembali':
                break
            elif choice == 'update':
                med_id_str, new_stock_str = sv.prompt_update_stock()
                try:
                    med_id = int(med_id_str)
                    new_stock = int(new_stock_str)
                except ValueError:
                    shared_view.display_error("ID dan Stok harus berupa angka.")
                    continue

                medicine_to_update = self.medicine_objects.get(med_id)
                if medicine_to_update:
                    medicine_to_update.stock = new_stock
                    shared_view.display_success(f"Stok untuk {medicine_to_update.name} berhasil diubah menjadi {new_stock}.")
                else:
                    shared_view.display_error("Obat dengan ID tersebut tidak ditemukan.")
            else:
                shared_view.display_error("Pilihan tidak valid.")