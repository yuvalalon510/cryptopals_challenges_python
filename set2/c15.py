# PKCS7 padding with validation

def pad_pkcs7(data: bytes):
    padding = 16 - len(data) % 16
    return data + bytes(padding for i in range(padding))

def unpad_pkcs7(string: bytes):
    count = -1
    length = 0
    if len(string) % 16 == 0 and 0 < string[-1] and string[-1] <= 16:
        length = string[-1]
        count = string[-length:].count(length)
    
    if count != length:
        raise ValueError("Incorrect padding")

    return string[:-count]

if __name__ == "__main__":
    assert(unpad_pkcs7(b"ICE ICE BABY\x04\x04\x04\x04") == b"ICE ICE BABY")
    assert(unpad_pkcs7(b"A"*16 + b"\x10"*16) == b"A"*16)
    # Should throw error
    unpad_pkcs7(b"ICE ICE BABY\x05\x05\x05\x05\x05")
