import unittest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.staff_controller import StaffController
from models.user import Staff, Patient
from models.medicine import Medicine
from models.prescription import Prescription

class TestStaffController(unittest.TestCase):

    def setUp(self):
        self.mock_staff = Staff(user_id=100, username='staff_test', password='pw')
        self.mock_medicines = [
            Medicine(med_id=1, name='Paracetamol', stock=50),
            Medicine(med_id=2, name='Amoxicillin', stock=10)
        ]
        self.mock_prescriptions = [
            Prescription(pres_id=1, patient_id=1, doctor_id=10, medicines={1: 20}, status='submitted'), # Stok cukup
            Prescription(pres_id=2, patient_id=2, doctor_id=10, medicines={2: 15}, status='submitted')  # Stok kurang
        ]
        self.controller = StaffController(self.mock_staff, self.mock_prescriptions, self.mock_medicines, [])

    @patch('views.shared_view.display_success')
    @patch('views.staff_view.prompt_process_prescription', return_value='1') # Proses resep ID 1
    @patch('views.staff_view.display_prescription_requests')
    @patch('views.staff_view.display_staff_menu', side_effect=['1', '3'])
    def test_process_prescription_stock_sufficient(self, mock_menu, mock_display_req, mock_prompt, mock_success):
        """Menguji proses resep dimana stok obat mencukupi."""
        # Act
        self.controller.run()
        # Assert
        # 1. Stok obat harus berkurang
        self.assertEqual(self.mock_medicines[0].stock, 30) # 50 - 20 = 30
        # 2. Status resep menjadi 'fulfilled'
        self.assertEqual(self.mock_prescriptions[0].status, 'fulfilled')
        # 3. Pesan sukses ditampilkan
        mock_success.assert_called()

    @patch('views.shared_view.display_success')
    @patch('views.staff_view.prompt_process_prescription', return_value='2') # Proses resep ID 2
    @patch('views.staff_view.display_prescription_requests')
    @patch('views.staff_view.display_staff_menu', side_effect=['1', '3'])
    def test_process_prescription_stock_insufficient(self, mock_menu, mock_display_req, mock_prompt, mock_success):
        """Menguji proses resep dimana stok obat tidak cukup."""
        # Act
        self.controller.run()
        # Assert
        # 1. Stok obat TIDAK BOLEH berubah
        self.assertEqual(self.mock_medicines[1].stock, 10)
        # 2. Status resep menjadi 'pending'
        self.assertEqual(self.mock_prescriptions[1].status, 'pending')
        # 3. Pesan info ditampilkan
        mock_success.assert_called()