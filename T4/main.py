import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys

from floodfill import rotula

#===============================================================================

INPUT_IMAGE =  '205.bmp'

#===============================================================================

def main():
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.')
        sys.exit ()
    #Ruido
    img = cv2.GaussianBlur(img, (3,3),0)
    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    #img = img.reshape ((img.shape [0], img.shape [1], 1))
    #img = img.astype (np.float32) / 255
    
    #bin_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 7)
    
    bin_img = cv2.Sobel(img, cv2.CV_16S,1,1)
    print(bin_img[:3][:3])
    print(img[:3][:3][0])
    exit()
    componenents = rotula(bin_img)
    n_componentes = len (componentes)
    print(n_componentes)
    for c in componentes:
        cv2.rectangle (bin_img, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow('out ', bin_img)
    cv2.imwrite ('out.png', bin_img)
    cv2.waitKey (1000)
    cv2.destroyAllWindows ()


if __name__ == "__main__":
    main()

