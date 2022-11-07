def xor(A, B):
    assert(len(A) == len(B))

    # if A is a hexadecimal encoded str (assume b is too) convert it to bytes.
    if type(A) is str:
        A, B = bytes.fromhex(A), bytes.fromhex(B)

    # xor every byte of C
    C = bytes(x ^ y for x,y in zip(A, B))   
    return C.hex()
    
if __name__ == "__main__":    
    print(xor("1c0111001f010100061a024b53535009181c", "686974207468652062756c6c277320657965"))