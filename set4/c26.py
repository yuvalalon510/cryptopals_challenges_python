from set3.c18 import AES_CTR
from random import randint

class CTR_Oracle:
    
    def __init__(self):
        self._key = bytes(randint(0, 0xFF) for i in range(16))
        self.oracle = AES_CTR(self._key, 0)
        self._pref = b"comment1=cooking%20MCs;userdata="    
        self._suff = b";comment2=%20like%20a%20pound%20of%20bacon"
    
    def encrypt(self, data):
        data = data.replace("=","'='").replace(";","';'").encode() 
        return self.oracle.encrypt(self._pref + data + self._suff)
    
    def is_admin(self, data):
        decrypted = self.oracle.decrypt(data)
        return (b";admin=true;" in decrypted)

if __name__ == "__main__":
    oracle = CTR_Oracle()
    data = ":admin<true:"
    cipher = bytearray(oracle.encrypt(data))
    # Flipping bits in the cipher produces the same errors
    # in the same place when decrypted, so : becomes ; and < becomes =
    cipher[32] ^= 1
    cipher[38] ^= 1
    cipher[43] ^= 1

    cipher = bytes(cipher)
    print(oracle.is_admin(cipher))