from base64 import b64decode
from itertools import combinations
import c3
import c5

count_bits = lambda x: sum((x >> i) & 1 for i in range(8))

def hamming_distance(s ,t):
    assert(len(s) == len(t))
    C = bytes(x ^ y for x,y in zip(s, t))
    return sum(count_bits(x) for x in C)

def break_repeating_xor(cipher):
    normalized_distances = {}

    for keysize in range(2, 41):
        
        # Get 4 chunks of key size
        chunks = [cipher[i:i + keysize] for i in range(0, len(cipher), keysize)][:4]

        # Calculate the normalized average hamming distance between pairs
        avg_distance = 0
        for (x, y) in combinations(chunks, 2):
            avg_distance += hamming_distance(x, y)
        
        avg_distance /= 6
        normalized_distances[keysize] = avg_distance / keysize

    # Select possible key sizes, with the lowest normalized distances.
    possible_keysizes = sorted(normalized_distances, key = normalized_distances.get)[:3]
    
    keys = []
    for keysize in possible_keysizes:
        
        key = ""

        for i in range(keysize):

            # Partition the text into blocks of keysize and transpose the blocks
            block = bytes(cipher[j] for j in range(i, len(cipher), keysize))

            # Treat each block as a single byte key and decrypt
            # The key which produces the text with the highest english score is the next character of the full key
            key += chr(c3.decrypt(block)[2])

        keys.append(key)

    return keys

if __name__ == "__main__":
    with open("6.txt", "r") as f:
        cipher = b64decode(f.read())

    cipher_ascii = cipher.decode("utf-8")
    for key in break_repeating_xor(cipher):
        print("--- using key:", key, "---")
        print(c5.xor_decryption(cipher_ascii, key))
        print("\n")
