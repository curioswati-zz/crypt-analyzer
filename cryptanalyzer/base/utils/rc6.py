from .helpers import *


class RC6():

    def __init__(self, key):
        self.key = generateKey(key)

    def encrypt(self, sentence):
        encoded = blockConverter(sentence)
        A = int(encoded[0], 2)
        B = int(encoded[1], 2)
        C = int(encoded[2], 2)
        D = int(encoded[3], 2)
        r = 12
        modulo = 2**32
        lgw = 5
        B = (B + self.key[0]) % modulo
        D = (D + self.key[1]) % modulo
        for i in range(1, r+1):
            t_temp = (B*(2*B + 1)) % modulo
            t = ROL(t_temp, lgw, 32)
            u_temp = (D*(2*D + 1)) % modulo
            u = ROL(u_temp, lgw, 32)
            tmod = t % 32
            umod = u % 32
            A = (ROL(A ^ t, umod, 32) + self.key[2*i]) % modulo
            C = (ROL(C ^ u, tmod, 32) + self.key[2*i + 1]) % modulo
            (A, B, C, D) = (B, C, D, A)
        A = (A + self.key[2*r + 2]) % modulo
        C = (C + self.key[2*r + 3]) % modulo
        cipher = []
        cipher.append(A)
        cipher.append(B)
        cipher.append(C)
        cipher.append(D)

        cipher = deBlocker(cipher)

        return cipher

    def decrypt(self, esentence):
        encoded = blockConverter(esentence)
        A = int(encoded[0], 2)
        B = int(encoded[1], 2)
        C = int(encoded[2], 2)
        D = int(encoded[3], 2)
        r = 12
        modulo = 2**32
        lgw = 5
        C = (C - self.key[2*r+3]) % modulo
        A = (A - self.key[2*r+2]) % modulo
        for j in range(1, r+1):
            i = r+1-j
            (A, B, C, D) = (D, A, B, C)
            u_temp = (D*(2*D + 1)) % modulo
            u = ROL(u_temp, lgw, 32)
            t_temp = (B*(2*B + 1)) % modulo
            t = ROL(t_temp, lgw, 32)
            tmod = t % 32
            umod = u % 32
            C = (ROR((C-self.key[2*i+1]) % modulo, tmod, 32) ^ u)
            A = (ROR((A-self.key[2*i]) % modulo, umod, 32) ^ t)
        D = (D - self.key[1]) % modulo
        B = (B - self.key[0]) % modulo
        orgi = []
        orgi.append(A)
        orgi.append(B)
        orgi.append(C)
        orgi.append(D)

        sentence = deBlocker(orgi)
        return sentence
