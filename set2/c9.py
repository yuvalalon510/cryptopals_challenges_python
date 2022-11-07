# AES 16 byte padding

blocksize = 16

def pad(data):
    padding = blocksize - len(data) % blocksize
    return data + bytes(padding for i in range(padding))

def unpad(text):
    padding_length = text[-1]
    return text[:-padding_length]

if __name__ == "__main__":
    assert(unpad(pad(b"a"*16)) == b"a"*16)