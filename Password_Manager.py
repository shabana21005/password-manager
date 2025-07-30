from cryptography.fernet import Fernet
import os

# ---------- SETUP ----------
KEY_FILE = "key.key"
DATA_FILE = "passwords.txt"

# Generate and save encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

# Load the saved key
def load_key():
    return open(KEY_FILE, "rb").read()

# Encrypt password
def encrypt_password(password, key):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

# Decrypt password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

# Add new password entry
def add_password():
    account = input("🔑 Enter account name: ")
    password = input("🔒 Enter password: ")
    encrypted_pw = encrypt_password(password, key)

    with open(DATA_FILE, "a") as f:
        f.write(f"{account}|{encrypted_pw}\n")
    print("✅ Password saved.")

# View saved passwords
def view_passwords():
    if not os.path.exists(DATA_FILE):
        print("⚠️ No passwords saved.")
        return

    with open(DATA_FILE, "r") as f:
        for line in f:
            account, encrypted_pw = line.strip().split("|")
            try:
                decrypted_pw = decrypt_password(encrypted_pw, key)
                print(f"{account} → {decrypted_pw}")
            except:
                print(f"{account} → ❌ Error decrypting.")


if not os.path.exists(KEY_FILE):
    print("🔐 First time setup: Generating key...")
    generate_key()

key = load_key()

while True:
    print("\n🛡️ Password Manager")
    print("1. Add Password")
    print("2. View Passwords")
    print("3. Exit")
    choice = input("Choose option (1/2/3): ")

    if choice == "1":
        add_password()
    elif choice == "2":
        view_passwords()
    elif choice == "3":
        print("👋 Exiting Password Manager.")
        break
    else:
        print("❌ Invalid option. Try again.")
