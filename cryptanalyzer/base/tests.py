from django.test import TestCase

from base.utils.analyzer import (
    AESCipher, DES3Cipher, BlowfishCipher,
    TwofishCipher, RC6Cipher
)


# Create your tests here.
class TestAnalyzer(TestCase):
    def test_aes_cipher(self):
        key = 'asdfjkl'
        text = open('/home/rebekah/Documents/texts/data_to_parse.txt').read()
        obj = AESCipher(key, text)
        obj.make_valid_text()
        obj.encrypt()
        obj.decrypt()
        self.assertEqual(obj.text, obj.original)

    def test_des_cipher(self):
        key = 'asdfjkl'
        text = open('/home/rebekah/Documents/texts/data_to_parse.txt').read()
        obj = DES3Cipher(key, text)
        obj.make_valid_text()
        obj.encrypt()
        obj.decrypt()
        self.assertEqual(obj.text, obj.original)

    def test_blowfish_cipher(self):
        key = 'asdfjkl'
        text = open('/home/rebekah/Documents/texts/data_to_parse.txt').read()
        obj = BlowfishCipher(key, text)
        obj.make_valid_text()
        obj.encrypt()
        obj.decrypt()
        self.assertEqual(obj.text, obj.original)

    def test_twofish_cipher(self):
        key = 'asdfjkl'
        text = open('/home/rebekah/Documents/texts/data_to_parse.txt').read()
        obj = TwofishCipher(key, text)
        obj.make_valid_text()
        obj.encrypt()
        obj.decrypt()
        self.assertEqual(obj.text, obj.original)

    def test_rc6_cipher(self):
        key = 'asdfjkl'
        text = open('/home/rebekah/Documents/texts/data_to_parse.txt').read()
        obj = RC6Cipher(key, text)
        obj.make_valid_text()
        obj.encrypt()
        obj.decrypt()
        self.assertEqual(obj.text, obj.original)
