import argparse
import itertools
import string
import hashlib


def brute_force(target_password):
    '''Funktion för att knäcka hashade lösenord'''
    charcters = string.ascii_lowercase + string.digits

    for reps in range(1, 10):
        for guess in itertools.product(charcters,repeat=reps):
            guess = ''.join(guess)
            print(f"Checking: {guess}")
            hash_object = hashlib.sha256()
            hash_object.update(guess.encode())
            guess_hash_value = hash_object.hexdigest()

            if guess_hash_value == target_password:
                print(f"password found: {guess}")
                return guess
    return None

def main():


    parser = argparse.ArgumentParser(description="knäcka hashad lösenord")
    parser.add_argument("hash", help="ange lösenords hash ")


    args = parser.parse_args()

    if args.hash:
        brute_force(args.hash)

if __name__=="__main__":
    main()
    
