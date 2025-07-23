
import unittest
import subprocess
import os
import tempfile

class TestAESEncryption(unittest.TestCase):
    def setUp(self):
        self.key_path = 'test/test_files/key.txt'
        self.iv_path = 'test/test_files/iv.txt'
        self.aad_path = 'test/test_files/aad.txt'
        self.plaintext_path = 'test/test_files/plaintext.txt'
        self.temp_enc = tempfile.NamedTemporaryFile(delete=False).name
        self.temp_dec = tempfile.NamedTemporaryFile(delete=False).name

    def tearDown(self):
        if os.path.exists(self.temp_enc):
            os.remove(self.temp_enc)
        if os.path.exists(self.temp_dec):
            os.remove(self.temp_dec)

    def run_encrypt_decrypt(self, mode, use_iv=False, use_aad=False):
        encrypt_cmd = [
            'python3', 'encrypt.py',
            '-key', self.key_path,
            '-input', self.plaintext_path,
            '-out', self.temp_enc,
            '-mode', mode
        ]
        if use_iv:
            encrypt_cmd += ['-IV', self.iv_path]
        if use_aad:
            encrypt_cmd += ['-gcm_arg', self.aad_path]

        decrypt_cmd = [
            'python3', 'decrypt.py',
            '-key', self.key_path,
            '-input', self.temp_enc,
            '-out', self.temp_dec,
            '-mode', mode
        ]
        if use_iv:
            decrypt_cmd += ['-IV', self.iv_path]

        subprocess.run(encrypt_cmd, check=True)
        subprocess.run(decrypt_cmd, check=True)

        with open(self.plaintext_path, 'rb') as orig, open(self.temp_dec, 'rb') as dec:
            self.assertEqual(orig.read(), dec.read())

    def test_ecb_mode(self):
        self.run_encrypt_decrypt('ecb')

    def test_cbc_mode(self):
        self.run_encrypt_decrypt('cbc', use_iv=True)

    def test_gcm_mode(self):
        self.run_encrypt_decrypt('gcm', use_iv=True, use_aad=True)

if __name__ == '__main__':
    unittest.main()


