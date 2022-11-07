from base64 import b64decode
from Crypto.Cipher import AES

def Decrypt_AES_128_ECB(ciphertext, key):
    assert(len(key) == 16)
    decipher = AES.new(key, AES.MODE_ECB)
    return decipher.decrypt(ciphertext)

def Encrypt_AES_128_ECB(plaintext, key):
    assert(len(key) == 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plaintext)

if __name__ == "__main__":
    with open("7.txt", "r") as f:
        encrypted_data = b64decode(f.read())
    print(Decrypt_AES_128_ECB(encrypted_data, b"YELLOW SUBMARINE").decode("utf-8"))