import time

from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.Cipher import Blowfish
from twofish import Twofish

from .rc6 import RC6
from . import utils


class BaseCipher():

    def make_valid_text(self):
        self.text = str(self.text)

        if (
            isinstance(self, AESCipher) or
            isinstance(self, TwofishCipher) or
            isinstance(self, RC6Cipher)
           ):
            min_multiple = 16
        else:
            min_multiple = 8

        quotient = len(self.text) % min_multiple
        if quotient:
            self.text += "X" * (min_multiple - quotient)

    def make_valid_key(self):
        self.key = str(self.key)

        quotient = len(self.key) % 16

        if quotient:
            self.key += "X" * (16 - quotient)

        if isinstance(self, DES3Cipher):
            self.key = self.key[:24]

    def encrypt(self):
        self.ciph = self.cipher_obj.encrypt(self.text)

    def decrypt(self):
        to_return = self.cipher_obj.decrypt(self.ciph)[:len(self.text)]
        return to_return


class AESCipher(BaseCipher):

    def __init__(self, key, text):
        self.key = key
        self.text = text
        self.original = text

        # prepare cipher object
        self.make_valid_key()
        self.cipher_obj = AES.new(self.key, AES.MODE_ECB)


class DES3Cipher(BaseCipher):

    def __init__(self, key, text):
        self.key = key
        self.text = text
        self.original = text

        # prepare cipher object
        self.make_valid_key()
        self.cipher_obj = DES3.new(self.key, DES3.MODE_ECB)


class BlowfishCipher(BaseCipher):

    def __init__(self, key, text):
        self.key = key
        self.text = text
        self.original = text

        # prepare cipher object
        self.make_valid_key()
        self.cipher_obj = Blowfish.new(self.key, Blowfish.MODE_ECB)

    def make_valid_key(self):
        if len(self.key) < 4:
            self.key += "X" * (4 - len(self.key))


class TwofishCipher(BaseCipher):

    def __init__(self, key, text):
        self.key = key
        self.text = text
        self.original = text

        # prepare cipher object
        self.make_valid_key()
        self.cipher_obj = Twofish(self.key.encode())

    def make_valid_key(self):
        pass

    def encrypt(self):
        parts = [self.text[i:i+16] for i in range(0, len(self.text), 16)]
        self.ciph = []

        for part in parts:
            ciph = self.cipher_obj.encrypt(part.encode())
            self.ciph.append(ciph)

    def decrypt(self):
        decrypted = []

        for encrypted_part in self.ciph:
            decrypted_part = self.cipher_obj.decrypt(encrypted_part)
            decrypted.append(decrypted_part)

        return ''.join(map(lambda x: x.decode(), decrypted))[:len(self.original)]


class RC6Cipher(BaseCipher):

    def __init__(self, key, text):
        self.key = key
        self.text = text
        self.original = text

        # prepare cipher object
        self.make_valid_key()
        self.cipher_obj = RC6(self.key)

    def make_valid_key(self):
        if len(self.key) < 16:
            self.key += "X" * (16 - len(self.key))
        self.key = self.key[:16]

    def encrypt(self):
        parts = [self.text[i:i+16] for i in range(0, len(self.text), 16)]
        self.ciph = []

        for part in parts:
            ciph = self.cipher_obj.encrypt(part)
            self.ciph.append(ciph)

    def decrypt(self):
        decrypted = []

        for encrypted_part in self.ciph:
            decrypted_part = self.cipher_obj.decrypt(encrypted_part)
            decrypted.append(decrypted_part)

        return ''.join(decrypted)[:len(self.original)]


class Analyzer():

    def __init__(self):
        pass

    def analyze_varying_data(self, analysis_type, algorithms, key, files):
        algo_choices = {'aes': 'AESCipher',
                        'des': 'DES3Cipher',
                        'blowfish': 'BlowfishCipher',
                        'twofish': 'TwofishCipher',
                        'rc6': 'RC6Cipher'
                        }

        # iterate over the selected algorithms by user
        for algo in algorithms:
            if algo in algo_choices:
                class_instance = eval(algo_choices[algo])
                algo_obj = class_instance(key=key, text=None)

                for datafile in files:
                    algo_obj.text = datafile['content']
                    algo_obj.original = datafile['content']
                    algo_obj.make_valid_text()

                    key = algo+"_time"
                    if analysis_type == "encryption":
                        datafile[key] = self.calc_enc_time(algo_obj)

                        # save encrypted file for later decryption
                        file_instance = utils.save_encrypted_file(datafile['name'],
                                                                  algo_obj.ciph)
                        datafile['file_path'] = file_instance.file_data.path

                    elif analysis_type == "decryption":
                        datafile[key] = self.calc_dec_time(algo_obj)

        return files

    def analyze_varying_key(self, analysis_type, algorithms, data, keys):
        algo_choices = {'aes': 'AESCipher',
                        'des': 'DES3Cipher',
                        'blowfish': 'BlowfishCipher',
                        'twofish': 'TwofishCipher',
                        'rc6': 'RC6Cipher'
                        }

        # iterate over the selected algorithms by user
        for algo in algorithms:
            if algo in algo_choices:
                class_instance = eval(algo_choices[algo])

                for keyfile in keys:
                    stripped_key = keyfile['content'][2:-1]
                    algo_obj = class_instance(key=stripped_key, text=data)
                    algo_obj.make_valid_text()

                    key = algo+"_time"
                    if analysis_type == "encryption":
                        keyfile[key] = self.calc_enc_time(algo_obj)

                        # save encrypted file for later decryption
                        file_instance = utils.save_encrypted_file(keyfile['name'],
                                                                  algo_obj.ciph)

                        keyfile['file_path'] = file_instance.file_data.path

                    elif analysis_type == "decryption":
                        keyfile[key] = self.calc_dec_time(algo_obj)

        return keys

    def calc_enc_time(self, algo_obj):
        taken_times = []
        for i in range(5):
            start = time.clock()
            eval('algo_obj.encrypt')()
            stop = time.clock()
            taken_times.append(stop - start)

        return sum(taken_times) / float(len(taken_times))

    def calc_dec_time(self, algo_obj):
        algo_obj.encrypt()

        taken_times = []
        for i in range(5):
            start = time.clock()
            eval('algo_obj.decrypt')()
            stop = time.clock()
            taken_times.append(stop - start)

        return sum(taken_times) / float(len(taken_times))
