import struct
import hashlib

"""rotate a 32-bit int"""
def leftrotate(w, c):
    return ((w << c) & 0xFFFFFFFF) | (w >> (32 - c))

"""SHA-1 implementation using the pseudocode from wikipedia"""
def sha1(message: bytes, h0 = 0x67452301, h1 = 0xEFCDAB89,  h2 = 0x98BADCFE, h3 = 0x10325476, h4 = 0xC3D2E1F0, ml=None):

    if ml == None:
        ml = len(message) * 8

    message += bytes([0x80])
    while (8 * len(message)) % 512 != 448:
        message += bytes([0x00])
    message += struct.pack(">Q", ml)

    for chunk_offset in range(0, len(message), 64):
        
        w = [0] * 80
        for i in range(16):
            w[i] = struct.unpack(">I", message[chunk_offset + 4*i:chunk_offset + 4*(i+1)])[0]
        
        for i in range(16, 80):
            w[i] = leftrotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)
        
        a, b, c, d, e = h0, h1, h2, h3, h4

        for i in range(80):
            if i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif i <= 59:
                f = (b & c) | (b & d) | (c & d) 
                k = 0x8F1BBCDC
            elif i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (leftrotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
            e = d
            d = c
            c = leftrotate(b, 30)
            b = a
            a = temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

def sha1_mac(message: bytes, key: bytes):
    return sha1(key + message)

def run():
    h1 = sha1(b"")
    h2 = hashlib.sha1(b"")

    assert(h1 == h2.hexdigest())

    h1 = sha1(b"The quick brown fox jumps over the lazy dog")
    print(h1)
    h2 = hashlib.sha1(b"The quick brown fox jumps over the lazy dog")

    assert(h1 == h2.hexdigest())

    h1 = sha1(b"Secret Message!")
    h2 = hashlib.sha1(b"Secret Message!")

    assert(h1 == h2.hexdigest())

if __name__ == "__main__":
    run()
