import sys
import numpy as np
import numpy.ma as ma
import cv2

#INPUT_IMAGE = "Wind Waker GC.bmp"
INPUT_IMAGE = "GT2.BMP"
OUTPUT_NAME = INPUT_IMAGE[:-4]
BRIGHT_THRESHOLD = 0.7

def bright_pass(img, option):
    if not isinstance(img, np.ndarray):
        raise Exception("img is not numpy ndarray")
    if option == 0:
        return np.where(img > BRIGHT_THRESHOLD, img, 0)
    else:
        imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
        imgL = imgHLS[:,:,1]
        mask = cv2.inRange(imgL, BRIGHT_THRESHOLD, 1)
        return cv2.bitwise_and(img, img, mask=mask)

def blur(img, option):
    if not isinstance(img, np.ndarray):
        raise Exception("img is not numpy ndarray")
    blurImg = np.zeros(img.shape)
    MAX_LOOPS = 9
    if option == 0:
        for i in range(1,MAX_LOOPS,2):
            ksize = (5 * i, 5 * i)
            blurImg += cv2.GaussianBlur(img, ksize, 3)
        return np.where(blurImg > 1, 1, blurImg)
    else:
        for i in range(1,MAX_LOOPS,2):
            kernel = np.ones((5*i,5*i), np.float32)/(25*i*i)
            blurImg += cv2.filter2D(img, -1, kernel)
        return np.where(blurImg > 1, 1, blurImg)

def main():
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()
    
    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.astype(np.float32) / 255
    
    cv2.imshow(OUTPUT_NAME, img)
    cv2.waitKey(2000)
    
    bright = bright_pass(img, 1)
    cv2.imshow(OUTPUT_NAME, bright)
    cv2.waitKey(2000)

    option = 1
    if option == 1:
        blured = blur(bright, 1)
        cv2.imshow(OUTPUT_NAME, blured)
        cv2.waitKey(2000)
        out = 0.7*blured + img
        
        cv2.imshow(OUTPUT_NAME, out)
        cv2.waitKey(2000)

        out = 0.3*blured + img
        
        cv2.imshow(OUTPUT_NAME, out)
        cv2.waitKey(2000)
    else:
        blured = blur(bright, 0)
        cv2.imshow(OUTPUT_NAME, blured)
        cv2.waitKey(2000)
        out = blured + img
        cv2.imshow(OUTPUT_NAME, out)
        cv2.waitKey(2000)
    # out, out2 = bright_pass(img)
    # cv2.imshow(OUTPUT_NAME,out )

    # cv2.waitKey(2000)

    # cv2.imshow(OUTPUT_NAME,out2 )
    # cv2.waitKey(2000)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()