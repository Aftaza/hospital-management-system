import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.medicine import Medicine

class TestMedicineModel(unittest.TestCase):

    def test_create_medicine(self):
        """Menguji pembuatan objek Medicine dan tipe data atributnya."""
        # Arrange
        med = Medicine(med_id=101, name='Paracetamol', stock='150')

        # Assert
        self.assertIsInstance(med, Medicine)
        self.assertEqual(med.id, 101)
        self.assertEqual(med.name, 'Paracetamol')
        # Memastikan stok dikonversi menjadi integer
        self.assertEqual(med.stock, 150)
        self.assertIsInstance(med.stock, int)