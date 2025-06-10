import views.patient_view as pv
import views.shared_view as shared_view
from models.appointment import Appointment
from models.user import Doctor
from models.medicine import Medicine

class PatientController:
    # Terima 'all_medicines' dari AppController
    def __init__(self, user, all_users, appointments, prescriptions, all_medicines, data_manager):
        self.current_user = user
        self.all_users = all_users
        self.appointments = appointments
        self.prescriptions = prescriptions
        self.data_manager = data_manager
        self.doctors = [u for u in all_users if isinstance(u, Doctor)]
        
        # Buat map untuk pencarian nama yang efisien
        self.doctors_map = {doc.id: doc.username for doc in self.doctors}
        self.medicines_map = {med.id: med.name for med in all_medicines}

    def run(self):
        while True:
            choice = pv.display_patient_menu(self.current_user.username)
            if choice == '1':
                self.view_doctor_schedules()
            elif choice == '2':
                self.register_appointment()
            elif choice == '3':
                self.view_my_queue()
            elif choice == '4':
                # Panggil metode baru untuk menangani resep
                self._handle_prescriptions()
            elif choice == '5':
                break
            else:
                shared_view.display_error("Pilihan tidak valid.")

    def _handle_prescriptions(self):
        """Alur kerja untuk melihat dan mengajukan resep."""
        # 1. Filter resep hanya untuk pengguna saat ini
        my_prescriptions = [p for p in self.prescriptions if p.patient_id == self.current_user.id]

        # 2. Tampilkan semua resep yang dimiliki pasien
        pv.display_my_prescriptions(my_prescriptions, self.doctors_map, self.medicines_map)

        # 3. Filter resep yang masih baru (bisa diajukan)
        new_prescriptions = [p for p in my_prescriptions if p.status == 'new']
        
        # Jika tidak ada resep baru, cukup pause dan kembali
        if not new_prescriptions:
            print("\nTidak ada resep baru yang bisa diajukan.")
            shared_view.pause()
            return

        # 4. Minta pasien memilih resep mana yang akan diajukan
        pres_id_str = pv.prompt_submit_prescription(new_prescriptions)

        if not pres_id_str:
            return # Pengguna tidak memasukkan apa-apa, kembali ke menu

        try:
            pres_id_to_submit = int(pres_id_str)
            # Cari resep yang dipilih dari daftar resep BARU
            prescription = next((p for p in new_prescriptions if p.id == pres_id_to_submit), None)

            if prescription:
                # 5. Ubah status dan simpan
                prescription.status = 'submitted'
                self.data_manager.save_prescriptions(self.prescriptions)
                shared_view.display_success(f"Resep ID {prescription.id} berhasil diajukan ke apotek.")
            else:
                shared_view.display_error("ID Resep yang Anda masukkan tidak valid atau sudah pernah diajukan.")

        except ValueError:
            shared_view.display_error("Input harus berupa angka ID Resep.")

    def view_doctor_schedules(self):
        pv.display_doctor_schedules(self.doctors)

    def register_appointment(self):
        if any(app.patient_id == self.current_user.id and app.status == 'waiting' for app in self.appointments):
            shared_view.display_error("Anda sudah memiliki antrean aktif.")
            return
        
        pv.display_doctor_schedules(self.doctors)
        try:
            doc_id_str = pv.prompt_for_doctor_id()
            if not doc_id_str: return
            doc_id = int(doc_id_str)
        except ValueError:
            shared_view.display_error("ID Dokter harus berupa angka.")
            return

        doctor = next((doc for doc in self.doctors if doc.id == doc_id), None)
        if not doctor:
            shared_view.display_error("Dokter tidak ditemukan.")
            return

        queue_for_doctor = [app for app in self.appointments if app.doctor_id == doc_id and app.status == 'waiting']
        queue_number = len(queue_for_doctor) + 1
        
        new_app_id = (max([app.id for app in self.appointments], default=0) + 1)
        new_app = Appointment(new_app_id, self.current_user.id, doc_id, queue_number)
        self.appointments.append(new_app)
        
        self.data_manager.save_appointments(self.appointments)
        pv.display_queue_info(new_app, doctor)

    def view_my_queue(self):
        my_app = next((app for app in self.appointments if app.patient_id == self.current_user.id and app.status == 'waiting'), None)
        if my_app:
            doctor = next((doc for doc in self.doctors if doc.id == my_app.doctor_id), None)
            if doctor:
                pv.display_queue_info(my_app, doctor)
        else:
            shared_view.display_error("Anda tidak memiliki antrean aktif.")