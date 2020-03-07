#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.8
ALTURA_MIN = 10
LARGURA_MIN = 10
N_PIXELS_MIN = 400

#===============================================================================

def binariza (img, threshold):
    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''
    return np.where( img < threshold, 0.0, 1.0)

#-------------------------------------------------------------------------------


def inunda(label, rotulado, x0, y0, componente):
    if(rotulado[y0][x0][0] == -1 ): # nao foi rotulado e nao eh pixel preto
        # atribui label para o pixel
        rotulado[y0][x0][0] = label

        componente["label"] = label
        componente["n_pixels"] = componente["n_pixels"] + 1 if "n_pixels" in componente else 1
        componente["T"] = y0 if ( not ("T" in componente) or y0 < componente['T']) else componente['T']
        componente["L"] = x0 if ( not ("L" in componente) or x0 < componente['L']) else componente['L']
        componente["B"] = y0 if ( not ("B" in componente) or y0 > componente['B']) else componente['B']
        componente["R"] = x0 if ( not ("R" in componente) or x0 > componente['R']) else componente['R']
        

        if x0 - 1 >= 0 and rotulado[y0][x0 - 1][0] == -1:
            inunda(label, rotulado, x0 - 1, y0, componente)

        if x0 + 1 < rotulado.shape[1] and rotulado[y0][x0 + 1][0] == -1:
            inunda(label, rotulado, x0 + 1, y0, componente)

        if y0 - 1 >= 0 and rotulado[y0 - 1][x0][0] == -1:
            inunda(label, rotulado, x0, y0 - 1, componente)

        if y0 + 1 < rotulado.shape[0] and rotulado[y0 + 1][x0][0] == -1: 
            inunda(label, rotulado, x0, y0 + 1, componente)

def componenteValido(componente, largura_min, altura_min, n_pixels_min):
    if componente == {}:
        return False

    if componente["n_pixels"] < n_pixels_min:
        return False
    
    if (componente["B"] - componente["T"]) < altura_min:
        return False

    if (componente["R"] - componente["L"]) < largura_min:
        return False
        

    return True

def rotula (img, largura_min, altura_min, n_pixels_min):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''
    altura, largura = img.shape[:2]
    componentes = []
    label = 0.1
    img = np.where( img == 0, 0.0, -1.0)
    componente_atual = { }

    for y in range(altura):
        for x in range(largura):
            inunda(label, img, x,y, componente_atual)
            if componenteValido(componente_atual, largura_min, altura_min, n_pixels_min):
                componentes.append(componente_atual)
                label += 0.1
            componente_atual = { }

    return componentes
    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.

#===============================================================================

def main ():

    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)
    
    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza (img, THRESHOLD)
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey (1000)
    cv2.destroyAllWindows ()


if __name__ == '__main__':
    main ()

#===============================================================================
