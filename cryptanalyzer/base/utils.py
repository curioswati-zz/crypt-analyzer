import time

from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.Cipher import Blowfish


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


class DES3Cipher(BaseCipher):
    def __init__(self, key, text):
        self.key = key
        self.text = text

        # prepare cipher object
        self.key = self.make_valid_input(self.key)
        self.cipher_obj = DES3.new(self.key, DES3.MODE_ECB)


class BlowfishCipher(BaseCipher):
    def __init__(self, key, text):
        self.key = key
        self.text = text

        # prepare cipher object
        self.key = self.make_valid_input(self.key)
        self.cipher_obj = Blowfish.new(self.key, Blowfish.MODE_ECB)


class TwofishCipher(BaseCipher):
    def __init__(self, key, text):
        self.key = key
        self.text = text

        # prepare cipher object
        self.key = self.make_valid_input(self.key)
        self.cipher_obj = AES.new(self.key, AES.MODE_ECB)


class RC6Cipher(BaseCipher):
    def __init__(self, key, text):
        self.key = key
        self.text = text

        # prepare cipher object
        self.key = self.make_valid_input(self.key)
        self.cipher_obj = AES.new(self.key, AES.MODE_ECB)


class Analyzer():
    def __init__(self):
        pass

    def analyze(self, analysis_type, algorithms, key, files):
        algo_choices = {'aes': 'AESCipher',
                        'des': 'DES3Cipher',
                        'blowfish': 'BlowfishCipher',
                        'twofish': 'TwoCipher',
                        'rc6': 'RCCipher'
                        }

        # iterate over the selected algorithms by user
        for algo in algorithms:
            if algo in algo_choices:
                class_instance = eval(algo_choices[algo])
                algo_obj = class_instance(key=key, text=None)

                for f in files:
                    algo_obj.text = f['content']
                    key = algo+"_time"
                    if analysis_type == "encryption":
                        f[key] = self.calc_enc_time(algo_obj)

                    elif analysis_type == "decryption":
                        f[key] = self.calc_dec_time(algo_obj)

        print(files)
        return files

    def calc_enc_time(self, algo_obj):
        taken_times = []
        for i in range(10):
            start = time.clock()
            eval('algo_obj.encrypt')()
            stop = time.clock()
            taken_times.append(stop - start)

        return sum(taken_times) / float(len(taken_times))

    def calc_dec_time(self, algo_obj):
        algo_obj.encrypt()

        taken_times = []
        for i in range(10):
            start = time.clock()
            eval('algo_obj.decrypt')()
            stop = time.clock()
            taken_times.append(stop - start)

        return sum(taken_times) / float(len(taken_times))
