from c21 import TwisterRNG
from random import randint
from struct import pack, unpack

def xor_bytes(st1: bytes, st2: bytes):
    return bytes(x ^ y for (x, y) in zip(st1, st2))

class RNGCipher:

    def __init__(self, _s):
        self._rng = TwisterRNG()
        self._seed = _s

    def encrypt(self, data):
        self._rng.seed(self._seed)
        ciphertext = b""
        keystream = b""

        for i in range(len(data)):
            if i % 4 == 0:
                keystream = pack(">I", self._rng.random()) 
            ciphertext += bytes([data[i] ^ keystream[i % 4]])

        return ciphertext
    
    def decrypt(self, data):
        return self.encrypt(data)

class Oracle:
    def __init__(self):
        self.__seed__ = 0xABCD # Secret 16 bit seed
    
    def encrypt(self, data):
        cipher = RNGCipher(self.__seed__)
        prefix = bytes(randint(0, 0xFF) for i in range(randint(0, 32)))
        return cipher.encrypt(prefix + data)

if __name__ == "__main__":
    oracle = Oracle()
    ciphertext = oracle.encrypt(b"A"*14)

    # if n divides by 4, then we can xor the plaintext with the ciphertext at bytes n-4 to n, and get
    # the n/4th 32-bit output of the rng
    n = len(ciphertext) - (len(ciphertext) % 4)
    keystream_part = xor_bytes(ciphertext[n-4:n], b"AAAA")
    rng_output = unpack(">I", keystream_part)[0]
    
    n = n // 4 - 1
    cloned_rng = TwisterRNG()

    # Iterate over all 16-bit possible seeds, there are only 2**16, until the same n/4th output is produced again 

    for s in range(2**16):

        cloned_rng.seed(s)

        for i in range(n):
            cloned_rng.random()

        # Compare the n/4th output with the original one to discover the seed
        if cloned_rng.random() == rng_output:
            print("seed is", s)
            break;


