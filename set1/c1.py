def encode_base64(hex_str):
    b64_str = []
    length = len(hex_str)
    for i in range(0, length, 6):
        if i + 6 > length:
            size = length % 6
        else:
            size = 6
        block = int(hex_str[i:i+size], 16)
        nbits = size * 4
        b64_str.extend(convert_buffer(block, nbits))
    return ''.join(b64_str)


def convert_buffer(block, nbits):
    res = []
    padding = 0
    nbytes = nbits // 8
    while nbits > 0:
        if nbits >= 6:
            digit = (block >> (nbits - 6))
            nbits -= 6
        else:
            padding = 3 - nbytes
            digit = (block << (6 - nbits)) & 63
            nbits = 0
        res.append(b64_digit(digit & 63))
    res.extend(['=' for i in range(padding)])    
    return res

def b64_digit(digit):
    if digit < 26:
        offset = ord('A')
        i = digit
    elif digit < 52:
        offset = ord('a')
        i = digit - 26
    elif digit < 62:
        offset = ord('0')
        i = digit - 52
    elif digit == 62:
        return '+'
    else:
        return '/'

    return chr(offset + i)

print(encode_base64("040404"))
print(encode_base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"))
print(encode_base64("abfabfab"))
print(encode_base64("abdcef0bcc"))
