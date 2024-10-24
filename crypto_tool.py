# Kryptera en fil med hjälp av en symmetrisk nyckel (filnamn som argument).
# Dekryptera en krypterad fil med rätt nyckel (filnamn som argument).
#  Kryptering och Dekryptering:

# Implementera ett andra skript (ex crypto_tool.py) som använder argparse för att hantera kommandoradsalternativ och utföra följande funktioner:
# Kryptera en fil med en befintlig nyckel.
# Dekryptera en krypterad fil och återställa originalet.
import sys
import argparse
from getpass import getpass
import os
import hashlib
import base64
import keygen
from cryptography.fernet import Fernet

# Lägg till funktionalitet för att skapa en lösenordsbaserad nyckel med hjälp av PBKDF2.
def pbkdf2_key_from_password(password,salt):
    hash_name = "sha256"
    password_key = hashlib.pbkdf2_hmac(hash_name, password,salt, 200000)
    password_key = base64.urlsafe_b64encode(password_key)
    return password_key

def encrypt(file, key=None, password=None):
    if password:
        salt = os.urandom(16)
        key = pbkdf2_key_from_password(password,salt)
    else:
        try:
            if key:
                with open(key, "rb") as f:
                    key = f.read()
                salt=None
        except PermissionError:
            print("Fil ej hittad!\nAnge filnamn på .txt som önskas läsas där nyckel befinns. (Möjligen glömt sista steg i angiven path?)\n")
            sys.exit()
        except FileNotFoundError:
            print("Ange filens hela namn där nyckel befinns (inkl. t.ex .txt)\n")
            sys.exit()

    cipher_suite = Fernet(key)

    with open(file, "rb") as encrypt_file:
        file_encrypt = encrypt_file.read()

    cipher_text =  cipher_suite.encrypt(file_encrypt)

    if salt:
        cipher_text = salt + cipher_suite.encrypt(file_encrypt)

    file_name = input("ange namn på fil: ")
    with open(f"{file_name}.enc", "wb") as encoded_file:
        encoded_file.write(cipher_text)
        print(f"Fil har skapats och sparats som: {file_name}.enc")

def decrypt(file,key=None, password=None):
    with open(file, "rb") as encoded_file:
        data_file = encoded_file.read()
    if key:
        with open(key, "rb") as f:
            key = f.read()
    elif password:
        salt = data_file[:16]
        data_file = data_file[16:]
        key = pbkdf2_key_from_password(password,salt)

    cipher_suite = Fernet(key)

    plain_text = cipher_suite.decrypt(data_file)

    with open(file, "wb") as decrypt_file:
        decrypt_file.write(plain_text)
        print("Fil dekrypterad!")

def main():
    parser = argparse.ArgumentParser(description="Kryptera en fil med en befintlig nyckel samt dekryptera en krypterad fil och återställa originalet")
    parser.add_argument("-v", "--verbose", action="store_true", help="Visar utökad info")

    subparsers = parser.add_subparsers(dest='command')

    get_key = subparsers.add_parser("generate", help= 'Genererar en symetrisk nyckel, möjligt att spara resultat i önskad fil.')
    get_key.add_argument("-o", "--output", help="Ange path där du vill att nyckel sparas | -o/--output <path\\filename> ")

    encrypt_file = subparsers.add_parser("encrypt", help="Krypterar fil | encrypt <fil> <optional>")
    encrypt_file.add_argument("file", help="Ange fil. Om filen inte finns i samma folder, ange path till filen.")
    encrypt_file.add_argument("-k","--key", help="Ange nyckel fil. Om filen inte finns i samma folder, ange path till filen. | -k/--key <path\\filename>")
    encrypt_file.add_argument("-p","--password",action="store_true", help="ange lösenord | -p/--password <lösenord>")

    decrypt_file = subparsers.add_parser("decrypt", help="dekrypterar fil | decrypt <fil> <optional>")
    decrypt_file.add_argument("file", help="Ange fil. Om filen inte finns i samma folder, ange path till filen.")
    decrypt_file.add_argument("-k","--key", help="Ange nyckel fil. Om filen inte finns i samma folder, ange path till filen. | -k/--key <path\\filename>")
    decrypt_file.add_argument("-p","--password",action="store_true", help="ange lösenord | -p/--password <lösenord>")

    args = parser.parse_args()

    if args.command == "generate":
        if args.output:
            keygen.key_generator(args.output)
        else:
            keygen.key_generator()

    if args.command == "encrypt":
        if args.key:
            encrypt(args.file, key=args.key)
        elif args.password:
            user_password = getpass("Ange lösenord: ").encode()
            encrypt(args.file, password=user_password)
        else:
            print("måste välja key eller password")

    if args.command == "decrypt":
        if args.key:
            decrypt(args.file, key=args.key)
        elif args.password:
            try:
                check_password = getpass("Ange lösenord: ").encode()
                decrypt(args.file, password=check_password)
            except Exception as e:
                print(f"Fel lösenord {e}")
        else:
            print("måste välja key eller password")

    if args.verbose is True:
        print(f"Mode: {args.mode}\nFile: {args.file}\nKey: {args.key_file}")


if __name__ == "__main__":
    main()
