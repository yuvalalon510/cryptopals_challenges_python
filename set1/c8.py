import c7 as AES

if __name__ == "__main__":
    
    key = b"YELLOW SUBMARINE"

    with open("8.txt", "r") as f:
        ciphertexts = f.readlines()
    
    for cipher in ciphertexts:
        encoded_cipher = bytes.fromhex(cipher)

        # AES in ECB mode is deterministic. it always produces the same cipher for the same 128-bit block and key.
        # Check for repetitions by counting all distinct blocks.
        blocks = {encoded_cipher[i:i+16] for i  in range(0, len(encoded_cipher), 16)}
        if len(blocks) < len(encoded_cipher)//16:
            print(cipher)
        