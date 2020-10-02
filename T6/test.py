import numpy as np
import time
import matplotlib.pyplot as plt

from fft import cooley_tukey_1d
from dft import dft

def fft1d_test(n):
    print(f"Testing FFT for n = {n}")
    x = np.random.randint(100,size=(n))
    start = time.time()
    res1 = cooley_tukey_1d(x)
    end = time.time() - start
    print(f"My FFT Time: {end}, ",end=' ')

    start = time.time()
    res2 = np.fft.fft(x)
    end = time.time() - start
    print(f"Numpy time: {end}")

    close = np.allclose(res1, res2)
    if not close:
        print("Wrong answer")
    else:
        print("OK")

def dft1d_test(n):
    print(f"Testing DFT for n = {n}")
    x = np.random.randint(100,size=(n))
    start = time.time()
    res1 = dft(x)
    end = time.time() - start
    print(f"My DFT Time: {end}, ",end=' ')

    start = time.time()
    res2 = np.fft.fft(x)
    end = time.time() - start
    print(f"Numpy time: {end}")

    close = np.allclose(res1, res2)
    if not close:
        print("Wrong answer")
    else:
        print("OK")

def compare(n):
    print(f"Comparing DFT and FFT for n = {n}")
    x = np.random.randint(100,size=(n))
    start = time.time()
    res1 = dft(x)
    end = time.time() - start
    print(f"My DFT Time: {end}, ",end=' ')

    start = time.time()
    res2 = cooley_tukey_1d(x)
    end = time.time() - start
    print(f"My FFT Time: {end}, ",end=' ')

    start = time.time()
    res_np = np.fft.fft(x)
    end = time.time() - start
    print(f"Numpy time: {end}")

    close = np.allclose(res1, res_np) and np.allclose(res2, res_np)
    if not close:
        print("Wrong answer")
    else:
        print("OK")

def timeit(func, arg):
    start = time.time_ns()        
    func(arg)
    return time.time_ns() - start

def plot_comparison():
    sizes = [i**2 for i in range(1,11)]
    np_times = []
    dft_times = []
    fft_times = []

    for n in sizes:
        x = np.random.randint(100,size=(n))
        np_time = timeit(np.fft.fft, x)
        dft_time = timeit(dft, x)
        fft_time = timeit(cooley_tukey_1d, x)
        np_times.append(np_time)
        dft_times.append(dft_time)
        fft_times.append(fft_time)

    plt.plot(sizes, np_times)
    plt.plot(sizes, dft_times)
    plt.plot(sizes, fft_times)
    plt.legend( ['Numpy', 'DFT', 'FFT'] )
    plt.xlabel("Size of input")
    plt.ylabel("Run time (ns)")
    plt.show()

if __name__ == "__main__":
    plot_comparison()