from c21 import TwisterRNG

get_bit = lambda x, i: (x >> (31 - i)) & 1 if 0 <= i and i <= 31 else 0 
set_bit = lambda x, i: x | (1 << (31 - i))

def undo_shr_xor(x, shiftLen):
    """ Undo x = x ^ (x >> shiftLen) """

    y = 0
    for i in range(32):
        bit = get_bit(x,i) ^ get_bit(y, i-shiftLen)
        if bit:
            y = set_bit(y, i)
    return y

def undo_shl_xor_and(x, shiftLen, mask):
    """ Undo x = x ^ ((x << shiftLen) & mask) """

    y = 0
    for i in range(32):
        bit = get_bit(x, 31 - i) ^ (get_bit(y, 31 - i + shiftLen) & \
              get_bit(mask, 31 - i))
        if bit:
            y = set_bit(y, 31 - i)
    return y

def untemper(y):
    """ Untemper the number returned by a generator, to get the internal state """
    y = undo_shr_xor(y, TwisterRNG.l)
    y = undo_shl_xor_and(y, TwisterRNG.t, TwisterRNG.c)
    y = undo_shl_xor_and(y, TwisterRNG.s, TwisterRNG.b)
    y = undo_shr_xor(y, TwisterRNG.u)
    return y

def clone_rng(rng: TwisterRNG):
    """ Get the internal state and clone the generator """

    MT = []

    for i in range(TwisterRNG.n):
        MT.append(untemper(rng.random()))

    cloned = TwisterRNG()
    cloned.seed(0)
    cloned.MT = MT
    return cloned

if __name__ == "__main__":
    rng = TwisterRNG()
    rng.seed(100)
    rng2 = clone_rng(rng)
    for i in range(1000):
        assert(rng.random() == rng2.random())
    
    



   