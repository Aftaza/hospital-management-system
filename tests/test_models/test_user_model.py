import unittest
# Menambahkan path proyek ke sys.path agar bisa mengimpor dari folder models
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User, Patient, Doctor, Staff

class TestUserModels(unittest.TestCase):

    def test_create_patient(self):
        """Menguji pembuatan objek Patient dan pewarisan dari User."""
        # Arrange
        patient = Patient(user_id=1, username='pasien_test', password='pw')
        
        # Assert
        self.assertIsInstance(patient, Patient)
        self.assertIsInstance(patient, User)
        self.assertEqual(patient.id, 1)
        self.assertEqual(patient.username, 'pasien_test')
        self.assertEqual(patient.password, 'pw')
        self.assertEqual(patient.role, 'pasien') # Atribut role harus otomatis terisi

    def test_create_doctor(self):
        """Menguji pembuatan objek Doctor dan atribut spesifiknya."""
        # Arrange
        doctor = Doctor(
            user_id=2, 
            username='dokter_test', 
            password='pw_doc', 
            specialty='Jantung', 
            schedule='Senin 09:00-12:00'
        )

        # Assert
        self.assertIsInstance(doctor, Doctor)
        self.assertIsInstance(doctor, User)
        self.assertEqual(doctor.id, 2)
        self.assertEqual(doctor.username, 'dokter_test')
        self.assertEqual(doctor.role, 'dokter')
        self.assertEqual(doctor.specialty, 'Jantung')
        self.assertEqual(doctor.schedule, 'Senin 09:00-12:00')

    def test_create_staff(self):
        """Menguji pembuatan objek Staff."""
        # Arrange
        staff = Staff(user_id=3, username='staff_test', password='pw_staff')

        # Assert
        self.assertIsInstance(staff, Staff)
        self.assertIsInstance(staff, User)
        self.assertEqual(staff.id, 3)
        self.assertEqual(staff.username, 'staff_test')
        self.assertEqual(staff.role, 'staff')