class Prescription:
    def __init__(self, pres_id, patient_id, doctor_id, medicines, status='new'):
        self.id = pres_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.medicines = medicines # Dictionary: {medicine_id: quantity}
        self.status = status # new, submitted, fulfilled, pending