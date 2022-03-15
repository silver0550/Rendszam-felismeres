import cv2 as cv


def show_Lplate(picture):
    'rendszám-tábla detektálása ( eredményként egy maszkot ad vissza )'

    # Kép megnyitása -> szürke árnyalat-> átméretezés
    img = cv.imread(picture, cv.IMREAD_COLOR)
    img = cv.resize(img, (800, 800))
    img_act = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Zajcsökkentés
    img_act = cv.bilateralFilter(img_act, 5, 100, 500)

    # Éldetektálás
    img_act = cv.Canny(img_act, 0, 250, None)

    # Contúrok detektálása
    contours, hierarchy = cv.findContours(img_act, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contureSizes = []

    for i in range(len(contours)):
        size = cv.contourArea(contours[i])
        contureSizes.append((size, i))
    contureSizes.sort(reverse=True)

    # találatok tesztelése
    chek: int
    for i in range(10):
        chek = contureSizes[i][1]
        break

    #Rendszám kirajzolása, maszk létrehozása
    cv.drawContours(img, contours, chek, (0, 0, 255), -1)


    return img



if __name__ == "__main__":
    cv.imshow('Picure', show_Lplate('rszimg/rsz_test_3.jpg'))
    cv.waitKey(0)
    cv.destroyAllWindows()