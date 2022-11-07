import struct
from c28 import sha1, sha1_mac
import random

"""Return a SHA-1 padding for a message of length in bytes"""
def md_padding(length):
    ml = length * 8
    padding = bytes([0x80])
    while (ml + 8 * len(padding)) % 512 != 448:
        padding += bytes([0x00])
    padding += struct.pack(">Q", ml)
    return padding

"""Execute a length extension attack
   message is the original message
   sha1_hash is the mac of the message with a secret key
   key_length is the length of the key used
   extension is the message to append at the end"""
def sha1_length_extension_attack(message: bytes, sha1_hash:bytes, key_length: int, extension: bytes):
    forged_message = message + md_padding(key_length + len(message)) + extension
    h0, h1, h2, h3, h4 = struct.unpack(">5I", sha1_hash)
    return forged_message, sha1(extension, h0, h1, h2, h3, h4, (key_length + len(forged_message))*8)

if __name__ == "__main__":
    msg = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    key = bytes(random.randint(0, 0xff) for i in range(random.randint(1, 32))) #Random key of random length, unknown to the attacker
    ext = b";admin=true"
    
    h = sha1_mac(msg, key)
    for i in range(1, 33):
        # Try to forge the new message for different key lengths
        forged_message, signature = sha1_length_extension_attack(msg, bytes.fromhex(h), i, ext)
        digest = sha1_mac(forged_message, key)
        if signature == digest:
            print("Key Length:", i)
            print("Forged message:", forged_message)
            print("Signature:", signature)
            break
    assert(signature == sha1_mac(forged_message, key))