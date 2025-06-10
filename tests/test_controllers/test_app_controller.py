import unittest
from unittest.mock import patch, MagicMock

# Menambahkan path proyek agar bisa impor dari folder lain
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.app_controller import AppController
from models.user import Patient, Doctor, Staff

class TestAppController(unittest.TestCase):

    def setUp(self):
        """Setup yang berjalan sebelum setiap tes."""
        # Kita mock metode _load_data agar tidak membaca file CSV sungguhan
        with patch.object(AppController, '_load_data', return_value=None):
            self.app = AppController()
            # Buat data mock secara manual
            self.app.users = [
                Patient(user_id=1, username='pasien1', password='pw1'),
                Doctor(user_id=2, username='dokter1', password='pw2', specialty='Umum', schedule='Senin'),
                Staff(user_id=3, username='staff1', password='pw3')
            ]
            # Inisialisasi atribut yang hilang yang seharusnya dibuat oleh _load_data
            self.app.appointments = []  # <-- PERBAIKAN DITAMBAHKAN
            self.app.prescriptions = [] # <-- PERBAIKAN DITAMBAHKAN
            self.app.medicines = []     # <-- PERBAIKAN DITAMBAHKAN

    @patch('builtins.input', side_effect=['pasien1', 'pw1'])
    def test_login_success(self, mock_input):
        """Menguji login berhasil."""
        # Act
        result = self.app._login()
        # Assert
        self.assertTrue(result)
        self.assertEqual(self.app.current_user.username, 'pasien1')

    @patch('builtins.input', side_effect=['salah', 'salah'])
    def test_login_failure(self, mock_input):
        """Menguji login gagal."""
        # Act
        result = self.app._login()
        # Assert
        self.assertFalse(result)
        self.assertIsNone(self.app.current_user)

    @patch('controllers.app_controller.PatientController')
    @patch('builtins.input', side_effect=['pasien1', 'pw1'])
    def test_run_delegates_to_patient_controller(self, mock_input, mock_patient_controller):
        """Menguji delegasi ke PatientController saat pasien login."""
        # Act
        self.app.run()
        # Assert
        # Pastikan PatientController dipanggil
        mock_patient_controller.assert_called_once()
        # Pastikan metode run() dari instance PatientController dipanggil
        mock_patient_controller.return_value.run.assert_called_once()
        
    @patch('controllers.app_controller.DoctorController')
    @patch('builtins.input', side_effect=['dokter1', 'pw2'])
    def test_run_delegates_to_doctor_controller(self, mock_input, mock_doctor_controller):
        """Menguji delegasi ke DoctorController saat dokter login."""
        self.app.run()
        mock_doctor_controller.assert_called_once()
        mock_doctor_controller.return_value.run.assert_called_once()

    @patch('controllers.app_controller.StaffController')
    @patch('builtins.input', side_effect=['staff1', 'pw3'])
    def test_run_delegates_to_staff_controller(self, mock_input, mock_staff_controller):
        """Menguji delegasi ke StaffController saat staff login."""
        self.app.run()
        mock_staff_controller.assert_called_once()
        mock_staff_controller.return_value.run.assert_called_once()