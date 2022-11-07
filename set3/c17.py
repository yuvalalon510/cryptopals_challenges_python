import set2.c10 as crypto
import set2.c15 as padding
from random import randint
from base64 import b64decode

class CBC_Padding_Oracle:

    def __init__(self):
        self._blocksize = 16
        self._key = bytes(randint(0, 0xFF) for i in range(self._blocksize))
        self._iv = bytes(randint(0, 0xFF) for i in range(self._blocksize))
        with open("17.txt") as strings:
            self._strings = strings.readlines()
        

    def encrypt(self):
        i = randint(0, len(self._strings)-1)
        data = padding.pad_pkcs7(b64decode(self._strings[i]))
        return self._iv + crypto.AES_Encrypt_CBC(data, self._key, self._iv)
    
    def decrypt(self, data: bytes):
        data = crypto.AES_Decrypt_CBC(data, self._key, self._iv)[self._blocksize:]
        try:
            padding.unpad_pkcs7(data)
        except ValueError:
            return False
        return True

def cbc_padding_attack(oracle, C):
    blocksize = 16
    C = [C[i:i+blocksize] for i in range(0, len(C), blocksize)]
    P = b""

    for n in range(len(C)-1, 0, -1):

        corrupt_block = bytearray(ord('A') for i in range(blocksize))
        p_block = bytearray(blocksize)
        I = bytearray(blocksize)

        for i in range(blocksize-1, -1, -1):

            target_padding = blocksize - i
            for j in range(i+1, blocksize):
                corrupt_block[j] = target_padding ^ I[j]

            for b in range(256):
                corrupt_block[i] = b
                correct_padding = oracle.decrypt(bytes(corrupt_block) + C[n])
                if correct_padding:
                    I[i] = corrupt_block[i] ^ target_padding
                    p_block[i] = C[n-1][i] ^ I[i]
                    break

        P = bytes(p_block) + P
    
    return P

if __name__ == "__main__":
    oracle = CBC_Padding_Oracle()
    print(cbc_padding_attack(oracle, oracle.encrypt()))