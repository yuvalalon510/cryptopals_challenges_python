import c18 as crypto
from base64 import b64decode
from random import randint
import set1.c3
import set1.c2

### Note: This challenge and the next one are similar, I used the statistical
###       approach suggested by the next challenge to solve both of them.

def break_aes_ctr(ciphers):
    keystream = b""

    # Each column was xor'd with the same keystream byte
    # Therefore we treat each column as a single character cipher
    for i in range(max(len(c) for c in ciphers)):
        
        block = b""
        for c in ciphers:
            block += bytes([c[i]]) if i < len(c) else b''
        
        # Append key that produces the highest english score.
        keystream += bytes([get_keystream_byte(block)])

    return keystream

def get_keystream_byte(block):

    max_score, bestkey = 0, 0

    # for every possible key
    for k in range(256):

        # produce text from the cipher and the key
        P = set1.c3.xor_single_byte(block, k)
        if not all(c < 128 for c in P):
            continue

        # save key with the best text
        plaintext = P.decode("utf-8")
        score = set1.c3.score_text(plaintext)
        if score > max_score:
            max_score = score
            bestkey = k
    
    return bestkey


if __name__ == "__main__":
    with open("19.txt") as f:
        strings = [b64decode(s) for s in f.readlines()]

    encrypted = []
    key = bytes(randint(0, 0xFF) for i in range(16))
    for s in strings:
        ctr = crypto.AES_CTR(key, 0)
        encrypted.append(ctr.encrypt(s))
    
    keystream = break_aes_ctr(encrypted)

    # We got an almost accurate keystream, because the ciphers
    # are of different lengths, therefore part of the keystream
    # was used in few strings, and simple guesses by context can be 
    # used to complete the decryption.

    for c in encrypted:
        p = bytes.fromhex(set1.c2.xor(c, keystream[:len(c)])).decode()
        print(p)
