from c2 import xor

def xor_encryption(text, key):
    times = len(text) // len(key)
    residue = len(text) - len(key) * times
    key = key * times

    if residue > 0:
        key += key[:residue]
    
    return xor(text.encode().hex(), key.encode().hex())

def xor_decryption(text, key):
    hexstr = xor_encryption(text, key)
    return bytes.fromhex(hexstr).decode("utf-8")

if __name__ == "__main__":
    text = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    key = "ICE"
    result = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
    assert(xor_encryption(text,key) == result)