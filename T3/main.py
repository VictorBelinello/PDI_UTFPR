import sys
import numpy as np
import cv2

######################################################################################################
#INPUT_IMAGE = "Wind Waker GC.bmp"
INPUT_IMAGE = "GT2.BMP"
OUTPUT_NAME = INPUT_IMAGE[:-4]                  # Nome usado no titulo das janelas apresentando os resultados
BRIGHT_THRESHOLD = 0.8                          # Quanto menor mais 'partes' da imagens sofrem o efeito de bloom

                                                # Qual 'metodo' para gerar a mascara de fontes de luz
BRIGHT_OPTIONS = ["HSL"]                        # NP_WHERE ou HSL se colocar os 2 ira rodar com ambos e criar imagens para cada resultado

                                                # Qual metodo para borrar a mascara
BLUR_OPTIONS = ["BOX_FILTER"]                   #GAUSSIAN ou BOX_FILTER se colocar os 2 ira rodar com ambos e criar imagens para cada resultado

NUMBER_BLURS = 5                                #Quantas vezes a mascara sera borrada, quanto maior mais o efeito é evidente
START_KSIZE = 25                                #Tamanho inicial do kernel(deve ser impar), nao parece ter mt efeito no filtro gaussiano, ja no box filter tem resultadores melhores para valores maiores
END_KSIZE = START_KSIZE + (NUMBER_BLURS*2)      #ksize deve sempre ser impar

SHOW_INTERM_IMG = False                         #Mostrar ou nao imagens intermediarias (bright pass e blur)
######################################################################################################

def brightPass(img, option):
    if not isinstance(img, np.ndarray):
        raise Exception("img is not numpy ndarray")
    if option == "NP_WHERE": # Simples de implementar, mas o resultado nao é mt bom
        # E nao descobri se a comparação usa uma media ou se todos estão acima do valor
        return np.where(img > BRIGHT_THRESHOLD, img, 0)
    elif option == "HSL": # Parece ter um resultado visual melhor
        imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        mask = cv2.inRange(imgHLS[:,:,1], BRIGHT_THRESHOLD, 1)
        return cv2.bitwise_or(img, img, mask=mask)
    else:
        raise Exception(f"bright option '{option}' is not valid.")

def blur(img, option):
    if not isinstance(img, np.ndarray):
        raise Exception("img is not numpy ndarray")
    blurImg = np.zeros(img.shape)
    imgCopy = img.copy()

    if option == "GAUSSIAN":
        for i in range(START_KSIZE,END_KSIZE,2): 
            imgCopy = cv2.GaussianBlur(imgCopy, (i, i), 3)
            blurImg += imgCopy
        return blurImg
    elif option == "BOX_FILTER":
        for i in range(START_KSIZE,END_KSIZE,2):
            imgCopy = cv2.boxFilter(imgCopy, -1, (i, i))
            blurImg += imgCopy
        return np.where(blurImg > 1, 1, blurImg)
    else:
        raise Exception(f"blur option '{option}' is not valid")

def bloom(img):   
    cv2.imshow(OUTPUT_NAME, img)

    brightImages = []    
    for option in BRIGHT_OPTIONS:
        brightImages.append( brightPass(img, option) )
    if SHOW_INTERM_IMG:
        for idx, bright in enumerate(brightImages):
            cv2.imshow(f"{OUTPUT_NAME} brightPass {BRIGHT_OPTIONS[idx]}" , bright)
   

    blurredImages = []
    
    for option in BLUR_OPTIONS:
        for bright in brightImages:
            blurredImages.append( blur(bright, option))
    if SHOW_INTERM_IMG:
        for idx, blurred in enumerate(blurredImages):
            cv2.imshow(f"{OUTPUT_NAME} blurred {idx}" , blurred)
    
    outputImages = []
    for blurredImg in blurredImages:
        out = img + 0.7*blurredImg
        outputImages.append( out )

    for idx, output in enumerate(outputImages):
        cv2.imshow(f"{OUTPUT_NAME} bloom {idx}" , output)

    

def main():
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()
    
    # Converte para float32.
    img = img.astype(np.float32) / 255
    
    bloom(img)
    # O numero de images resultantes eh dado por: len(BRIGHT_OPTIONS) * len(BLUR_OPTIONS)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()