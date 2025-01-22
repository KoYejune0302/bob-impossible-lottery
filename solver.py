#!/usr/bin/env python3

import operator
import math
import struct

class Math:
    state0, state1 = 18334895118323930352, 508147093636674015 # Start with random seed
    @classmethod
    def random(cls):
        ret = (cls.state0 >> 12) + 0x3ff0_0000_0000_0000
        ret, = struct.unpack('d', struct.pack('Q', ret))
        cls.nextRand()
        return ret - 1

    @classmethod
    def nextRand(cls):
        s0 = cls.state1
        s1 = cls.state0
        cls.state0 = s0
        s1 ^= (s1 << 23) & 0xffff_ffff_ffff_ffff
        s1 ^= s1 >> 17
        s1 ^= s0
        s1 ^= s0 >> 26
        cls.state1 = s1


class VMath:
    cache = []
    @classmethod
    def random(cls):
        try:
            return cls.cache.pop()
        except IndexError:
            cls.cache = [Math.random() for _ in range(64)]
            return cls.cache.pop()

NUMBERS = list(map(int, range(1, 46)))

genNonce = lambda: [NUMBERS[int(VMath.random() * 45)] for _ in range(16)]
genNonceR = lambda: [NUMBERS[int(Math.random() * 45)] for _ in range(16)]

class BitVec(list):
    def __lshift__(self, sh):
        return BitVec([0] * sh + self[:-sh])

    def __rshift__(self, sh):
        return BitVec(self[sh:] + [0] * sh)

    def __xor__(self, sh):
        return BitVec(map(operator.xor, self, sh))


def seed_from_sequence(nonce):
    xorshift0 = BitVec([2 ** i for i in range(0, 64)])
    xorshift1 = BitVec([2 ** i for i in range(64, 128)])

    paralela = []

    for x in nonce:
        try:
            v = NUMBERS.index(x)
        except ValueError:
            pass
        else:
            vmin = (2 ** 52) * v // 45
            vmax = (2 ** 52) * (v + 1) // 45 - 1

            vnow = vmax
            while vnow and vnow >= vmin:
                vmin2 = vnow
                vnow -= vnow & -vnow
            vnow = vmin
            while vnow <= vmax:
                vmax2 = vnow
                vnow += ~vnow & -~vnow
            vmin2 &= vmin & vmax
            vmax2 |= vmin | vmax
            suremask = ~(vmin2 ^ vmax2)

            for i in range(51, -1, -1):
                if vmin2 & (2**i) == vmax2 & (2**i):
                    paralela.append((xorshift0[12 + i] << 1) | bool(vmin2 & (2**i)))

        x0 = xorshift1
        x1 = xorshift0
        xorshift0 = x0
        x1 ^= x1 << 23
        x1 ^= x1 >> 17
        x1 ^= x0
        x1 ^= x0 >> 26
        xorshift1 = x1
    for _ in range(2):
        for i, x in enumerate(paralela):
            if x < 1:
                continue
            j = int(math.log2(x))
            for k, y in enumerate(paralela):
                if k != i and y & (2**j):
                    paralela[k] ^= x

    print(sorted(set(paralela))[:2])
    st0ok = st1ok = None
    if 1 in paralela:
        print(nonce, 'unsatisfiable')
    else:
        st0ok = st1ok = 0
        have = set()
        for x in paralela:
            if x < 2:
                continue

            j = int(math.log2(x))
            have.add(j)
            if x & 1:
                if j <= 64:
                    st0ok |= 2 ** (j - 1)
                else:
                    st1ok |= 2 ** (j - 65)
        missing = set(range(1, max(have))) - have  
        print('missing =', missing)  

        print(bin(st0ok)[2:].zfill(64))
        print(bin(st1ok)[2:].zfill(64))

        Math.state0 = st0ok
        Math.state1 = st1ok

        print(genNonceR())
        print(nonce, '(orig)')
        print("----------------------------------------------------------------")

    return st0ok, st1ok

while True:
    st0ok = None
    while st0ok is None:
        print("plz enter nonces : ")
        nonce0 = list(map(int, input().split()))
        nonce1 = list(map(int, input().split()))
        nonce2 = list(map(int, input().split()))

        print(nonce0, nonce1, nonce2)

        for nonce in (nonce2[::-1] + nonce1[::-1] + nonce0[::-1],
                      nonce0[::-1] + ['?'] * 80 + nonce2[::-1] + nonce1[::-1],
                      nonce1[::-1] + nonce0[::-1] + ['?'] * 80 + nonce2[::-1]):
            print("nonce : ", nonce)
            st0ok, st1ok = seed_from_sequence(nonce)
            if st0ok is not None:
                break

    Math.state0 = st0ok
    Math.state1 = st1ok

    for i in range(8):  
        print(genNonceR()[::-1])

    nowy_nonce_na_pewno = genNonceR()[::-1]

    print("----------------------------------------------------------------")
    print(nowy_nonce_na_pewno)