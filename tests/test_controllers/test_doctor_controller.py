import unittest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.doctor_controller import DoctorController
from models.user import Doctor, Patient
from models.appointment import Appointment
from models.prescription import Prescription

class TestDoctorController(unittest.TestCase):

    def setUp(self):
        self.mock_data_manager = MagicMock()
        self.mock_doctor = Doctor(user_id=10, username='dr_budi', password='pw', specialty='Anak', schedule='Rabu')
        self.mock_patient = Patient(user_id=1, username='pasien_anak', password='pw')
        self.mock_waiting_appointment = Appointment(app_id=1, patient_id=1, doctor_id=10, queue_number=1, status='waiting')
        self.mock_appointments = [self.mock_waiting_appointment]
        self.mock_prescriptions = []
        self.mock_medicines = []
        
        self.controller = DoctorController(
            self.mock_doctor, self.mock_appointments, self.mock_prescriptions, 
            self.mock_medicines, [self.mock_doctor, self.mock_patient], self.mock_data_manager
        )

    @patch('views.shared_view.display_success')
    @patch('views.doctor_view.prompt_for_medicines', return_value={101: 2})
    @patch('views.doctor_view.prompt_select_patient')
    @patch('views.doctor_view.display_doctor_menu', side_effect=['2', '3'])
    def test_create_prescription_from_queue_success(self, mock_menu, mock_select_patient, mock_get_medicines, mock_success):
        """Menguji alur pembuatan resep dari antrean berhasil."""
        # Arrange: Atur agar prompt_select_patient mengembalikan appointment yang sedang menunggu
        mock_select_patient.return_value = self.mock_waiting_appointment

        # Act
        self.controller.run()

        # Assert
        # 1. Resep baru ditambahkan
        self.assertEqual(len(self.mock_prescriptions), 1)
        # 2. Status appointment berubah menjadi 'done'
        self.assertEqual(self.mock_waiting_appointment.status, 'done')
        # 3. DataManager dipanggil untuk menyimpan kedua perubahan
        self.mock_data_manager.save_prescriptions.assert_called_once_with(self.mock_prescriptions)
        self.mock_data_manager.save_appointments.assert_called_once_with(self.mock_appointments)

    @patch('views.doctor_view.prompt_select_patient')
    @patch('views.doctor_view.display_doctor_menu', side_effect=['2', '3'])
    def test_create_prescription_canceled_if_no_patient_selected(self, mock_menu, mock_select_patient):
        """Menguji pembuatan resep batal jika tidak ada pasien dipilih."""
        # Arrange: Atur agar dokter tidak memilih pasien (prompt mengembalikan None)
        mock_select_patient.return_value = None

        # Act
        self.controller.run()

        # Assert: Tidak ada resep dibuat, tidak ada data disimpan
        self.assertEqual(len(self.mock_prescriptions), 0)
        self.mock_data_manager.save_prescriptions.assert_not_called()
        self.mock_data_manager.save_appointments.assert_not_called()
