import unittest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.patient_controller import PatientController
from models.user import Patient, Doctor
from models.medicine import Medicine
from models.appointment import Appointment
from models.prescription import Prescription

class TestPatientController(unittest.TestCase):

    def setUp(self):
        """Siapkan objek mock untuk diinjeksi ke controller."""
        self.mock_data_manager = MagicMock()
        self.mock_patient = Patient(user_id=1, username='pasien_test', password='pw')
        self.mock_doctors = [Doctor(user_id=10, username='dr_budi', password='pw', specialty='Anak', schedule='Rabu')]
        self.mock_medicines = [Medicine(med_id=101, name="Obat A", stock=10)]
        self.mock_appointments = []
        self.mock_prescriptions = [
            Prescription(pres_id=1, patient_id=1, doctor_id=10, medicines={101: 1}, status='new')
        ]
        
        self.controller = PatientController(
            self.mock_patient, self.mock_doctors + [self.mock_patient], self.mock_appointments, 
            self.mock_prescriptions, self.mock_medicines, self.mock_data_manager
        )

    @patch('views.patient_view.display_patient_menu', return_value='5')
    def test_run_can_exit(self, mock_menu):
        self.controller.run()
        mock_menu.assert_called_once()

    @patch('views.patient_view.prompt_for_doctor_id', return_value='10')
    @patch('views.patient_view.display_doctor_schedules')
    @patch('views.patient_view.display_patient_menu', side_effect=['2', '5'])
    def test_register_appointment_saves_data(self, mock_menu, mock_schedules, mock_doc_id):
        """Menguji pendaftaran appointment memanggil save_appointments."""
        with patch('views.patient_view.display_queue_info'): # mock view agar tidak print
            self.controller.run()
            # Assert
            self.assertEqual(len(self.mock_appointments), 1)
            self.mock_data_manager.save_appointments.assert_called_once_with(self.mock_appointments)

    @patch('views.shared_view.display_success')
    @patch('views.patient_view.prompt_submit_prescription', return_value='1') # Pasien memilih resep ID 1
    @patch('views.patient_view.display_my_prescriptions')
    @patch('views.patient_view.display_patient_menu', side_effect=['4', '5'])
    def test_handle_prescriptions_submit_success(self, mock_menu, mock_display, mock_prompt, mock_success):
        """Menguji alur pengajuan resep berhasil dan menyimpan data."""
        # Act
        self.controller.run()
        # Assert
        # 1. Status resep harus berubah menjadi 'submitted'
        submitted_prescription = self.mock_prescriptions[0]
        self.assertEqual(submitted_prescription.status, 'submitted')
        # 2. Metode save dari DataManager harus dipanggil
        self.mock_data_manager.save_prescriptions.assert_called_once_with(self.mock_prescriptions)
