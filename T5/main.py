import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

#===============================================================================

BASE_IMAGE = 'img/1.BMP'
BASE_IMAGE_NAME = BASE_IMAGE[4:-4]
BACKGROUND_IMAGE = 'backgrounds/background2.jpg'

#===============================================================================
def getBackgroundImage(original_shape):
	background = cv.imread(BACKGROUND_IMAGE)
	if background is None:
		sys.exit(f"Error reading the image at {BACKGROUND_IMAGE}")
	
	dim = (original_shape[1],original_shape[0])
	resized = cv.resize(background, dim)

	cv.imshow("Background", resized)
	key = cv.waitKey(0)
	if key == ord("s"):
		cv.imwrite(f"resultados/Background{BASE_IMAGE_NAME}.png", resized)
	return resized

def removeBackground(img):
	# Separa os 3 canais e remapeia entre 0 e 1
	red_ratio = img[:, :, 0] / 255
	green_ratio = img[:, :, 1] / 255
	blue_ratio = img[:, :, 2] / 255
	
	# Obtem as relacoes entre R e G, B e G
	# Soma valor arbitrario para que valores negativos (mas pequenos em modulo) fiquem acima de 0
	# Pixels escuros facilmente ficariam negativos, o que atrapalharia o proximo passo (onde seriam confundidos com o fundo)
	offset = .1 # Baixar ou subir muito causa problemas. Explicacao analoga a variavel min_alfa no metodo blendBackground abaixo
	red_vs_green = (red_ratio - green_ratio) + offset 
	blue_vs_green = (blue_ratio - green_ratio) + offset

	# Os valores negativos, provavelmente indicam um fundo verde, pois o green_ratio foi consideravelmente maior que o outro canal
	# Trunca os valores para 0
	red_vs_green[red_vs_green < 0] = 0
	blue_vs_green[blue_vs_green < 0] = 0

	# Usa o canal alfa para misturar as imagens posteriormente
	# No fundo os valores em red_vs_green e blue_vs_green devem ser 0. Fundo deve ter contribuicao alfa em 0
	# Nas bordas um deles deve ser 0, mas o outro nao, mas eh um valor baixo. Bordas devem ter uma contribuicao alfa baixa (mas nao zero)
	# Na imagem de interesse os valores sao positivos, potencialmente altos.  Imagem de interesse deve ter uma contribuicao alfa alta
	alpha = (red_vs_green + blue_vs_green) * 255
	# Trunca a partir de valor arbitrario 
	alpha[alpha > 255] = 255 # Para ver o resultado precisa salvar a imagem 'Alpha'

	# Seta o canal alpha da imagem original
	img[:, :, 3] = alpha

	cv.imshow("Alpha", alpha)
	key = cv.waitKey(0)
	if key == ord("s"):
		cv.imwrite(f"resultados/AlphaMask{BASE_IMAGE_NAME}.png", alpha)
	return img

def blendBackground(img, background):
	# Subir muito esse valor causa problemas, pois algumas cores comecam a ser consideradas fundo verde
	# Amarelo por exemplo( na camisa da foto 6) o valor red_vs_green eh perto de 0.03 e blue_vs_green fica truncado em 0, logo tem um alfa baixo
	# Logo dependendo desse limiar um alfa baixo (como esse amarelo) pode ser confundindo com o fundo verde
	# Serve apenas para ver o resultado em caso diferentes como o explicado acima, o melhor valor parece ser sempre 0 mesmo
	min_alfa = 5 
	blended = np.copy(background)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i, j, 3] > min_alfa:
				blended[i, j, :] = img[i, j, :3]
	cv.imshow("Blended", blended)
	key = cv.waitKey(0)
	if key == ord("s"):
		cv.imwrite(f"resultados/Blended{BASE_IMAGE_NAME}.png", blended)
	return blended

def main(img):
	# Mostra imagem original, com o fundo verde
	cv.imshow("Original", img)
	key = cv.waitKey(0)
	if key == ord("s"): # Salva se pressionou tecla 's'
		cv.imwrite(f"resultados/Original{BASE_IMAGE_NAME}.png", img)

	# Retira o fundo da imagem (usando o canal alfa como mascara)
	# Altera a imagem original
	img = removeBackground(img)

	# Carrega a imagem de fundo, ja redimensionada se necessario
	background = getBackgroundImage(img.shape)

	# Mistura o fundo carregado e a imagem, usando o canal alfa da imagem
	final = blendBackground(img, background)

if __name__ == "__main__":
	img = cv.imread(BASE_IMAGE)
	if img is None:
		sys.exit(f"Error reading the image at {BASE_IMAGE}")
	print(f"Loading image {BASE_IMAGE_NAME} with shape(h,w,c) {img.shape}")
	print("Pressing the key 's' saves the image")
	img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
	main(img)