import os
from cryptography.fernet import Fernet


def key_generator(output=None):
    '''
    Funktion för att generera en fernet key till crypto_tool
    Används med/utan command -o om man vill spara nyckeln till specifik path,
    annars sparas i folder där genereringen körs.
    '''
    key = Fernet.generate_key()
    if output:
        with open(f"{output}.key", "wb") as f:
            f.write(key)
            print(f"Nyckeln har sparats i {output}.key")
    else:
        with open("crypto.key", "wb") as key_file:
            key_file.write(key)
            print(f"Nyckeln har sparats i {os.getcwd()}\\crypto.key")
