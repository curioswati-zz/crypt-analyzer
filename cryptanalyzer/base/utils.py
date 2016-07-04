from Crypto.Cipher import AES


class BaseCipher():
    def make_valid_input(self, in_str):
        if len(in_str) % 16:
            quotient = len(in_str) % 16
            in_str += "X" * (16-quotient)
        return in_str

    def encrypt(self):
        text = self.make_valid_input(self.text)
        self.ciph = self.cipher_obj.encrypt(text)

    def decrypt(self):
        return self.cipher_obj.decrypt(self.ciph)[:len(self.text)]


class AESCipher(BaseCipher):
    def __init__(self, key, text):
        self.key = key
        self.text = text

        # prepare cipher object
        self.key = self.make_valid_input(self.key)
        self.cipher_obj = AES.new(self.key, AES.MODE_ECB)


class DESCipher(BaseCipher):
    def __init__(self, key, text):
        self.key = key
        self.text = text

        # prepare cipher object
        self.key = self.make_valid_input(self.key)
        self.cipher_obj = AES.new(self.key, AES.MODE_ECB)


class BlowCipher(BaseCipher):
    def __init__(self, key, text):
        self.key = key
        self.text = text

        # prepare cipher object
        self.key = self.make_valid_input(self.key)
        self.cipher_obj = AES.new(self.key, AES.MODE_ECB)


class TwoCipher(BaseCipher):
    def __init__(self, key, text):
        self.key = key
        self.text = text

        # prepare cipher object
        self.key = self.make_valid_input(self.key)
        self.cipher_obj = AES.new(self.key, AES.MODE_ECB)


class RCCipher(BaseCipher):
    def __init__(self, key, text):
        self.key = key
        self.text = text

        # prepare cipher object
        self.key = self.make_valid_input(self.key)
        self.cipher_obj = AES.new(self.key, AES.MODE_ECB)


def encrypt(key, files, algorithms):
    algos = {'aes': AESCipher(key=key, text=None),
             'des': DESCipher(key=key, text=None),
             'blowfish': BlowCipher(key=key, text=None),
             'twofish': TwoCipher(key=key, text=None),
             'rc6': RCCipher(key=key, text=None)
             }
    print(algorithms)
    print(key)
