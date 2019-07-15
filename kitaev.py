import numpy as np


def kitaev(phi_true, m):

    rho = estimate(np.arange(m), m, phi_true)
    out = np.zeros(m)

    for i in np.arange(m):
        out[i] = infer(rho, i+1)[1]

    return out


def infer(rho, m):

    rho = rho[:m]
    octant = 0.125 * np.arange(8)
    distance = np.abs(octant - rho[-1])
    beta_m = int(8 * octant[np.argmin(distance)])
    alpha = bin(beta_m)[2:].zfill(3)

    for k in range(m - 1):

        test = length((int('0' + alpha[:2], 2) / 8 - rho[-k - 2]) % 1)
        if test < 0.25:
            alpha = '0' + alpha
        else:
            # print(length((int('1' + alpha[:2], 2) / 8 - rho[-k - 2]) % 1))
            alpha = '1' + alpha

    return alpha, int(alpha, 2) / 2 ** (m + 2)


def estimate(i, m, phi_true):

    s = np.ceil(np.log2(m))

    # simulate quantum outputs

    # perform s measurements for cos
    p = (1-np.cos(2*np.pi*2**i*phi_true))/2
    cos_est = 1-2*np.random.binomial(s, p)/s

    # perform s measurements for sin
    p = (1-np.sin(2*np.pi*2**i*phi_true))/2
    sin_est = 1-2*np.random.binomial(s, p)/m

    out = 0.5*np.arctan2(sin_est, cos_est)/np.pi % 1

    return out


def length(x):

    assert x == x%1
    return min(x, 1-x)
