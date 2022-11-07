import c10
import c9 as padding
import random

debug = 1

def encryption_orcale(data):
    # Pad a random amount of bytes to data
    padLeft = bytes(random.randint(0, 0xFF) for i in range(random.randint(5, 10)))
    padRight = bytes(random.randint(0, 0xFF) for i in range(random.randint(5, 10)))
    padded_data = padding.pad(padLeft + data + padRight)
    
    # Encrypt with a random key, algorithm (and iv)
    key = bytes(random.randint(0, 0xFF) for i in range(16))
    rand = random.random()

    if rand < 0.5:
        if debug:
            print("Encrypting in ECB Mode")
        cipher = c10.AES_Encrypt_ECB(padded_data, key)
    else:
        if debug:
            print("Encrypting in CBC Mode")
        iv = bytes(random.randint(0, 0xFF) for i in range(16))
        cipher = c10.AES_Encrypt_CBC(padded_data, key, iv)
    
    return cipher

def detection_oracle():
    # Choose an input with enough repeated 16-bye blocks
    function_input = bytes(65 for i in range(64))
    cipher = encryption_orcale(function_input)

    # Detect repetitions in cipher
    blocks = {cipher[i:i+16] for i in range(0, len(cipher), 16)}
    if len(blocks) < len(cipher)//16:
        print("Detected ECB")
    else:
        print("Detected CBC")

if __name__ == "__main__":
    for i in range(10):
        detection_oracle()
        print()


