import c10
import c9 as padding
import random
from base64 import b64decode

appended_str = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg" \
                + "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq" \
                + "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg" \
                + "YnkK"

key = b"\rO\xacJk\x87\x9e\xf9B3\xf5\xc7\xef\xf3\xbc\x1c"

def encryption_orcale(data):
    padded_data = padding.pad(data + b64decode(appended_str))
    cipher = c10.AES_Encrypt_ECB(padded_data, key)
    return cipher

def detect_ecb_block_size(max_size):
    for blocksize in range(1, max_size+1):
        
        # Encrypt a repeated string of guessed block size
        cipher = encryption_orcale(bytes(ord("A") for i in range(2*blocksize)))

        if cipher[:blocksize] == cipher[blocksize:2*blocksize]:
            # Detected ECB and block size
            return blocksize

    # Discovered no block size in range
    return -1


def decrypt_ecb():
    blocksize = detect_ecb_block_size(64)
    assert(blocksize > 0)
    # Now we know the function is using ECB, and which block size.

    # Get the length of the secret string padded by the oracle
    length = len(encryption_orcale(b""))
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
                possible_ciphers[possible_block] = encryption_orcale(possible_block)[:blocksize]

            # Compare the cipher with the dictionary to get the last byte of the block
            cipher = encryption_orcale(short_block)[offset:offset+min(blocksize, length-offset)]
            for entry, output in possible_ciphers.items():
                if output == cipher:
                    # The last byte of the chosen cipher is the next byte of the secret
                    secret += bytes([entry[-1]])
                    short_block = short_block[1:]
        
        short_block = secret[-blocksize+1:]
        offset += blocksize

    return secret

if __name__ == "__main__":
    print(decrypt_ecb().decode("utf-8"))

