import c10 as crypto
import c9 as padding
import random

class Oracle:

    def __init__(self):
        self._key = bytes(random.randint(0, 0xFF) for i in range(16))
    
    def encrypt(self, email):
        encoded = encode_kv(profile_for(email)).encode()
        return crypto.AES_Encrypt_ECB(padding.pad(encoded), self._key)
    
    def decrypt(self, cipher):
        data = crypto.AES_Decrypt_ECB(cipher, self._key)
        data = padding.unpad(data).decode()
        return parse_kv(data)


def encode_kv(profile: dict):
    encoded_obj = ""

    for key, value in profile.items():
        encoded_obj += key + "=" + str(value) + "&"

    return encoded_obj[:-1]

def parse_kv(encoded_obj: str):
    output = {}
    for item in encoded_obj.split("&"):
        key, value = item.split("=")
        if value.isdecimal():
            value = int(value)
        output[key] = value

    return output

def profile_for(email: str):
    email = email.replace("&", "").replace("=","")

    profile = {
        'email': email,
        'uid': 10,
        'role': 'user'
    }

    return profile

def cut_and_paste_attack():
    oracle = Oracle()
    
    # We want a cipher such that the last block contains only the value of role
    # BLOCK 1           BLOCK 2             BLOCK 3
    # email=name@mail.  com&uid=10&role=    user\x0C\x0C\x0C...    
    cipher_a = oracle.encrypt("name@mail.com")
    profile_no_role = cipher_a[:32]

    # We want to this to show instead of 'user'
    # We pad it so that we can cut it from
    # the cipher and it will decrypt to 'admin'
    cut = b"admin"+b"\x0B"*11

    # An email such that our cut will sit exactly in the
    # second block of the cipher
    # BLOCK 1           BLOCK 2             ...
    # email=aaa@bb.com  admin\x0B\x0B\x0B...
    email = "aaa@bb.com" + cut.decode()
    role_value = oracle.encrypt(email)[16:32]

    # Put the blocks together to make a valid profile with admin role
    # BLOCK 1           BLOCK 2          || BLOCK 3
    # email=name@mail.  com&uid=10&role=    admin\x0B\x0B\x0B...
    forged_admin = profile_no_role + role_value

    # The forged ciphertext decrypts to a profile with admin role
    return oracle.decrypt(forged_admin)


if __name__ == "__main__":
    print(cut_and_paste_attack())