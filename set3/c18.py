from Crypto.Cipher import AES
from struct import pack
from base64 import b64decode
from base64 import b64encode

class AES_CTR:

    def __init__(self, key: bytes, nonce: int):
        self._key = key
        self._nonce = nonce
        self._blocksize = 16
        self._ECB = AES.new(key, AES.MODE_ECB)
        self._count = 0

    def encrypt(self, data: bytes):
        keystream = b""
        self._count = 0

        while len(keystream) < len(data):
            counter_block = pack("<QQ", self._nonce, self._count)
            keystream += self._ECB.encrypt(counter_block)
            self._count += 1

        return xor_bytes(data, keystream[:len(data)])

    def decrypt(self, data: bytes):
        return self.encrypt(data)

        
def xor_bytes(st1: bytes, st2: bytes):
    return bytes(x ^ y for (x, y) in zip(st1, st2))

if __name__ == "__main__":
    st = """L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="""
    key = b"YELLOW SUBMARINE"
    ctr = AES_CTR(key, 0)
    ptext = ctr.decrypt(b64decode(st))
    print(b64encode(ctr.encrypt(ptext)))