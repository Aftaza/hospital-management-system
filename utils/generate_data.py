import csv
import random
from faker import Faker

# Inisialisasi Faker untuk data berbahasa Indonesia
fake = Faker('id_ID')

# --- KONFIGURASI ---
NUM_DOCTORS = 10
NUM_PATIENTS = 100
NUM_MEDICINES = 80
USERS_FILENAME = 'data/users.csv'
MEDICINES_FILENAME = 'data/medicines.csv'

# --- DATA SOURCE untuk DOKTER ---
SPECIALTIES = [
    'Umum', 'Anak', 'Penyakit Dalam', 'Jantung', 'THT', 
    'Mata', 'Kulit dan Kelamin', 'Saraf', 'Gigi', 'Bedah Umum'
]
DAYS = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
TIME_SLOTS = ['08:00-11:00', '10:00-13:00', '14:00-17:00', '16:00-19:00']

# --- DATA SOURCE untuk OBAT ---
PREFIXES = [
    'Amox', 'Levo', 'Cefix', 'Vita', 'Neuro', 'Para', 'Ibu', 'Dexam', 'Metron', 'Clinda'
]
TERMS = [
    'cillin', 'floksasin', 'ime', 'bion', 'min', 'mol', 'profen', 'thasone', 'dazole', 'mycin'
]
FORMS = ['500mg', '250mg', 'Forte', 'Plus', 'Syrup', 'Tablet', 'Kaplet']


def generate_users_data():
    """Membuat dan menyimpan data user (dokter dan pasien) ke file CSV."""
    users_data = []
    user_id_counter = 1

    print(f"Membuat data untuk {NUM_DOCTORS} dokter...")
    # Generate Dokter
    for _ in range(NUM_DOCTORS):
        full_name = fake.name_male()
        first_name = full_name.split(' ')[0].lower()
        username = f"dr_{first_name}"
        
        # Buat jadwal acak untuk 2 hari
        schedule_days = random.sample(DAYS, 2)
        schedule = ";".join([f"{day} {random.choice(TIME_SLOTS)}" for day in schedule_days])
        
        users_data.append({
            'id': user_id_counter,
            'username': username,
            'password': f"pw{random.randint(100,999)}",
            'role': 'dokter',
            'specialty': random.choice(SPECIALTIES),
            'schedule': schedule
        })
        user_id_counter += 1

    print(f"Membuat data untuk {NUM_PATIENTS} pasien...")
    # Generate Pasien
    for _ in range(NUM_PATIENTS):
        full_name = fake.name()
        first_name = full_name.split(' ')[0].lower()
        # Tambahkan angka acak agar username unik
        username = f"{first_name}{random.randint(10,99)}"
        
        users_data.append({
            'id': user_id_counter,
            'username': username,
            'password': f"pw{random.randint(100,999)}",
            'role': 'pasien',
            'specialty': '',
            'schedule': ''
        })
        user_id_counter += 1
    
    # Menambahkan 1 user staff untuk kelengkapan
    users_data.append({
        'id': user_id_counter, 'username': 'staff1', 'password': 'pwstaff',
        'role': 'staff', 'specialty': '', 'schedule': ''
    })

    # Menulis ke file CSV
    with open(USERS_FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'username', 'password', 'role', 'specialty', 'schedule'])
        writer.writeheader()
        writer.writerows(users_data)
        
    print(f"✅ Data user berhasil disimpan di '{USERS_FILENAME}'")

def generate_medicines_data():
    """Membuat dan menyimpan data obat ke file CSV."""
    medicines_data = []
    
    print(f"Membuat data untuk {NUM_MEDICINES} jenis obat...")
    medicine_names = set() # Untuk memastikan nama obat unik
    while len(medicine_names) < NUM_MEDICINES:
        name = f"{random.choice(PREFIXES)}{random.choice(TERMS)} {random.choice(FORMS)}"
        medicine_names.add(name)

    for i, name in enumerate(medicine_names):
        medicines_data.append({
            'id': i + 1,
            'name': name,
            'stock': random.randint(20, 500)
        })

    # Menulis ke file CSV
    with open(MEDICINES_FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'stock'])
        writer.writeheader()
        writer.writerows(medicines_data)
        
    print(f"✅ Data obat berhasil disimpan di '{MEDICINES_FILENAME}'")

if __name__ == "__main__":
    print("--- Mulai Membuat Dummy Data ---")
    generate_users_data()
    generate_medicines_data()
    print("--- Selesai ---")