from math import ceil, log2, floor
import cv2
import numpy as np

def showFFTMag(fft):
  fft_abs = np.abs(fft)
  
  magnitude = np.log10(fft_abs)
  magnitude = magnitude/np.max(magnitude)

  cv2.imshow ('magnitude', magnitude)
  cv2.waitKey ()

def getGaussianKernel(ksize):
  #https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html#gac05a120c1ae92a6060dd0db190a61afa
  sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8
  sigma_2 = sigma**2
  half = int(ksize/2)

  kernel = np.empty(shape=(ksize, ksize))
  for i in range(ksize):
    y = i - half
    gy = np.exp(-y**2/sigma_2)
    for j in range(ksize):
      x = j - half
      gx = np.exp(-x**2/sigma_2)
      kernel[i, j] = gx*gy
  return kernel
    
def padImage(img):

  next_row = pow(2, ceil(log2(img.shape[0])))
  top = ceil((next_row - img.shape[0])/2)
  bottom = floor((next_row - img.shape[0])/2)

  next_col = pow(2, ceil(log2(img.shape[1])))
  left = ceil((next_col - img.shape[1])/2)
  right = floor((next_col - img.shape[1])/2)

  image = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT)
  return image