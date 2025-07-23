**AES Crypto Tool**

This is a simple Python-based AES encryption and decryption utility supporting three modes: 'EBC', 'CBC', and 'GCM'. It allows secure file encryption and decryption with optional IV and additional authenticated data for GCM.

**Features**

- AES encryption in 'ECB', 'CBC', and 'GCM' modes
- Handles 'IV' (Initialization Vector) and 'GCM additional data'
- Clean CLI usage with 'argparse'
- Works on binary files (e.g., text, images, executables)

**Project Structure**

**Usage**

**Encrypt**

-command: python encrypt.py -key data/example_key.txt -input data/sample_plaintext.txt -out data/sample_ciphertext.enc -mode cbc -IV data/example_iv.txt

**Decrypt**

-command: python decrypt.py -key data/example_key.txt -input data/sample_ciphertext.enc -out data/decrypted.txt -mode cbc -IV data/example_iv.txt

**Installation**

-Install the required dependency from 'requirements.txt'
-command: pip install -r requirements.txt

**Test**

-Unit tests can be found: test_encrypt.py, test_decrypt.py
-command: python -m unittest discover test

**Author**

-Srinija Battula
-Cybersecurity and Threat Intelligence


