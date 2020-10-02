import numpy as np
import matplotlib.pyplot as plt
from dft import dft, idft
from fft import cooley_tukey_1d


def test(x, signal):
    signal_fft = np.fft.fft(signal)
    original = np.fft.ifft(signal_fft)
    plt.plot(x, np.real(original), 'o')

    signal_dft = dft(signal)
    original = idft(signal_dft)
    plt.plot(x, np.real(original), 'x')
    plt.show()

def main():
    num_samples = 2
    x = np.linspace(0, 2*np.pi, num_samples)
    freq = 1
    signal = np.sin(freq*x) 
    plt.plot(x, signal, 'b')
    plt.show()
    test(x, signal)



if __name__ == "__main__":  
    main()
    