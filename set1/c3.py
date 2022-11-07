frequencies = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}

letter_score = lambda c: frequencies[c] if c in frequencies else 0

score_text = lambda text: sum(letter_score(c.lower()) for c in text)

def xor_single_byte(C, k):
    # if C is a hex str convert it to bytes.
    if type(C) is str:
        C = bytes.fromhex(C)

    P = bytes(c ^ k for c in C)
    return P

def decrypt(cipher):
    max_score, result, bestkey = 0, None, None

    # for every possible key
    for k in range(128):

        # produce text from the cipher and the key
        P = xor_single_byte(cipher, k)
        if not all(c < 128 for c in P):
            continue

        # save the highest english scored text
        plaintext = P.decode("utf-8")
        score = score_text(plaintext)
        if score > max_score:
            max_score = score
            result = plaintext
            bestkey = k
    
    return result, max_score, bestkey

if __name__ == "__main__":
    print(decrypt("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")[0])