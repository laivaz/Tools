import argparse
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # Progress bar library

# Event to signal threads to stop
found_password = threading.Event()

def is_encrypted_pem(pem_file):
    """Check if the PEM file contains the encrypted private key header."""
    try:
        with open(pem_file, "r") as f:
            first_line = f.readline().strip()
            return first_line == "-----BEGIN ENCRYPTED PRIVATE KEY-----"
    except FileNotFoundError:
        print(f"[-] PEM file '{pem_file}' not found!")
        sys.exit(1)

def try_password(pem_file, password):
    """Attempt to decrypt the PEM file using a single password."""
    if found_password.is_set():
        return None  # Stop checking if another thread found the password

    result = subprocess.run(
        ["openssl", "pkey", "-in", pem_file, "-passin", f"pass:{password}"],
        capture_output=True,
        text=True
    )

    if "BEGIN PRIVATE KEY" in result.stdout:
        print(f"\n[+] Password found: {password}")
        found_password.set()  # Signal other threads to stop
        return password
    return None

def password_generator(wordlist_file):
    """Generator to read passwords one by one, handling UTF-8 errors gracefully."""
    try:
        with open(wordlist_file, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        print(f"[-] Wordlist file '{wordlist_file}' not found!")
        sys.exit(1)

def brute_force_pem(pem_file, wordlist_file, max_threads=6):
    """Brute-force the PEM key using multiple threads while handling large wordlists efficiently."""
    
    if not is_encrypted_pem(pem_file):
        print("[-] The provided PEM file is not encrypted or has an unexpected format.")
        sys.exit(1)

    # Read passwords first to know how many we need to check
    passwords = list(password_generator(wordlist_file))
    total_attempts = len(passwords)

    print(f"[+] Attempting to brute-force {pem_file} with {total_attempts} passwords using {max_threads} threads...")

    with ThreadPoolExecutor(max_threads) as executor:
        # Initialize tqdm for progress bar
        with tqdm(total=total_attempts, desc="Progress", ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            futures = {executor.submit(try_password, pem_file, pw): pw for pw in passwords}

            # Update progress bar as futures complete
            for future in futures:
                if future.result():  # If a password is found, stop all threads
                    executor.shutdown(wait=False)
                    return
                pbar.update(1)  # Update the progress bar by 1 password attempt

    print("[-] No valid password found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multithreaded brute-force attack on an encrypted PEM key.")
    parser.add_argument("-p", "--pem", required=True, help="Path to the encrypted PEM file")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the password wordlist")
    parser.add_argument("-t", "--threads", type=int, default=6, help="Number of concurrent threads (default: 6)")

    args = parser.parse_args()
    brute_force_pem(args.pem, args.wordlist, args.threads)

