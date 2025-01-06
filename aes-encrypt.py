# Srinija Battula

import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os

def encrypt(key, plaintext, mode, iv=None, additional=None):
    if mode == 'ecb':
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        return ciphertext

    elif mode == 'cbc':
        if iv is None:
            raise ValueError("IV is required for CBC mode.")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        return ciphertext

    elif mode == 'gcm':
        if iv is None:
            raise ValueError("IV is required for GCM mode.")
        cipher = AES.new(key, AES.MODE_GCM, iv)
        if additional:
            cipher.update(additional)  # Call update before encryption
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return ciphertext + tag  # Return combined ciphertext and tag

    else:
        raise ValueError("Unsupported mode: {}".format(mode))

def main():
    parser = argparse.ArgumentParser(description='AES Encryption')
    parser.add_argument('-key', type=str, required=True, help='Path to the key file')
    parser.add_argument('-input', type=str, required=True, help='Path to the input plaintext file')
    parser.add_argument('-out', type=str, required=True, help='Path to the output ciphertext file')
    parser.add_argument('-mode', type=str, required=True, choices=['ecb', 'cbc', 'gcm'], help='AES mode')
    parser.add_argument('-IV', type=str, help='Path to the IV file (for CBC and GCM modes)')
    parser.add_argument('-gcm_arg', type=str, help='Path to the additional data file (for GCM mode)')

    args = parser.parse_args()

    # Read key and input data
    with open(args.key, 'r') as f:
        key = bytes.fromhex(f.read().strip())
    with open(args.input, 'rb') as f:
        plaintext = f.read()

    iv = None
    if args.IV:
        with open(args.IV, 'r') as f:
            iv = bytes.fromhex(f.read().strip())

    additional = None
    if args.gcm_arg:
        with open(args.gcm_arg, 'rb') as f:
            additional = f.read()

    # Encrypt and write to output
    ciphertext = encrypt(key, plaintext, args.mode, iv, additional)
    with open(args.out, 'wb') as f:
        f.write(ciphertext)

if __name__ == '__main__':
    main()

