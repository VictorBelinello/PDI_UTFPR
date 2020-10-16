import numpy as np

def roll_rows(x, amnt):
  h = x.shape[0]
  amnt = amnt%h
  a = np.copy(x)
  for i in range(amnt):
    a = np.concatenate((a[-1:], a[:-1]))
  return a

def roll_cols(x, amnt):
  c = x.shape[1]
  amnt = amnt%c
  a = np.copy(x)
  for i in range(amnt):
    for idx, row in enumerate(a):
      a[idx] = np.concatenate((row[-1:],row[:-1]))
  return a

def shift(x):
  height = x.shape[0]//2 
  width = x.shape[1]//2 
  a = roll_rows(x, height)
  a = roll_cols(a, width)
  return a
  

def ifft_2d(x):
  # Troca real e imaginario
  for i in range(x.shape[0]):
    for j in range(x.shape[1]):
      real = np.imag(x[i,j])
      imag = np.real(x[i,j])
      x[i,j] = np.complex(real, imag)
  # Faz a FFT
  res = cooley_tukey_2d(x)/(x.shape[0]*x.shape[1])
  # Troca novamente real e imaginario
  for i in range(res.shape[0]):
    for j in range(res.shape[1]):
      real = np.imag(res[i,j])
      imag = np.real(res[i,j])
      res[i,j] = np.complex(real, imag)
  return res
  
def cooley_tukey_2d(x):
  _fft = np.empty(shape=x.shape, dtype=np.complex)
  
  # Faz a fft em cada linha
  for row in range(x.shape[0]):
    _fft[row] = cooley_tukey_1d(x[row])
  # Faz a fft de cada coluna resultante
  for col in range(x.shape[1]):
    _fft[:,col] = cooley_tukey_1d(_fft[:,col])
  
  return _fft



def cooley_tukey_1d(x):
  N = len(x)
  half = int(N/2)
  if N <= 1:
      return x

  x_even = cooley_tukey_1d( x[0:N:2] )
  x_odd = cooley_tukey_1d( x[1:N:2] )

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

def test():
  n = 3
  x = np.empty(shape=(n,n))
  for i in range(n):
    x[i] = np.random.randint(100,size=(n))
  r = shift(x)
  #print(r)


if __name__ == "__main__":
    test()