import time

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


class Analyzer():
    def __init__(self, algorithms, key):
        algo_choices = {'aes': 'AESCipher',
                        'des': 'DESCipher',
                        'blowfish': 'BlowCipher',
                        'twofish': 'TwoCipher',
                        'rc6': 'RCCipher'
                        }

        self.algo_objs = []

        for algo in algorithms:
            if algo in algo_choices:
                class_instance = eval(algo_choices[algo])
                self.algo_objs.append(class_instance(key=key, text=None))

    def analyze(self, files):
        for algo_obj in self.algo_objs:
            for f in files:
                algo_obj.text = f['content']
                f['encryption_time'] = self.calc_time(algo_obj)

        return files

    def calc_time(self, algo_obj):
        start = time.clock()
        eval('algo_obj.encrypt')
        stop = time.clock()
        total = stop - start
        return total
