import views.doctor_view as dv
import views.shared_view as shared_view
from models.prescription import Prescription

class DoctorController:
    def __init__(self, user, appointments, prescriptions, medicines, all_users, data_manager):
        self.current_user = user
        self.appointments = appointments
        self.prescriptions = prescriptions
        self.medicines = medicines
        self.data_manager = data_manager
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
        doctor_appointments = [
            app for app in self.appointments 
            if app.doctor_id == self.current_user.id
        ]
        dv.display_patient_queue(doctor_appointments, self.patients_map)

    def _create_prescription(self):
        """
        REVISI: Alur kerja baru untuk membuat resep.
        1. Dokter memilih pasien dari antrean.
        2. Dokter memasukkan detail obat untuk pasien tersebut.
        """
        # Langkah 1: Dapatkan daftar antrean khusus untuk dokter ini
        doctor_appointments = [
            app for app in self.appointments 
            if app.doctor_id == self.current_user.id
        ]
        
        # Langkah 2: Minta dokter memilih pasien dari antrean via view
        selected_appointment = dv.prompt_select_patient(doctor_appointments, self.patients_map)
        
        # Jika dokter tidak memilih atau tidak ada pasien, hentikan proses
        if not selected_appointment:
            return

        # Langkah 3: Minta dokter memasukkan detail obat via view
        selected_medicines = dv.prompt_for_medicines(self.medicines)

        if not selected_medicines:
            shared_view.display_error("Pembuatan resep dibatalkan karena tidak ada obat yang dipilih.")
            return

        # Langkah 4: Buat resep dan perbarui data
        new_prescription_id = (max([p.id for p in self.prescriptions], default=0) + 1)
        new_prescription = Prescription(
            pres_id=new_prescription_id,
            patient_id=selected_appointment.patient_id,
            doctor_id=self.current_user.id,
            medicines=selected_medicines,
            status='new'
        )
        self.prescriptions.append(new_prescription)
        self.data_manager.save_prescriptions(self.prescriptions)

        # Langkah 5: Ubah status appointment menjadi 'done' dan simpan
        selected_appointment.status = 'done'
        self.data_manager.save_appointments(self.appointments)
        
        patient_name = self.patients_map.get(selected_appointment.patient_id, "pasien")
        shared_view.display_success(f"Resep untuk {patient_name} (Antrean No. {selected_appointment.queue_number}) berhasil dibuat.")