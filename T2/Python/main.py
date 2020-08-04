import sys
import timeit
import numpy as np
import cv2

# ===============================================================================

INPUT_IMAGE = "flores.bmp"
ALTURA_JANELA = 21
LARGURA_JANELA = 21
COLOR = True if INPUT_IMAGE == "flores.bmp" else False
FILTRO = 2
# ===============================================================================
def mediaIngenuo(img, largura_janela, altura_janela):
    """Implementação do filtro da media utilizando o algoritmo 'ingenuo'.\\
       Não modifica imagem de entrada.
       Parametros: 
        img: Imagem de entrada 
        largura_janela: Largura da janela
        altura_janela: Altura da janela
       Retorno:
        img_saida: Imagem de saida, apos aplicar o filtro da media
    """
    altura, largura, num_canais = img.shape[:]
    # Variaveis auxiliares
    meia_altura_janela = altura_janela//2
    meia_largura_janela = largura_janela//2

    img_out = img.copy()

    # Percorrendo a imagem inteira, incluindo canais (ignorando as bordas)
    for k in range(0, num_canais):
        for y in range(meia_altura_janela, altura - meia_altura_janela):
            for x in range(meia_largura_janela, largura - meia_largura_janela):

                soma = 0.0
                # Percorrendo a janela relevante (centrada em y,x )
                # OBS: range(a,b) vai de a até b - 1
                for i in range(y - meia_altura_janela, y + meia_altura_janela + 1):
                    for j in range(x - meia_largura_janela, x + meia_largura_janela + 1):
                        soma += img[i][j][k]
                img_out[y][x][k] = soma / (largura_janela * altura_janela)
    return img_out

def mediaFiltroSeparavel(img, largura_janela, altura_janela):
    """Implementação do filtro da media utilizando filtro separável.\\
       Não modifica imagem de entrada.
       Parametros: 
        img: Imagem de entrada 
        largura_janela: Largura da janela
        altura_janela: Altura da janela
       Retorno:
        img_saida: Imagem de saida, apos aplicar o filtro da media
    """
    altura, largura, num_canais = img.shape[:]
    # Variaveis auxiliares
    meia_altura_janela = altura_janela//2
    meia_largura_janela = largura_janela//2

    buffer = img.copy()
    img_out = img.copy()

    # Aplicando filtro na horizontal
    for k in range(0, num_canais):
        for y in range(0, altura):
            for x in range(meia_largura_janela, largura - meia_largura_janela):
                soma = 0.0

                for j in range(x - meia_largura_janela, x + meia_largura_janela + 1):
                    soma += img[y][j][k]
                buffer[y][x][k] = soma / largura_janela 
    

    # Aplicando filtro na vertical
    for k in range(0, num_canais):
        for y in range(meia_altura_janela, altura - meia_altura_janela):
            for x in range(meia_largura_janela, largura - meia_largura_janela):
                soma = 0.0

                for i in range(y - meia_altura_janela, y + meia_altura_janela + 1):
                    soma += buffer[i][x][k]
                img_out[y][x][k] = soma / altura_janela
    return img_out

def obterImagemIntegral(img):
    altura, largura, num_canais = img.shape[:]
    img_out = np.empty(img.shape)
    for k in range(num_canais):
        for i in range(altura):
            img_out[i][0][k] = img[i][0][k]
            for j in range(1, largura):
                img_out[i][j][k] = img[i][j][k] + img_out[i][j - 1][k]
        for i in range(1,  altura):
            for j in range(largura):
                img_out[i][j][k] += img_out[i - 1][j][k]
    return img_out

def mediaImagensIntegrais(img, largura_janela, altura_janela):
    """Implementação do filtro da media utilizando imagens integrais.\\
       Não modifica imagem de entrada.
       Parametros: 
        img: Imagem de entrada 
        largura_janela: Largura da janela
        altura_janela: Altura da janela
       Retorno:
        img_saida: Imagem de saida, apos aplicar o filtro da media
    """
    altura, largura, num_canais = img.shape[:]
    # Variaveis auxiliares
    meia_altura_janela = altura_janela//2
    meia_largura_janela = largura_janela//2

    img_out = img.copy()

    img_integral = obterImagemIntegral(img)

    # Percorrendo a imagem inteira, incluindo canais (ignorando as bordas)
    for k in range(0, num_canais):
        for y in range(meia_altura_janela, altura - meia_altura_janela):
            for x in range(meia_largura_janela  , largura - meia_largura_janela):
                soma = 0.0
                # soma = g(r,b) - g(r,t) - g(l,b) + g(l,t)
                r = x + meia_largura_janela
                l = x - meia_largura_janela - 1
                t = y - meia_altura_janela  - 1
                b = y + meia_altura_janela
                # soma = g[b,r] - g[t,r] - g[b,l] + g[t,l]
                soma = img_integral[b][r][k]
                if t >= 0:
                    soma -= img_integral[t][r][k]
                if l >= 0:
                    soma -= img_integral[b][l][k]
                if t >= 0 and l >= 0:
                    soma += img_integral[t][l][k]
                img_out[y][x][k] = soma / (largura_janela * altura_janela) 
    # Aplicando janela 3x3 nas bordas
    for k in range(0, num_canais):
        for y in range(1, altura - 1):
            for x in range(1, largura - 1):
                # Se estiver na parte já borrada pula
                if y >= meia_altura_janela and y < altura - meia_altura_janela and x >= meia_largura_janela and x < largura - meia_largura_janela:
                    continue
                soma = 0.0
                # soma = g(r,b) - g(r,t) - g(l,b) + g(l,t)
                r = x + 1
                l = x - 1 - 1
                t = y - 1 - 1
                b = y + 1
                # soma = g[b,r] - g[t,r] - g[b,l] + g[t,l]
                soma = img_integral[b][r][k]
                if t >= 0:
                    soma -= img_integral[t][r][k]
                if l >= 0:
                    soma -= img_integral[b][l][k]
                if t >= 0 and l >= 0:
                    soma += img_integral[t][l][k]
                img_out[y][x][k] = soma / (3 * 3) 

    return img_out

def aplicarFiltro(img, LARGURA_JANELA, ALTURA_JANELA):
    out_name = INPUT_IMAGE[:-4] + " - borrada"
    start_time = timeit.default_timer()
    if FILTRO == 0:
        # Ingenuo
        img_out = mediaIngenuo(img, LARGURA_JANELA, ALTURA_JANELA)
        out_name += "(ingenuo) "
    elif FILTRO == 1:
        # Separavel
        img_out = mediaFiltroSeparavel(img, LARGURA_JANELA, ALTURA_JANELA)
        out_name += "(separavel) "
    elif FILTRO == 2:
        # Integrais
        img_out = mediaImagensIntegrais(img, LARGURA_JANELA, ALTURA_JANELA)
        out_name += "(integrais) "
    else:
        print("FILTRO deve estrar entre 0 e 2")
    # Mostra tempo de execução do algoritmo
    print("Tempo de execução filtro {}: {:f}".format(FILTRO, timeit.default_timer() - start_time))

    out_name += str(ALTURA_JANELA) + "x" + str(LARGURA_JANELA)
    # Mostra e salva imagem de saída(img_out)
    #cv2.imshow("{}".format(out_name), img_out)
    cv2.imwrite("{}.png".format(out_name), img_out*255)


def main():

    # Abre a imagem em escala de cinza ou colorida de acordo com flag COLOR.
    MODE = cv2.IMREAD_COLOR if COLOR else cv2.IMREAD_GRAYSCALE
    img = cv2.imread(INPUT_IMAGE, MODE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    if not COLOR:  # Se imagem esta em escala de cinza
        img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255

    # Usando algoritmo desenvolvido

    # Aplica filtro em img
    aplicarFiltro(img, LARGURA_JANELA, ALTURA_JANELA)
    
    cv2.waitKey(10000)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

# ===============================================================================
