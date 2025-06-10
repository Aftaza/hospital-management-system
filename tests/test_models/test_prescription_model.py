import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.prescription import Prescription

class TestPrescriptionModel(unittest.TestCase):

    def test_create_prescription(self):
        """Menguji pembuatan objek Prescription."""
        # Arrange
        medicines_dict = {1: 2, 5: 1} # {medicine_id: quantity}
        pres = Prescription(
            pres_id=1,
            patient_id=15,
            doctor_id=4,
            medicines=medicines_dict
        )

        # Assert
        self.assertIsInstance(pres, Prescription)
        self.assertEqual(pres.id, 1)
        self.assertEqual(pres.patient_id, 15)
        self.assertEqual(pres.doctor_id, 4)
        # Memastikan status default adalah 'new'
        self.assertEqual(pres.status, 'new')
        # Memastikan dictionary obat disimpan dengan benar
        self.assertDictEqual(pres.medicines, medicines_dict)