from set3.c18 import AES_CTR
from random import randint

class CipherSeeker:

    key = bytes(randint(0,255) for i in range(16))

    def __init__(self):
        self.oracle = AES_CTR(self.key, 0)
        with open("25.txt", "r") as f:
            self.cipher = self.oracle.encrypt(f.read().encode())
        
    def get_cipher(self):
        return self.cipher
    
    def edit(self, ciphertext, offset, newtext):
        ptext = self.oracle.decrypt(ciphertext)
        st1 = ptext[:offset]
        st2 = ptext[offset+len(newtext):]
        ptext = st1 + newtext + st2
        return self.oracle.encrypt(ptext)


if __name__ == "__main__":
    cs = CipherSeeker()
    c1 = cs.get_cipher()
    # c1 is the cipher, we know that the edit function will encrypt using the same
    # keystream, so we can send c1 which will be xor'd with the same one used to encrypt it, and give us back
    # the plaintext
    c2 = cs.edit(c1, 0, c1) 
    print(c2)

