class TwisterRNG():
    w, n, m, r = 32, 624, 397, 31
    a = 0x9908B0DF
    u, d = 11, 0xFFFFFFFF
    s, b = 7, 0x9D2C5680
    t, c = 15, 0xEFC60000
    l = 18
    f = 1812433253
    lowermask = (1 << r) - 1
    uppermask = (~ lowermask) & ~(-1 << w)


    def __init__(self):
        self.MT = [0 for i in range(self.n)]
        self.index = self.n + 1

    def seed(self, seed):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            temp = self.MT[i-1] ^ (self.MT[i-1] >> (self.w - 2))
            temp = self.f * temp + i
            self.MT[i] = temp & ~(-1 << self.w)
    
    def random(self):
        if self.index >= self.n:
            if self.index > self.n:
                raise("Generator was never seeded")
            self.twist()

        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)

        self.index += 1
        return y & ~(1 << self.w)

    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.uppermask) + (self.MT[(i+1) % self.n] & self.lowermask)
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA

        self.index = 0

if __name__ == "__main__":
    gen = TwisterRNG()
    gen.seed(0)
    for i in range(10):
        print(gen.random())