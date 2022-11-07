import c3 as util

if __name__ == "__main__":
    with open("input", "r") as f:
        results = sorted([util.decrypt(cipher) for cipher in f.readlines()], key=lambda x: x[1], reverse=True)
        print(results[0][0])

