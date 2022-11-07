from time import time
from binascii import hexlify
import requests

delay = 0.005
samples = 10

def break_hmac():
    signature_bytes = bytearray(b'\x00'*20)
    for i in range(20):
        max_median, arg_max = 0, 0
        # for each possible byte, send a number of requests and select the median response time
        # choose the next byte with the maximum median response time
        for v in range(256):
            signature_bytes[i] = v
            signature = hexlify(signature_bytes).decode()
            request = "http://localhost:8080/test?file=foo&signature=" + signature
            elapsed_times = []
            for j in range(samples):
                response = requests.get(request)
                elapsed_times.append(response.elapsed.total_seconds())
            elapsed_times.sort()
            median = elapsed_times[samples//2]
            max_median, arg_max = (median, v) if median > max_median else (max_median, arg_max)
        signature_bytes[i] = arg_max
        print("Iteration", i+1, hexlify(signature_bytes).decode())
    print("Correct signature: ", hexlify(signature_bytes).decode()) 


if __name__ == "__main__":
    url = "http://localhost:8080/test?file=foo&signature=0687cbf21cf68bc3806d556aa6c1a754c564fcfb"
    break_hmac()