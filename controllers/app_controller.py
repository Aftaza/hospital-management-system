import pandas as pd
from models.user import Patient, Doctor, Staff
from models.medicine import Medicine
from models.appointment import Appointment
from models.prescription import Prescription

# Impor controller spesifik
from .patient_controller import PatientController
from .doctor_controller import DoctorController
from .staff_controller import StaffController

class AppController:
    def __init__(self):
        # Memuat semua data saat aplikasi dimulai
        self._load_data()
        self.current_user = None

    def _load_data(self):
        # Logika untuk memuat semua CSV ke dalam list of objects
        # Menggunakan _ di awal nama fungsi menandakan ini untuk penggunaan internal kelas
        users_df = pd.read_csv('data/users.csv')
        self.users = []
        for _, row in users_df.iterrows():
            if row['role'] == 'pasien':
                self.users.append(Patient(row['id'], row['username'], row['password']))
            elif row['role'] == 'dokter':
                self.users.append(Doctor(row['id'], row['username'], row['password'], row['specialty'], row['schedule']))
            elif row['role'] == 'staff':
                self.users.append(Staff(row['id'], row['username'], row['password']))
        
        meds_df = pd.read_csv('data/medicines.csv')
        self.medicines = [Medicine(row['id'], row['name'], row['stock']) for _, row in meds_df.iterrows()]
        
        # Data transaksional, bisa di-load dari CSV jika sudah ada
        self.appointments = [] 
        self.prescriptions = []

    def _login(self):
        print("--- Selamat Datang di Sistem Rumah Sakit ---")
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

        # Delegasi ke controller yang sesuai berdasarkan peran
        if self.current_user.role == 'pasien':
            # Membuat instance PatientController dan memberikan data yang diperlukan
            controller = PatientController(self.current_user, self.users, self.appointments, self.prescriptions)
            controller.run()
        elif self.current_user.role == 'dokter':
            controller = DoctorController(self.current_user, self.appointments, self.prescriptions, self.medicines)
            controller.run()
        elif self.current_user.role == 'staff':
            controller = StaffController(self.current_user, self.prescriptions, self.medicines)
            controller.run()
            
        print("\nAnda telah keluar dari sistem.")