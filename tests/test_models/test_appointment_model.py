import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.appointment import Appointment

class TestAppointmentModel(unittest.TestCase):

    def test_create_appointment_with_default_status(self):
        """Menguji pembuatan objek Appointment dengan status default."""
        # Arrange
        app = Appointment(app_id=1, patient_id=10, doctor_id=2, queue_number=5)

        # Assert
        self.assertIsInstance(app, Appointment)
        self.assertEqual(app.id, 1)
        self.assertEqual(app.patient_id, 10)
        self.assertEqual(app.doctor_id, 2)
        self.assertEqual(app.queue_number, 5)
        # Memastikan status default adalah 'waiting'
        self.assertEqual(app.status, 'waiting')

    def test_create_appointment_with_specific_status(self):
        """Menguji pembuatan objek Appointment dengan status yang ditentukan."""
        # Arrange
        app = Appointment(app_id=2, patient_id=11, doctor_id=3, queue_number=6, status='done')

        # Assert
        self.assertEqual(app.id, 2)
        self.assertEqual(app.status, 'done')