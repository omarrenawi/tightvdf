from src.protocol.utils import *

import hashlib

s = 2  # statistical security parameter


def setup(s):
    """

    input: s: statistical security parameter
    output: N
    """
    return gen_N(2 * s)  # can be change


def gen(N):
    """

    :param N: Modulus N
    :return: x in QR+_{N}
    """
    return generate_rand_residue(N)


def comp(N, x, T):
    """
     solution of the RSW time-lock puzzle (but over (QR+_{N}, ◦) not (Z∗_{N}, ·))
    :param N: Modulus
    :param x: random integer in QRN+_{N}
    :param T:
    :return: x**(2**T) in QR+_{N}
    """
    print("Solving ...")
    res = pow(pow(x, 2, N), T, N)
    res= abs(res)
    print("done")
    return res


def prov(N, x, T, y):



    print("Proving ...")

    # for the Fiat Shamir heuristic we will use sha256
    h = hashlib.sha256()
    t = int(math.log(T, 2))
    assert (2 **t) == T and assert_mem(y, N)

    xn, yn = x, y

    pi=[]

    for i in range(t):

        pwr = abs (pow(2, T // (2 ** (i+1)), N))
        tmp = abs (pow(xn, pwr, N))

        if not assert_mem(tmp, N):
            print(1)
            return reject()

        pi.append(tmp)
        tmp = "{}{}{}{}".format(xn, div(T, 2**(i)), yn, pi[i])
        h.update(tmp.encode())
        dig = h.hexdigest()
        h = hashlib.sha256()
        r = int(dig, 16)# % (2 ** s)
        xn = mul(pow(xn, r, N), pi[i], N)
        yn = mul(pow(pi[i], r, N), yn, N)

    print("done")

    return pi


def verify(N, x, T, y, pi):

    print("Verifying ... ")

    if not assert_mem(x, N):
        print("{} is not member in {}".format(x, N))
        return reject()

    if not assert_mem(y, N):
        print("{} is not member in {}".format(y, N))
        print("y= %d, N=%d " %(y, N))
        return reject()

    for i in pi:
        if not assert_mem(i, N):
            print("i = {} is not a member in {}".format(i, N))
            return reject()

    xn, yn = x, y

    t = int(math.log(T, 2))

    for i in range(t):
        tmp = "{}{}{}{}".format(xn, div(T, 2**(i+1)), yn, pi[i])
        h = hashlib.sha256()
        h.update(tmp.encode())
        hs = h.hexdigest()
        r = int(hs, 16) % (2 ** s)
        xn = mul(pow(xn, r, N), pi[i], N)
        yn = mul(pow(pi[i], r, N), yn, N)

    if yn == (xn ** 2) % N:  # mod?
        return accept()

    print("verification failed!\n{} != {}".format(yn, (xn**2 ) % N))
    return reject()
