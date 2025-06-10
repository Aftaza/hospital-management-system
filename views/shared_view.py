import os

def clear_screen():
    """Membersihkan layar terminal."""
    # Untuk Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Untuk MacOS dan Linux
    else:
        _ = os.system('clear')

def display_header(title):
    """Menampilkan header yang terformat."""
    print("=" * 40)
    print(f"{title:^40}")
    print("=" * 40)

def display_error(message):
    """Menampilkan pesan error."""
    print(f"\n[ERROR] {message}")
    pause()

def display_success(message):
    """Menampilkan pesan sukses."""
    print(f"\n[INFO] {message}")
    pause()

def pause():
    """Memberi jeda hingga pengguna menekan Enter."""
    input("\nTekan Enter untuk melanjutkan...")