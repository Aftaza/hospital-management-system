import pandas as pd
import os

class DataManager:
    """
    Handles all read and write operations for CSV files.
    """
    def __init__(self, data_folder='data/'):
        self.users_path = os.path.join(data_folder, 'users.csv')
        self.medicines_path = os.path.join(data_folder, 'medicines.csv')
        self.appointments_path = os.path.join(data_folder, 'appointments.csv')
        self.prescriptions_path = os.path.join(data_folder, 'prescriptions.csv')

    def save_medicines(self, medicines_list):
        """
        Saves the entire list of medicine objects to medicines.csv, overwriting it.
        """
        # Convert list of Medicine objects to list of dictionaries
        data_to_save = [
            {'id': med.id, 'name': med.name, 'stock': med.stock}
            for med in medicines_list
        ]
        df = pd.DataFrame(data_to_save)
        df.to_csv(self.medicines_path, index=False)
        print("[DataManager] Medicine data saved.")

    def save_appointments(self, appointments_list):
        """
        Saves the entire list of appointment objects to appointments.csv.
        """
        if not appointments_list:
            return # Don't save if the list is empty
            
        data_to_save = [
            {
                'id': app.id,
                'patient_id': app.patient_id,
                'doctor_id': app.doctor_id,
                'queue_number': app.queue_number,
                'status': app.status
            }
            for app in appointments_list
        ]
        df = pd.DataFrame(data_to_save)
        df.to_csv(self.appointments_path, index=False)
        print("[DataManager] Appointment data saved.")

    def save_prescriptions(self, prescriptions_list):
        """
        Saves the entire list of prescription objects to prescriptions.csv.
        """
        if not prescriptions_list:
            return

        def format_medicines(med_dict):
            # Convert dictionary {1:2, 3:1} to string "1:2;3:1" for CSV compatibility
            return ";".join([f"{med_id}:{qty}" for med_id, qty in med_dict.items()])

        data_to_save = [
            {
                'id': pres.id,
                'patient_id': pres.patient_id,
                'doctor_id': pres.doctor_id,
                'medicines': format_medicines(pres.medicines),
                'status': pres.status
            }
            for pres in prescriptions_list
        ]
        df = pd.DataFrame(data_to_save)
        df.to_csv(self.prescriptions_path, index=False)
        print("[DataManager] Prescription data saved.")