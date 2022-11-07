from md4 import MD4
import random
import struct

"""Return a message padded with the same padding MD4 algorithm does"""
def md4_padding(msg: bytes):
    ml = len(msg) * 8
    msg += b"\x80"
    msg += b"\x00" * (-(len(msg) + 8) % 64)
    msg += struct.pack("<Q", ml)
    return msg

"""Execute a length extension attack
   message is the original message
   md4_hash is the mac of the message with a secret key
   key_length is the length of the key used
   extension is the message to append at the end"""
def md4_length_extension_attack(message: bytes, md4_hash:bytes, key_length: int, extension: bytes):
    forged_message = md4_padding(b'A'*key_length + message) + extension
    forged_message = forged_message[key_length:]
    h0, h1, h2, h3 = struct.unpack("<4I", md4_hash)
    return forged_message, MD4(extension, [h0, h1, h2, h3], (key_length + len(forged_message))*8).bytes()

"""Compute a signature for the message using the key, MD4(key + message)"""
def md4_mac(message: bytes, key: bytes):
    return MD4(key + message).bytes()

if __name__ == "__main__":
    msg = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    key = bytes(random.randint(0, 0xff) for i in range(0)) #Random key of random length, unknown to the attacker
    ext = b";admin=true"
    
    h = md4_mac(msg, key)
    for i in range(0, 33):
        # Try to forge the new message for different key lengths
        forged_message, signature = md4_length_extension_attack(msg, h, i, ext)
        digest = md4_mac(forged_message, key)
        if signature == digest:
            print("Key Length:", i)
            print("Forged message:", forged_message)
            print("Signature:", signature)
            break
    assert(signature == md4_mac(forged_message, key))

