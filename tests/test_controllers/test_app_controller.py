import unittest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.app_controller import AppController
from models.user import Patient, Doctor, Staff
from utils.data_manager import DataManager

class TestAppController(unittest.TestCase):

    def setUp(self):
        """Setup yang berjalan sebelum setiap tes."""
        # Mock DataManager agar tidak ada I/O disk sungguhan
        self.mock_data_manager_instance = MagicMock(spec=DataManager)

        # Patch constructor DataManager agar mengembalikan instance mock kita
        patcher = patch('controllers.app_controller.DataManager', return_value=self.mock_data_manager_instance)
        self.addCleanup(patcher.stop)
        patcher.start()

        # Mock metode _load_data agar tidak membaca file CSV
        with patch.object(AppController, '_load_data', return_value=None):
            self.app = AppController()
            # Buat data mock secara manual
            self.app.users = [
                Patient(user_id=1, username='pasien1', password='pw1'),
                Doctor(user_id=2, username='dokter1', password='pw2', specialty='Umum', schedule='Senin'),
                Staff(user_id=3, username='staff1', password='pw3')
            ]
            self.app.medicines = []
            self.app.appointments = []
            self.app.prescriptions = []

    @patch('builtins.input', side_effect=['pasien1', 'pw1'])
    def test_login_success(self, mock_input):
        self.assertTrue(self.app._login())
        self.assertEqual(self.app.current_user.username, 'pasien1')

    @patch('builtins.input', side_effect=['salah', 'salah'])
    def test_login_failure(self, mock_input):
        self.assertFalse(self.app._login())
        self.assertIsNone(self.app.current_user)

    @patch('controllers.app_controller.PatientController')
    @patch('builtins.input', side_effect=['pasien1', 'pw1'])
    def test_run_delegates_to_patient_controller(self, mock_input, mock_patient_controller):
        """Menguji delegasi ke PatientController dengan argumen yang benar."""
        self.app.run()
        # Pastikan PatientController dipanggil dengan argumen yang benar
        mock_patient_controller.assert_called_with(
            self.app.current_user,
            self.app.users,
            self.app.appointments,
            self.app.prescriptions,
            self.app.medicines, # Cek dependensi baru
            self.mock_data_manager_instance # Cek dependensi DataManager
        )
        mock_patient_controller.return_value.run.assert_called_once()
        
    @patch('controllers.app_controller.DoctorController')
    @patch('builtins.input', side_effect=['dokter1', 'pw2'])
    def test_run_delegates_to_doctor_controller(self, mock_input, mock_doctor_controller):
        """Menguji delegasi ke DoctorController dengan argumen yang benar."""
        self.app.run()
        mock_doctor_controller.assert_called_with(
            self.app.current_user,
            self.app.appointments,
            self.app.prescriptions,
            self.app.medicines,
            self.app.users,
            self.mock_data_manager_instance # Cek dependensi DataManager
        )
        mock_doctor_controller.return_value.run.assert_called_once()