import views.patient_view as pv
from models.appointment import Appointment
from models.user import Doctor

class PatientController:
    def __init__(self, user, all_users, appointments, prescriptions):
        # Menerima data dari AppController, bukan memuatnya sendiri
        self.current_user = user
        self.all_users = all_users
        self.appointments = appointments
        self.prescriptions = prescriptions
        self.doctors = [u for u in self.all_users if isinstance(u, Doctor)]

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
                # Logika untuk mengajukan resep
                print("Fitur belum diimplementasikan.")
            elif choice == '5':
                break
            else:
                print("Pilihan tidak valid.")

    def view_doctor_schedules(self):
        pv.display_doctor_schedules(self.doctors)

    def register_appointment(self):
        self.view_doctor_schedules()
        try:
            doc_id = int(input("Masukkan ID dokter pilihan: "))
        except ValueError:
            print("ID Dokter harus berupa angka.")
            return

        doctor = next((doc for doc in self.doctors if doc.id == doc_id), None)
        if not doctor:
            print("Dokter tidak ditemukan.")
            return

        queue_for_doctor = [app for app in self.appointments if app.doctor_id == doc_id]
        queue_number = len(queue_for_doctor) + 1
        
        new_app_id = len(self.appointments) + 1
        new_app = Appointment(new_app_id, self.current_user.id, doc_id, queue_number)
        self.appointments.append(new_app)
        
        pv.display_queue_info(new_app, doctor)

    def view_my_queue(self):
        my_app = next((app for app in self.appointments if app.patient_id == self.current_user.id and app.status == 'waiting'), None)
        if my_app:
            doctor = next((doc for doc in self.doctors if doc.id == my_app.doctor_id), None)
            pv.display_queue_info(my_app, doctor)
        else:
            print("Anda tidak memiliki antrean aktif.")