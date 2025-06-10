class User:
    def __init__(self, user_id, username, password, role):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role

class Patient(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, 'pasien')

class Doctor(User):
    def __init__(self, user_id, username, password, specialty, schedule):
        super().__init__(user_id, username, password, 'dokter')
        self.specialty = specialty
        self.schedule = schedule

class Staff(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, 'staff')