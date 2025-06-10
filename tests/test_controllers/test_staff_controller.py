import unittest
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.staff_controller import StaffController
from models.user import Staff
from models.medicine import Medicine
from models.prescription import Prescription

class TestStaffController(unittest.TestCase):

    def setUp(self):
        self.mock_data_manager = MagicMock()
        self.mock_staff = Staff(user_id=100, username='staff_test', password='pw')
        self.mock_medicines = [
            Medicine(med_id=1, name='Paracetamol', stock=50),
            Medicine(med_id=2, name='Amoxicillin', stock=10)
        ]
        self.mock_prescriptions = [
            Prescription(pres_id=1, patient_id=1, doctor_id=10, medicines={1: 20}, status='submitted')
        ]
        self.controller = StaffController(
            self.mock_staff, self.mock_prescriptions, self.mock_medicines, 
            [], self.mock_data_manager
        )

    @patch('views.staff_view.prompt_process_prescription', return_value='1')
    @patch('views.staff_view.display_prescription_requests')
    @patch('views.staff_view.display_staff_menu', side_effect=['1', '3'])
    def test_process_prescription_saves_data(self, mock_menu, mock_display, mock_prompt):
        """Menguji proses resep memanggil DataManager."""
        with patch('views.shared_view.display_success'):
            self.controller.run()
            # Assert
            # Stok obat berkurang, status resep fulfilled
            self.assertEqual(self.mock_medicines[0].stock, 30)
            self.assertEqual(self.mock_prescriptions[0].status, 'fulfilled')
            # Cek apakah DataManager dipanggil untuk menyimpan kedua data
            self.mock_data_manager.save_medicines.assert_called_once_with(self.mock_medicines)
            self.mock_data_manager.save_prescriptions.assert_called_once_with(self.mock_prescriptions)

    @patch('views.staff_view.prompt_update_stock', return_value=('1', '100'))
    @patch('views.staff_view.display_medicine_stock')
    @patch('builtins.input', side_effect=['update', 'kembali'])
    @patch('views.staff_view.display_staff_menu', side_effect=['2', '3'])
    def test_manage_stock_saves_data(self, mock_menu, mock_submenu_input, mock_display, mock_prompt):
        """Menguji manajemen stok memanggil DataManager."""
        with patch('views.shared_view.display_success'):
            self.controller.run()
            # Assert
            self.assertEqual(self.mock_medicines[0].stock, 100)
            self.mock_data_manager.save_medicines.assert_called_once_with(self.mock_medicines)
