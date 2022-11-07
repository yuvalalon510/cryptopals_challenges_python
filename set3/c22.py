from c21 import TwisterRNG
import time
import random


def gettime():
    return int(time.time())

simulated_time = gettime()

def generate():
    oracle = TwisterRNG()
    startTime = gettime()
    seedTime = startTime + random.randint(40, 1000)
    oracle.seed(seedTime)
    global simulated_time
    simulated_time = seedTime + random.randint(40, 1000)
    return oracle.random()

if __name__== "__main__":
    output = generate()
    currentTime = simulated_time
    rng = TwisterRNG()
    for s in range(currentTime - 2000, currentTime):
        rng.seed(s)
        if rng.random() == output:
            print("seed is", s)
            break;


