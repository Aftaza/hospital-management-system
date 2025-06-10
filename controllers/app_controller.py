import pandas as pd
from models.user import Patient, Doctor, Staff
from models.medicine import Medicine
from models.appointment import Appointment
from models.prescription import Prescription

# Impor controller dan data manager
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from controllers.staff_controller import StaffController
from utils.data_manager import DataManager

class AppController:
    def __init__(self):
        self.data_manager = DataManager()
        self._load_data()
        self.current_user = None

    def _load_data(self):
        """Loads data using DataManager and handles potential errors."""
        try:
            # Load users
            users_df = pd.read_csv(self.data_manager.users_path)
            self.users = []
            for _, row in users_df.iterrows():
                if row['role'] == 'pasien':
                    self.users.append(Patient(row['id'], row['username'], row['password']))
                elif row['role'] == 'dokter':
                    self.users.append(Doctor(row['id'], row['username'], row['password'], row['specialty'], row['schedule']))
                elif row['role'] == 'staff':
                    self.users.append(Staff(row['id'], row['username'], row['password']))

            # Load medicines
            meds_df = pd.read_csv(self.data_manager.medicines_path)
            self.medicines = [Medicine(row['id'], row['name'], row['stock']) for _, row in meds_df.iterrows()]

            # Load appointments and prescriptions, handle if they don't exist yet
            try:
                app_df = pd.read_csv(self.data_manager.appointments_path)
                self.appointments = [Appointment(row['id'], row['patient_id'], row['doctor_id'], row['queue_number'], row['status']) for _, row in app_df.iterrows()]
            except FileNotFoundError:
                self.appointments = []

            try:
                pres_df = pd.read_csv(self.data_manager.prescriptions_path)
                # Helper function to parse medicine string "1:2;3:1" back to dict
                def parse_medicines(med_str):
                    if not isinstance(med_str, str): return {}
                    parts = med_str.split(';')
                    return {int(p.split(':')[0]): int(p.split(':')[1]) for p in parts if ':' in p}
                self.prescriptions = [Prescription(row['id'], row['patient_id'], row['doctor_id'], parse_medicines(row['medicines']), row['status']) for _, row in pres_df.iterrows()]
            except FileNotFoundError:
                self.prescriptions = []

        except FileNotFoundError as e:
            print(f"[ERROR] Critical file not found: {e}. Please run generate_data.py")
            exit()
            
    def _login(self):
        print("\n--- Selamat Datang di Sistem Rumah Sakit ---")
        username = input("Username: ")
        password = input("Password: ")
        
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                print(f"\nLogin berhasil! Selamat datang, {user.username} ({user.role})")
                return True
        print("Username atau password salah.")
        return False

    def run(self):
        if not self._login():
            return

        # Pass the data_manager instance to the specific controllers
        if self.current_user.role == 'pasien':
            controller = PatientController(self.current_user, self.users, self.appointments, self.prescriptions, self.medicines, self.data_manager)
            controller.run()
        elif self.current_user.role == 'dokter':
            controller = DoctorController(self.current_user, self.appointments, self.prescriptions, self.medicines, self.users, self.data_manager)
            controller.run()
        elif self.current_user.role == 'staff':
            controller = StaffController(self.current_user, self.prescriptions, self.medicines, self.users, self.data_manager)
            controller.run()
            
        print("\nAnda telah keluar dari sistem.")