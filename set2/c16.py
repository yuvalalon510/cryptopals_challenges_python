import c10 as crypto
import c15 as padding
from random import randint

class CBC_Oracle:
    
    def __init__(self):
        self._blocksize = 16
        self._key = bytes(randint(0, 0xFF) for i in range(self._blocksize))
        self._iv = bytes(randint(0, 0xFF) for i in range(self._blocksize))
        self._pref = b"comment1=cooking%20MCs;userdata="    
        self._suff = b";comment2=%20like%20a%20pound%20of%20bacon"
    
    def encrypt(self, data):
        data = data.replace("=","'='").replace(";","';'").encode() 
        data = padding.pad_pkcs7(self._pref + data + self._suff)
        return crypto.AES_Encrypt_CBC(data, self._key, self._iv)
    
    def is_admin(self, data):
        decrypted = crypto.AES_Decrypt_CBC(data, self._key, self._iv)
        return padding.unpad_pkcs7(decrypted).__contains__(b";admin=true;")

if __name__ == "__main__":
    oracle = CBC_Oracle()
    data = "A"*16 + ":admin<true:"
    cipher = bytearray(oracle.encrypt(data))
    # Flip three bits from the ciphertext at the position of our
    # encrypted AAA... block.
    # Flipping bits in the CBC cipher produces the same errors in the next block
    # so when decrypted, :admin<true: becomes ;admin=true;
    cipher[32] ^= 1
    cipher[38] ^= 1
    cipher[43] ^= 1

    cipher = bytes(cipher)
    print(oracle.is_admin(cipher))