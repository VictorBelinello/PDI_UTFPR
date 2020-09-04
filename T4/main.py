import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
from math import ceil
from flood import rotula

#===============================================================================

INPUT_IMAGE =  '205.bmp'

#===============================================================================

def conta_arroz(img, img_out):
    # Primeira tentativa de rotular 
    componentes = rotula(img)
    total_arroz = len (componentes)
    componentes_copia = componentes.copy()
    print("Original: ", total_arroz)
    
    # Para visualizar como foi a primeira rotulagem
    rotulagem_inicial = img_out.copy()
    for c in componentes:
        cv2.rectangle (rotulagem_inicial, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,255))
    cv2.imwrite("rotulagem_inicial.png", rotulagem_inicial)

    NUM_DESVIOS = 2 # Quantos desvios-padrao utilizar
    coef_variacao_antigo = -1
    
    while True:
        # Obtem estatisticas dos tamanhos dos componentes rotulados
        # Cria uma lista com os tamanhos dos componentes
        tamanhos = [x["n_pixels"] for x in componentes] 
        media = np.average(tamanhos)
        desvio = np.std(tamanhos)
        # Calcula coeficiente de variacao
        coef_variacao = desvio / media
        
        if coef_variacao < 0.2 or coef_variacao_antigo == (desvio / media):
            break

        for c in componentes:
            tam = c["n_pixels"]
            # Verifica componentes "anormais" e remove
            if tam > (media + NUM_DESVIOS*desvio):
                cv2.rectangle (rotulagem_inicial, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,255,0))
                componentes.remove(c)
            elif tam < (media - NUM_DESVIOS*desvio):
                cv2.rectangle (rotulagem_inicial, (c ['L'], c ['T']), (c ['R'], c ['B']), (255,0,0))
                componentes.remove(c)
        coef_variacao_antigo = coef_variacao
        
    # Agora tem uma media melhor, repete o processo usando os componentes iniciais
    grandes = 0
    pequenos = 0
    for c in componentes_copia:
        tam = c["n_pixels"]
        if tam > (media + NUM_DESVIOS*desvio):
            # Um blob com 'quant_dentro' arroz foi considerado um unico arroz, corrige isso
            quant_dentro = round(tam / media)
           # print(quant_dentro, tam //media )
            total_arroz += quant_dentro - 1 
            grandes += 1
            cv2.rectangle (rotulagem_inicial, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,255,255))
        elif tam < media * 0.1:
            # Ruido foi considerado arroz
            cv2.rectangle (rotulagem_inicial, (c ['L'], c ['T']), (c ['R'], c ['B']), (255,0,255))
            pequenos += 1
            total_arroz -= 1
    cv2.imwrite("rotulagem_final.png", rotulagem_inicial)
    print(f"Apos filtragem foram encontrados {grandes} componentes grandes e {pequenos} componentes pequenos")
    return total_arroz

def main():
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não.
    img = img.reshape ((img.shape [0], img.shape [1], 1))

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)
    
    # Remove ruido
    borrada = cv2.GaussianBlur(img, (15,15),0)
    # Binariza    
    binarizada = cv2.adaptiveThreshold(borrada, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 0)
    # Remove ruido novamente, usando morfologia
    kernel = np.ones((5, 5), np.uint8)
    binarizada = cv2.morphologyEx(binarizada,cv2.MORPH_OPEN , kernel )
    cv2.imwrite("binarizada.png", binarizada)

    # Fim do pré-processamento ######################################################################

    total_arroz = conta_arroz(binarizada, img_out)
       
    print(f"Total encontrado: {total_arroz}")
    #cv2.imshow('out ', img_out)
    #cv2.imwrite ('out.png', img_out)
    #cv2.waitKey (1000)
    cv2.destroyAllWindows ()


if __name__ == "__main__":
    #sys.setrecursionlimit(1600)
    main()
