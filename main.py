import cv2 as cv
import numpy as np


def show_lplate(picture, showme=False):
    'rendszám-tábla detektálása ( eredménynek a rendszám-táblát és sarokpontjait adja vissza )'

    # Kép megnyitása -> szürke árnyalat-> átméretezés
    img = cv.imread(picture, cv.IMREAD_COLOR)
    img = cv.resize(img, None,fx=0.15,fy=0.15)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Zajcsökkentés
    img_bil = cv.bilateralFilter(img_gray, 4, 100, 200)

    # Éldetektálás
    img_canny = cv.Canny(img_bil, 100, 200)

    # Contúrok detektálása
    contours, _ = cv.findContours(img_canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contureSizes = []

    for i in range(len(contours)):
        size = cv.contourArea(contours[i])
        contureSizes.append((size, i))

    contureSizes.sort(reverse=True)

    # találatok tesztelése ! FEJLESZTÉS ALATT !
    lplate: int
    for i in range(1):
        lplate = contureSizes[i][1]
        # if test:
        #   break
        # return ERROR

    #Masz készítés
    img_mask=np.ndarray((img.shape), np.uint8)
    img_mask.fill(0)
    cv.drawContours(img_mask, contours, lplate, (255, 255, 255), -1)

    #Hibák vágása ( finomítás)
    kernel = np.ones((5, 5), np.uint8)
    img_morph = cv.morphologyEx(img_mask, cv.MORPH_OPEN, kernel)
    img_morph = cv.cvtColor(img_morph, cv.COLOR_RGBA2GRAY)

    #sarokdetekktálás
    corners = cv.cornerHarris(img_morph, 5, 5, 0.05)

    #RSZ kivágás
    img_gray[img_morph < 255] = 0

    if showme:
        cv.imshow('show_Lplate', img_gray)
        cv.waitKey()

    return img_gray, corners

def rszNorm(picture,corners):
    'Méretezi és pozícionálja a rendszámot'

    # picture[corners>0.01*corners.max()] = 255
    # cv.imshow('norm',picture)
    # cv.waitKey()


if __name__ == "__main__":
    for i in range(1):
        lplate, corners = show_lplate('rszimg/rsz_test_'+str(i+1)+'.jpg', True)
        rszNorm(lplate, corners)

    cv.destroyAllWindows()
