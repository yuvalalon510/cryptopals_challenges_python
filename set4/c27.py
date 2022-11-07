import set2.c10 as crypto
import set2.c15 as padding
from random import randint

class CBC_Oracle:
    
    def __init__(self):
        self._blocksize = 16
        self._key = bytes(randint(0, 0xFF) for i in range(self._blocksize))
        print("Used key:", self._key)
        self._iv = self._key
        self._pref = b"comment1=cooking%20MCs;userdata="    
        self._suff = b";comment2=%20like%20a%20pound%20of%20bacon"
    
    def encrypt(self, data):
        data = data.replace("=","'='").replace(";","';'").encode() 
        data = padding.pad_pkcs7(self._pref + data + self._suff)
        return crypto.AES_Encrypt_CBC(data, self._key, self._iv)
    
    def decrypt(self, data):
        decrypted = padding.unpad_pkcs7(crypto.AES_Decrypt_CBC(data, self._key, self._iv))
        if not all(c < 128 for c in decrypted):
            return b"ERROR: High ascii found\n" + decrypted
        return decrypted
    
if __name__ == "__main__":
    oracle = CBC_Oracle()
    msg = "?"*16
    encrypted_msg = oracle.encrypt(msg)
    modified_cipher = encrypted_msg[:16] + bytes(0 for i in range(16)) + encrypted_msg[:]
    decrypted_str = oracle.decrypt(modified_cipher)[24:]
    key = bytes(x ^ y for (x,y) in zip(decrypted_str[:16], decrypted_str[32:48]))
    print("Extracted key:", key)



