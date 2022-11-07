from random import randint
import c9 as padding
from base64 import b64decode
import c10 as crypto

target_bytes = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg" \
                + "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq" \
                + "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg" \
                + "YnkK"

max_length = 0xFF
random_prefix = bytes(randint(0, 0xFF) for i in range(randint(0, max_length)))
key = b"\rO\xacJk\x87\x9e\xf9B3\xf5\xc7\xef\xf3\xbc\x1c"

def encryption_orcale(data):
    padded_data = padding.pad(random_prefix + data + b64decode(target_bytes))
    cipher = crypto.AES_Encrypt_ECB(padded_data, key)
    return cipher

def decrypt_ecb_harder():
    blocksize = 16
    
    # We need to find where the secret string starts
    # We will encrypt random_prefix || attack_prefix || target_bytes
    # with an attack_prefix of increasing size
    # until we discover two identical adjacent blocks
    attack_prefix = b""
    start = -1
    while start < 0:
        attack_prefix += bytes(ord('A') for i in range(1))
        cipher = encryption_orcale(attack_prefix)
        # Compare each pair of adjacent blocks
        for i in range(0, len(cipher) - 2*blocksize, blocksize):
            if cipher[i:i+blocksize] == cipher[i+blocksize:i+2*blocksize]:
                start = i + 2*blocksize
                # The secret string starts here
                break

    # Get the length of the secret string padded by the oracle
    length = len(encryption_orcale(attack_prefix)) - start
    secret = b""

    # Craft an input one byte short
    short_block = bytes(ord('A') for i in range(blocksize-1))

    # At each iteration, decrypt a block of bytes, 1 at a time
    # by feeding the oracle with shorter blocks
    # and comparing the input with a dictionary 
    # to get the block which produces the exact same cipher
    offset = 0
    while offset < length:

        for k in range(min(blocksize, length-offset)):

            possible_ciphers = {}
            for i in range(256):
                # Make a dictionary of ciphers produced by all blocks with all possible last bytes
                possible_block = short_block + secret[offset:offset+k] + bytes([i])
                possible_ciphers[possible_block] = encryption_orcale(attack_prefix + possible_block)[start:start+blocksize]

            # Compare the cipher with the dictionary to get the last byte of the block
            cipher = encryption_orcale(attack_prefix + short_block)[start+offset:start+offset+min(blocksize, length-offset)]
            for entry, output in possible_ciphers.items():
                if output == cipher:
                    secret += bytes([entry[-1]])
                    short_block = short_block[1:]
        
        short_block = secret[-blocksize+1:]
        offset += blocksize

    return secret


if __name__ == "__main__":
    print(decrypt_ecb_harder().decode())