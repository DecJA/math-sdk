from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


def get_gauss(n=10000, mu=2.0, sigma=4, offset=1.0):
    v = []
    for _ in range(n):
        v.append(min(abs(np.random.lognormal(mu, sigma)), 5000))

    plt.hist(v, 200)
    plt.show()


if __name__ == "__main__":

    get_gauss()
