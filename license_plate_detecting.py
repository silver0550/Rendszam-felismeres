import cv2 as cv
import numpy as np


def open2canny(picture, size=(0.15, 0.15), billfil=(3, 80, 150), canny=(100, 200)):

    # Kép megnyitása -> átméretezés -> szürke árnyalat
    img = cv.imread(picture, cv.IMREAD_COLOR)
    img = cv.resize(img, None, fx=size[0], fy=size[1])
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Zajcsökkentés
    img_bil = cv.bilateralFilter(img_gray, billfil[0], billfil[1], billfil[2])

    # Éldetektálás
    img_canny = cv.Canny(img_bil, canny[0], canny[1])

    return img_canny, img


def contour_detect(picture):        #  ! rendszámtábla tesztelése !

    # Contúrok detektálása
    contours, _ = cv.findContours(picture, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    conture_sizes = []

    # A talált alakzatok méret szerinti sorbarendezése
    for i in range(len(contours)):
        size = cv.contourArea(contours[i])
        conture_sizes.append((size, i))

    conture_sizes.sort(reverse=True)
    biggest_contour = conture_sizes[0][1]

    return contours, biggest_contour


def create_mask(size, contours, license_plate):

    # Maszk készítés
    img_mask = np.ndarray(size, np.uint8)
    img_mask.fill(0)
    cv.drawContours(img_mask, contours, license_plate, (255, 255, 255), -1)

    # Hibák vágása ( finomítás )
    kernel = np.ones((5, 5), np.uint8)
    img_morph = cv.morphologyEx(img_mask, cv.MORPH_OPEN, kernel)
    img_morph = cv.cvtColor(img_morph, cv.COLOR_RGBA2GRAY)

    return img_morph


def get_corners(img_mask, size=(5, 5), senz=0.08):

    # Sarokdetekktálás
    corners = cv.cornerHarris(img_mask, size[0], size[1], senz)

    return corners


def cut_the_mask(picture, mask):

    picture[mask < 255] = 0
    return picture


def get_lplate(picture, showme=False):
    'rendszám-tábla detektálása ( eredménynek a rendszám-táblát és sarokpontjait adja vissza )'

    img_canny, img = open2canny(picture)                                # élek kiemelése

    contours, license_plate = contour_detect(img_canny)                 # rendszámtábla detektálása

    img_mask = create_mask(img.shape, contours, license_plate)          # maszk készítése

    corners = get_corners(img_mask)                                     # Sarkok keresése

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    result = cut_the_mask(img_gray, img_mask)                           # maszk kivágása

    if showme:
        cv.imshow('get_Lplate', result)
        cv.waitKey()
        cv.destroyAllWindows()

    return result, corners


if __name__ == "__main__":

    image, _ = get_lplate('rsz_test_1.jpg', True)

