import numpy as np

def cooley_tukey_1d(x):
    N = len(x)
    half = int(N/2)
    if N <= 1:
        return x

    x_even = cooley_tuley_1d( x[0:N:2] )
    x_odd = cooley_tuley_1d( x[1:N:2] )

    temp = [0]*N
    #temp = np.empty(N, dtype=np.complex)

    # Eh possivel calcular o ponto k e k+half da fft ao mesmo tempo
    # Apenas trocando o sinal na conta
    # Assim so precisamos percorrer metade do vetor final
    for k in range(half):
        w = np.exp(-2*np.pi*1j*k/N)
        temp[k] = x_even[k] + x_odd[k] * w
        temp[k + half] = x_even[k] - x_odd[k] * w

    return temp