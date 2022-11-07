import web
from hashlib import sha1
from time import sleep

delay = 0.05 #0.05 for Set 4 Challenge 31, 0.005 for Set 4 Challenge 32

sha1_hash = lambda m: sha1(m).digest()
#secret_key = bytes(randint(0, 0xFF) for i in range(4,17))
secret_key = b"SECRET"

#calculate HMAC-H with hash function H
#using the pseudocode from wikipedia
def hmac(key: bytes, message: bytes, H=sha1_hash, block_size=64, output_size=20):
    if len(key) > block_size:
        key = H(key)
    
    if len(key) < block_size:
        key += b'\x00' * (block_size - len(key)) 

    o_key_pad = bytes(x ^ y for (x,y) in zip(key, b'\x5c' * block_size))
    i_key_pad = bytes(x ^ y for (x,y) in zip(key, b'\x36' * block_size))

    return H(o_key_pad + H(i_key_pad + message))

#verify that the signature on the incoming request is valid for the requested file
def verify(request: dict):
    return insecure_compare(request["file"].encode(), request["signature"])

#compare the hmac of the message m with the signature.
#the comparison is done one byte at a time with a delay after each byte, with early exit
def insecure_compare(m, signature):
    h = hmac(secret_key, m)
    signature = bytes.fromhex(signature)

    for i in range(len(h)):
        if h[i] != signature[i]:
            return False
        sleep(delay)
    
    return True


urls = (
    '/test?', 'test'
)
app = web.application(urls, globals())

class test:
    def GET(self):
        data = web.input()
        if verify({"file": data.file, "signature": data.signature}):
            return "200 OK"
        else:
            return web.internalerror("500 Internal Error")


if __name__ == "__main__":
    app.run()
    app.stop()
