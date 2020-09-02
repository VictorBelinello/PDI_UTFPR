import matplotlib.pyplot as plt
import numpy as np
import cv2

def inunda(label, rotulado, x0, y0, componente):
    if(rotulado[y0][x0] == -1 ): # nao foi rotulado e nao eh pixel preto
        # atribui label para o pixel
        rotulado[y0][x0] = label

        componente["label"] = label
        componente["n_pixels"] = componente["n_pixels"] + 1 if "n_pixels" in componente else 1
        componente["T"] = y0 if ( not ("T" in componente) or y0 < componente['T']) else componente['T']
        componente["L"] = x0 if ( not ("L" in componente) or x0 < componente['L']) else componente['L']
        componente["B"] = y0 if ( not ("B" in componente) or y0 > componente['B']) else componente['B']
        componente["R"] = x0 if ( not ("R" in componente) or x0 > componente['R']) else componente['R']
        

        if x0 - 1 >= 0 and rotulado[y0][x0 - 1] == -1:
            inunda(label, rotulado, x0 - 1, y0, componente)

        if x0 + 1 < rotulado.shape[1] and rotulado[y0][x0 + 1] == -1:
            inunda(label, rotulado, x0 + 1, y0, componente)

        if y0 - 1 >= 0 and rotulado[y0 - 1][x0] == -1:
            inunda(label, rotulado, x0, y0 - 1, componente)

        if y0 + 1 < rotulado.shape[0] and rotulado[y0 + 1][x0] == -1: 
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

def rotula (img):
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
            #if componenteValido(componente_atual, largura_min, altura_min, n_pixels_min):
            componentes.append(componente_atual)
            label += 0.1
            componente_atual = { }

    return componentes