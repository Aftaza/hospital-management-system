class Appointment:
    def __init__(self, app_id, patient_id, doctor_id, queue_number, status='waiting'):
        self.id = app_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.queue_number = queue_number
        self.status = status # waiting, in_progress, done