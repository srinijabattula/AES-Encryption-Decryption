# Srinija Battula

import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

def decrypt(key, ciphertext, mode, iv=None, additional=None):
    if mode == 'ecb':
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext

    elif mode == 'cbc':
        if iv is None:
            raise ValueError("IV is required for CBC mode.")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext

    elif mode == 'gcm':
        if iv is None:
            raise ValueError("IV is required for GCM mode.")
        # The last 16 bytes are the tag in GCM mode
        tag = ciphertext[-16:]
        ciphertext = ciphertext[:-16]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext

    else:
        raise ValueError("Unsupported mode: {}".format(mode))

def main():
    parser = argparse.ArgumentParser(description='AES Decryption')
    parser.add_argument('-key', type=str, required=True, help='Path to the key file')
    parser.add_argument('-input', type=str, required=True, help='Path to the input ciphertext file')
    parser.add_argument('-out', type=str, required=True, help='Path to the output plaintext file')
    parser.add_argument('-mode', type=str, required=True, choices=['ecb', 'cbc', 'gcm'], help='AES mode')
    parser.add_argument('-IV', type=str, help='Path to the IV file (for CBC and GCM modes)')

    args = parser.parse_args()

    # Read key and input data
    with open(args.key, 'r') as f:
        key = bytes.fromhex(f.read().strip())
    with open(args.input, 'rb') as f:
        ciphertext = f.read()

    iv = None
    if args.IV:
        with open(args.IV, 'r') as f:
            iv = bytes.fromhex(f.read().strip())

    # Decrypt and write to output
    plaintext = decrypt(key, ciphertext, args.mode, iv)
    with open(args.out, 'wb') as f:
        f.write(plaintext)

if __name__ == '__main__':
    main()


