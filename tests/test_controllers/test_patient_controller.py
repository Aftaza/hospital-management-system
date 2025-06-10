import unittest
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.patient_controller import PatientController
from models.user import Patient, Doctor
from models.appointment import Appointment

class TestPatientController(unittest.TestCase):

    def setUp(self):
        """Siapkan objek mock untuk diinjeksi ke controller."""
        self.mock_patient = Patient(user_id=1, username='pasien_test', password='pw')
        self.mock_doctors = [Doctor(user_id=10, username='dr_budi', password='pw', specialty='Anak', schedule='Rabu')]
        self.mock_appointments = []
        self.controller = PatientController(self.mock_patient, self.mock_doctors, self.mock_appointments, [])

    @patch('views.patient_view.display_patient_menu', return_value='5') # 5 = Keluar
    def test_run_exit(self, mock_menu):
        """Menguji controller bisa keluar dari loop dengan benar."""
        self.controller.run()
        mock_menu.assert_called_once()

    @patch('views.patient_view.display_doctor_schedules')
    @patch('views.patient_view.display_patient_menu', side_effect=['1', '5']) # 1 = Lihat Jadwal, 5 = Keluar
    def test_view_doctor_schedules_flow(self, mock_menu, mock_display_schedules):
        """Menguji alur untuk melihat jadwal dokter."""
        # Act
        self.controller.run()
        # Assert
        mock_display_schedules.assert_called_with(self.mock_doctors)

    @patch('views.patient_view.display_queue_info')
    @patch('builtins.input', return_value='10') # Pasien memilih dokter ID 10
    @patch('views.patient_view.display_doctor_schedules')
    @patch('views.patient_view.display_patient_menu', side_effect=['2', '5']) # 2 = Daftar, 5 = Keluar
    def test_register_appointment_success(self, mock_menu, mock_schedules, mock_input, mock_queue_info):
        """Menguji alur pendaftaran appointment berhasil."""
        # Act
        self.controller.run()
        # Assert
        # Pastikan appointment baru dibuat
        self.assertEqual(len(self.mock_appointments), 1)
        new_appointment = self.mock_appointments[0]
        self.assertEqual(new_appointment.patient_id, self.mock_patient.id)
        self.assertEqual(new_appointment.doctor_id, 10)
        self.assertEqual(new_appointment.queue_number, 1)
        # Pastikan view sukses dipanggil
        mock_queue_info.assert_called_once()