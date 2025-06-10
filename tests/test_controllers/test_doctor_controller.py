import unittest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.doctor_controller import DoctorController
from models.user import Doctor, Patient
from models.appointment import Appointment

class TestDoctorController(unittest.TestCase):

    def setUp(self):
        self.mock_doctor = Doctor(user_id=10, username='dr_budi', password='pw', specialty='Anak', schedule='Rabu')
        self.mock_patient = Patient(user_id=1, username='pasien_anak', password='pw')
        self.mock_appointments = [
            Appointment(app_id=1, patient_id=1, doctor_id=10, queue_number=1, status='waiting')
        ]
        self.mock_prescriptions = []
        self.mock_medicines = []
        self.controller = DoctorController(
            self.mock_doctor, self.mock_appointments, self.mock_prescriptions, 
            self.mock_medicines, [self.mock_doctor, self.mock_patient]
        )

    @patch('views.doctor_view.display_patient_queue')
    @patch('views.doctor_view.display_doctor_menu', side_effect=['1', '3']) # 1 = Lihat Antrean, 3 = Keluar
    def test_view_patient_queue_flow(self, mock_menu, mock_display_queue):
        """Menguji alur melihat antrean pasien."""
        self.controller.run()
        # Assert
        mock_display_queue.assert_called_once()
        # Cek apakah data yang dikirim ke view sudah benar (hanya appointment untuk dokter ini)
        self.assertEqual(len(mock_display_queue.call_args[0][0]), 1)
        self.assertEqual(mock_display_queue.call_args[0][0][0].patient_id, 1)

    @patch('views.shared_view.display_success')
    @patch('views.doctor_view.prompt_create_prescription', return_value=('1', {101: 2})) # (patient_id, {med_id: qty})
    @patch('views.doctor_view.display_doctor_menu', side_effect=['2', '3']) # 2 = Buat Resep, 3 = Keluar
    def test_create_prescription_success(self, mock_menu, mock_prompt, mock_success_view):
        """Menguji alur pembuatan resep berhasil."""
        # Act
        self.controller.run()
        # Assert
        # 1. Pastikan resep baru ditambahkan
        self.assertEqual(len(self.mock_prescriptions), 1)
        new_prescription = self.mock_prescriptions[0]
        self.assertEqual(new_prescription.patient_id, 1)
        self.assertEqual(new_prescription.medicines[101], 2)
        # 2. Pastikan status appointment pasien menjadi 'done'
        self.assertEqual(self.mock_appointments[0].status, 'done')
        # 3. Pastikan view sukses dipanggil
        mock_success_view.assert_called_once()