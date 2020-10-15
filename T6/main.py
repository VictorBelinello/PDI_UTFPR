import numpy as np
import matplotlib.pyplot as plt
import cv2
from fft import cooley_tukey_2d, ifft_2d
from math import floor, ceil
from util import *

def blur(image):
  # Lembrando que ksize maior borra menos, por isso nao usa o mesmo 
  ksize = 120
  # Variaveis para fazer padding to kernel para usar np.multiply
  pad_top = floor((image.shape[0] - ksize)/2)
  pad_bottom = ceil((image.shape[0] - ksize)/2)
  pad_left = floor((image.shape[1] - ksize)/2)
  pad_right = ceil((image.shape[1] - ksize)/2)

  # Pega o kernel gaussiano e realiza padding necessario
  gaussian_kernel = getGaussianKernel(ksize)
  gaussian_kernel = np.pad(gaussian_kernel, ((pad_top, pad_bottom), (pad_left, pad_right)), 'constant', constant_values=(0,0) )

  # FFT 2D da imagem
  fft = cooley_tukey_2d(image)
  #fft = np.fft.fft2(image)
  
  # Shifta componente DC para centro da imagem
  fft_shift = np.fft.fftshift(fft)
  
  # Pega magnitudes
  fft_abs = np.abs(fft_shift)
  
  # Aplica filtro ponto a ponto
  filtered = np.multiply(fft_shift, gaussian_kernel)

  # Reconstroi imagem
  img_back = ifft_2d(np.fft.ifftshift(filtered))
  img_back = np.real(img_back)
  img_back = img_back/np.max(img_back)
  
  return img_back
    


def main():
  # Carrega imagem
  img = cv2.imread ('small.jpg', cv2.IMREAD_GRAYSCALE)
  if img is None:
      print ('Erro abrindo a imagem.\n')
      exit()
  # Realiza o padding para que o tamanho seja uma potencia de 2
  image = padImage(img)
  # Borra imagem usando a fft
  fft_blur = blur(image)
  cv2.imshow ('fft_blur', fft_blur)
  cv2.waitKey ()

  ksize = 31
  # Borra usando opencv
  opencv_blur = cv2.GaussianBlur(image, (ksize, ksize), 0)
  cv2.imshow ('opencv_blur', opencv_blur)
  cv2.waitKey ()
  cv2.destroyAllWindows ()

if __name__ == "__main__":  
  main()
    