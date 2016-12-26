import os
import pickle
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
        if not self.original:
            trim_len = None
        else:
            trim_len = len(self.original)

        if trim_len:
            decrypted = self.cipher_obj.decrypt(self.ciph)[:trim_len]
        else:
            decrypted = self.cipher_obj.decrypt(self.ciph)

        self.text = decrypted.decode()


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
        parts = [self.text[i:i+16] for i in range(0, len(self.original), 16)]
        ciph = []

        for part in parts:
            part_ciph = self.cipher_obj.encrypt(part.encode())
            ciph.append(part_ciph)

        self.ciph = ciph

    def decrypt(self):
        if not self.original:
            trim_len = None
        else:
            trim_len = len(self.original)

        decrypted = []

        for encrypted_part in self.ciph:
            decrypted_part = self.cipher_obj.decrypt(encrypted_part)
            decrypted.append(decrypted_part)

        # if encrypted with varying key length then we don't have original content to trim
        # the output to so take complete content as output.
        if trim_len:
            self.text = ''.join(map(lambda x: x.decode(), decrypted))[:trim_len]
        else:
            self.text = ''.join(map(lambda x: x.decode(), decrypted))


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
        parts = [self.text[i:i+16] for i in range(0, len(self.original), 16)]
        ciph = []

        for part in parts:
            part_ciph = self.cipher_obj.encrypt(part)
            ciph.append(part_ciph.encode())

        self.ciph = ciph

    def decrypt(self):
        if not self.original:
            trim_len = None
        else:
            trim_len = len(self.original)

        decrypted = []

        for encrypted_part in self.ciph:
            decrypted_part = self.cipher_obj.decrypt(encrypted_part.decode())
            decrypted.append(decrypted_part)

        # if encrypted with varying key length then we don't have original content to trim
        # the output to so take complete content as output.
        if trim_len:
            self.text = ''.join(decrypted)[:trim_len]
        else:
            self.text = ''.join(decrypted)


class Analyzer():

    def __init__(self):
        self.algo_choices = {'aes': 'AESCipher',
                             'des': 'DES3Cipher',
                             'blowfish': 'BlowfishCipher',
                             'twofish': 'TwofishCipher',
                             'rc6': 'RC6Cipher'
                             }

    def encrypt_varying_data(self, algorithms, key, files):
        # iterate over the selected algorithms by user
        for algo in algorithms:
            class_instance = eval(self.algo_choices[algo])
            algo_obj = class_instance(key=key, text=None)

            for datafile in files:
                text = datafile['content']
                algo_obj.text = text
                algo_obj.original = text

                algo_obj.make_valid_text()

                datafile[algo+"_time"] = self.calc_enc_time(algo_obj)

                # save encrypted file for later decryption
                filename = utils.save_encrypted_file(algo, datafile['name'],
                                                     algo_obj.ciph)
                datafile[algo+'_encrypted'] = filename

        return files

    def decrypt_varying_data(self, algorithms, key, files):
        for algo in algorithms:
            class_instance = eval(self.algo_choices[algo])
            algo_obj = class_instance(key=key, text=None)

            for datafile in files:
                f = open(datafile[algo + "_encrypted"], 'rb')

                if algo in ['twofish', 'rc6']:
                    text = pickle.load(f)
                else:
                    text = f.read()
                    f.close()

                algo_obj.ciph = text
                algo_obj.make_valid_text()

                text = datafile['content']
                algo_obj.original = text

                datafile[algo+"_time"] = self.calc_dec_time(algo_obj)

                os.remove(datafile[algo + "_encrypted"])

        return files

    def encrypt_varying_key(self, algorithms, data, keys, data_file_name):
        # iterate over the selected algorithms by user
        for algo in algorithms:
            class_instance = eval(self.algo_choices[algo])

            for keyfile in keys:
                stripped_key = keyfile['content'][2:-1]
                algo_obj = class_instance(key=stripped_key, text=data)

                algo_obj.make_valid_text()

                keyfile[algo+"_time"] = self.calc_enc_time(algo_obj)

                # save encrypted file for later decryption
                name = data_file_name + "_" + keyfile['name']
                filename = utils.save_encrypted_file(algo, name, algo_obj.ciph)
                keyfile[algo+'_encrypted'] = filename

        return keys

    def decrypt_varying_key(self, algorithms, keys):
        # iterate over the selected algorithms by user
        for algo in algorithms:
            class_instance = eval(self.algo_choices[algo])

            for keyfile in keys:
                stripped_key = keyfile['content'][2:-1]

                f = open(keyfile[algo + '_encrypted'], 'rb')

                if algo in ['twofish', 'rc6']:
                    data = pickle.load(f)
                else:
                    data = f.read()
                    f.close()

                algo_obj = class_instance(key=stripped_key, text=None)
                algo_obj.ciph = data
                algo_obj.original = None

                algo_obj.make_valid_text()

                keyfile[algo+"_time"] = self.calc_dec_time(algo_obj)

                os.remove(keyfile[algo + "_encrypted"])

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
        taken_times = []
        for i in range(5):
            start = time.clock()
            eval('algo_obj.decrypt')()
            stop = time.clock()
            taken_times.append(stop - start)

        return sum(taken_times) / float(len(taken_times))
