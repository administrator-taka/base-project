import unittest

from cryptography.fernet import Fernet


class Encryption:
    def __init__(self, key=None):
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        encrypted_data = self.cipher.encrypt(data.encode())
        return encrypted_data

    def decrypt(self, encrypted_data):
        decrypted_data = self.cipher.decrypt(encrypted_data).decode()
        return decrypted_data


class TestEncryption(unittest.TestCase):
    def test_encrypt_decrypt(self):
        data_to_encrypt = "This is some secret data."
        encryption = Encryption()
        encrypted_data = encryption.encrypt(data_to_encrypt)
        decrypted_data = encryption.decrypt(encrypted_data)
        self.assertEqual(data_to_encrypt, decrypted_data)

    def test_custom_key(self):
        custom_key = b'6_j4tAdNX0lEOOkL1hNLNNvdyk2Z8uTJsjKqzXQfGM8='
        data_to_encrypt = "This is some secret data."
        encryption = Encryption(custom_key)
        encrypted_data = encryption.encrypt(data_to_encrypt)
        decrypted_data = encryption.decrypt(encrypted_data)
        self.assertEqual(data_to_encrypt, decrypted_data)

    def test_additional_functionality(self):
        # 追加の動作確認を行うためのメソッド
        encryption = Encryption()
        data_to_encrypt = "This is some additional secret data."
        encrypted_data = encryption.encrypt(data_to_encrypt)
        # 追加の暗号化されたデータと鍵を出力
        print("encrypted_data:", encrypted_data)
        print("custom_key:", encryption.key)

    def test(self):
        custom_key = b'44UEVToWihZk3GGlAZrvfpAX_SkTcQffvIKRwR0Dpu8='
        encryption = Encryption(custom_key)
        encrypted_data = b'gAAAAABmO4KFO9fYcppAHwYhxFEno2c_AD8EPolnqE56pXy4bMrF2uMRb-xxE10faGNDKm2y3W_uV8fzH4IyWFmK7HREszyYsbTDPvp6vHqo-5ZMGd3-39hVBVK4ixGpVbpoS8i7Jui8'
        decrypted_data = encryption.decrypt(encrypted_data)
        print("decrypted_data:", decrypted_data)


if __name__ == '__main__':
    unittest.main()
