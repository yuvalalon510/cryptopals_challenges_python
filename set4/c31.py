from time import time
from binascii import hexlify
import requests

delay = 0.05

def break_hmac():
    signature_bytes = bytearray(b'\x00'*20)
    for i in range(20):
        max_elapsed = 0
        best = 0
        for v in range(256):
            signature_bytes[i] = v
            signature = hexlify(signature_bytes).decode()
            request = "http://localhost:8080/test?file=foo&signature=" + signature
            start_time = time()
            requests.get(request)
            end_time = time()
            elapsed = end_time - start_time
            # the signature with the max elapsed time is the most likely,
            # because it has the most bytes that are correct
            if elapsed > max_elapsed:
                max_elapsed = elapsed
                best = v
        signature[i] = best
        print("Completed", i+1, "iterations. Signature:", signature)
    print("Correct signature: ", hexlify(signature_bytes).decode()) 


if __name__ == "__main__":
    url = "http://localhost:8080/test?file=foo&signature=0687cbf21cf68bc3806d556aa6c1a754c564fcfb"
    break_hmac()