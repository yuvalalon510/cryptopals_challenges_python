from base64 import b64decode
from Crypto.Cipher import AES

def AES_Encrypt_CBC(plaintext, key, iv):
    assert(len(key) == len(iv) == 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return cipher.encrypt(plaintext)

def AES_Decrypt_CBC(ciphertext, key, iv):
    assert(len(key) == len(iv) == 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(ciphertext)

def AES_Encrypt_ECB(plaintext, key):
    assert(len(key) == 16)
    cipher = AES.new(key, AES.MODE_ECB)

    return cipher.encrypt(plaintext)

def AES_Decrypt_ECB(ciphertext, key):
    assert(len(key) == 16)
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(ciphertext)


if __name__ == "__main__":
    with open("10.txt", "r") as f:
        ciphertext = b64decode(f.read())

    key = b"YELLOW SUBMARINE"
    decrypted = AES_Decrypt_CBC(ciphertext, key, bytes(16))
    encrypted = AES_Encrypt_CBC(decrypted, key, bytes(16))
    print(decrypted.decode())
    assert(encrypted == ciphertext)