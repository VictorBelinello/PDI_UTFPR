import numpy as np

def idft(f):
  return dft(f, True)

def dft(f, inverse=False):
  if inverse:
    f_real = np.imag(f)
    f_imag = np.real(f)
  else:
    f_real = np.real(f)
    f_imag = np.imag(f)

  n = len(f)
  F = np.zeros(n, dtype=np.complex)

  for k in range(n):
      soma_real = 0
      soma_imag = 0
      for t in range(n):
        alfa = 2*np.pi * t * k/n
        soma_real += f_real[t] * np.cos(alfa) + f_imag[t] * np.sin(alfa)
        soma_imag += -f_real[t] * np.sin(alfa) + f_imag[t] * np.cos(alfa)
      if inverse:
        F[k] = np.complex(soma_imag, soma_real)
      else:
        F[k] = np.complex(soma_real, soma_imag)
  if inverse:
    return F/n
  return F
