import views.doctor_view as dv
import views.shared_view as shared_view
from models.prescription import Prescription

class DoctorController:
    def __init__(self, user, appointments, prescriptions, medicines, all_users):
        """
        Inisialisasi DoctorController.
        
        Args:
            user (Doctor): Objek dokter yang sedang login.
            appointments (list): Daftar semua objek appointment.
            prescriptions (list): Daftar semua objek resep.
            medicines (list): Daftar semua objek obat.
            all_users (list): Daftar semua objek pengguna untuk mencari nama.
        """
        self.current_user = user
        self.appointments = appointments
        self.prescriptions = prescriptions
        self.medicines = medicines
        # Membuat 'map' untuk pencarian nama pasien yang efisien
        self.patients_map = {u.id: u.username for u in all_users if u.role == 'pasien'}

    def run(self):
        """Menjalankan loop utama untuk menu dokter."""
        while True:
            choice = dv.display_doctor_menu(self.current_user.username)
            if choice == '1':
                self._view_patient_queue()
            elif choice == '2':
                self._create_prescription()
            elif choice == '3':
                break
            else:
                shared_view.display_error("Pilihan tidak valid.")

    def _view_patient_queue(self):
        """Menampilkan daftar pasien yang mengantre untuk dokter ini."""
        # Filter appointment hanya untuk dokter yang sedang login dan yang belum selesai
        doctor_appointments = [
            app for app in self.appointments 
            if app.doctor_id == self.current_user.id and app.status != 'done'
        ]
        
        dv.display_patient_queue(doctor_appointments, self.patients_map)

    def _create_prescription(self):
        """Memandu dokter melalui proses pembuatan resep."""
        # Meminta input dari dokter melalui view
        patient_id_str, selected_medicines = dv.prompt_create_prescription(self.medicines)
        
        # Validasi input
        if not patient_id_str:
            shared_view.display_error("ID Pasien tidak boleh kosong.")
            return
            
        try:
            patient_id = int(patient_id_str)
        except ValueError:
            shared_view.display_error("ID Pasien harus berupa angka.")
            return

        if patient_id not in self.patients_map:
            shared_view.display_error("Pasien dengan ID tersebut tidak ditemukan.")
            return

        if not selected_medicines:
            shared_view.display_error("Resep harus berisi setidaknya satu obat.")
            return

        # Proses pembuatan resep
        # 1. Buat objek resep baru
        new_prescription_id = len(self.prescriptions) + 1
        new_prescription = Prescription(
            pres_id=new_prescription_id,
            patient_id=patient_id,
            doctor_id=self.current_user.id,
            medicines=selected_medicines,
            status='new' # Status awal: 'new', akan diubah pasien menjadi 'submitted'
        )
        self.prescriptions.append(new_prescription)

        # 2. Tandai appointment pasien tersebut sebagai 'done'
        appointment_to_update = next((
            app for app in self.appointments 
            if app.patient_id == patient_id and app.doctor_id == self.current_user.id and app.status == 'waiting'
        ), None)
        
        if appointment_to_update:
            appointment_to_update.status = 'done'
        
        shared_view.display_success(f"Resep untuk pasien {self.patients_map[patient_id]} berhasil dibuat.")