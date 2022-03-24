import cv2 as cv
import numpy as np


def show_lplate(picture, showme=False):
    'rendszám-tábla detektálása ( eredménynek a rendszám-táblát és sarokpontjait adja vissza )'

    # Kép megnyitása -> szürke árnyalat-> átméretezés
    img = cv.imread(picture, cv.IMREAD_COLOR)
    img = cv.resize(img, None, fx=0.15, fy=0.15)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Zajcsökkentés
    img_bil = cv.bilateralFilter(img_gray, 3, 80, 150)

    # Éldetektálás
    img_canny = cv.Canny(img_bil, 100, 200)

    # Contúrok detektálása
    contours, _ = cv.findContours(img_canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    conture_sizes = []

    for i in range(len(contours)):
        size = cv.contourArea(contours[i])
        conture_sizes.append((size, i))

    conture_sizes.sort(reverse=True)

    # Találatok tesztelése ! FEJLESZTÉS ALATT !
    lplate: int
    for i in range(1):
        lplate = conture_sizes[i][1]
        # if test:
        #   break
        # return ERROR

    # Maszk készítés
    img_mask = np.ndarray((img.shape), np.uint8)
    img_mask.fill(0)
    cv.drawContours(img_mask, contours, lplate, (255, 255, 255), -1)

    # Hibák vágása ( finomítás )
    kernel = np.ones((5, 5), np.uint8)
    img_morph = cv.morphologyEx(img_mask, cv.MORPH_OPEN, kernel)
    img_morph = cv.cvtColor(img_morph, cv.COLOR_RGBA2GRAY)

    # Sarokdetekktálás
    corners = cv.cornerHarris(img_morph, 5, 5, 0.08)

    # RSZ kivágás
    img_gray[img_morph < 255] = 0

    if showme:
        cv.imshow('show_Lplate', img_gray)
        cv.waitKey()

    return img_gray, corners


def rsz_poz(picture, corners):
    'Méretezi és pozícionálja a rendszámot, eredményül a rendszám képét adja'

    def create_point(corners):
        ' Összepárosítja a koordinátákat '

        points = []
        for i in range(len(corners[0])):
            pont = (corners[1][i], corners[0][i])
            points.append(pont)
        return points

    def distance_p2p(pt1, pt2, max_d=0):
        ' Igaz, ha a 2 pont között maximum max_d a távolság'

        distance = np.sqrt((pt2[0]-pt1[0])**2+(pt2[1]-pt1[1])**2)
        if max_d <= 0:
            return distance
        else:
            return distance <= max_d

    def avg(pont_list):
        ' Pontokat tartalmazó lista átlagát adja eredményül'
        sumx = 0
        sumy = 0
        if len(pont_list) == 0:
            return False

        for i in range(len(pont_list)):
            sumx += pont_list[i][0]
            sumy += pont_list[i][1]
        x = int(sumx / len(pont_list))
        y = int(sumy / len(pont_list))

        return (x, y)

    def group_corners(point_corners):
        'Sarkok definiálása'    #sarok csoportosítása

        fourpoint=[]

        while True:
            ref_point = None
            point = []
            delete_list = []

            for i in point_corners:     # az egymáshoz közeli pontok csoportba rendezése
                if ref_point == None:
                    ref_point = point_corners[0]
                    point.append(ref_point)

                else:
                    if distance_p2p(ref_point, i, 20):
                        point.append(i)

                    else:
                        delete_list.append(i)

            point_corners = delete_list
            fourpoint.append(avg(point))    # 1 sarokhoz tartozó pontokból 1 pont kijelölése

            if len(point_corners) == 0:
                break

        return fourpoint

    def order_corners(corners):
        ' Sarkok elhelyezése ( Top Left, Bottom Left, Top Right, Bottom Right )'

        if len(corners) != 4:   # ! hiba kezelése !
            print('error')
            return 'number error'

        corners.sort()

        if corners[0][1] > corners[1][1]:
             corners[0], corners[1] = corners[1], corners[0]

        if corners[2][1] > corners[3][1]:
             corners[2], corners[3] = corners[3], corners[2]

        return corners

    def new_points(befor_transfer):
        ' Meghatározza a transofmáció utáni sarokpontokat '

        bigger_edge = []   # leghosszabb élek meghatározása     ! Szebb megoldást keresni !

        ab = distance_p2p(befor_transfer[0], befor_transfer[1])
        ac = distance_p2p(befor_transfer[0], befor_transfer[2])
        bd = distance_p2p(befor_transfer[1], befor_transfer[3])
        cd = distance_p2p(befor_transfer[2], befor_transfer[3])

        if ac > bd:
            bigger_edge.append(ac)
        else:
            bigger_edge.append(bd)
        if ab > cd:
            bigger_edge.append(ab)
        else:
            bigger_edge.append(cd)

        after_transfer = [(0, 0), (0, bigger_edge[1]), (bigger_edge[0], 0), (bigger_edge[0], bigger_edge[1])]

        return np.float32(after_transfer), (int(bigger_edge[0]), int(bigger_edge[1]))

    corners = np.where(corners > 0)                     # sarkok helyének meghatározása
    corners= create_point(corners)                      # koordináták párosítása tuplebe
    pts_before = group_corners(corners)                 # sarokpontok csoporjának középpontja
    pts_before = np.float32(order_corners(pts_before))  # sarokpontok sorrendje
    pts_after, size = new_points(pts_before)            # pontok eltolt pozíció

    matrix = cv.getPerspectiveTransform(pts_before,pts_after)       # perspektíva számolása
    result = cv.warpPerspective(picture, matrix, size)              # transformálás
    _, result = cv.threshold(result, 127, 255, cv.THRESH_BINARY)

    return result


if __name__ == "__main__":
    for i in range(1):
        lplate, corners = show_lplate('rszimg/rsz_test_'+str(i+10)+'.jpg')
        rsz = rsz_poz(lplate, corners)
        cv.imshow('clear lplate', rsz)      # harrist kell finomítani
        cv.waitKey()

    cv.destroyAllWindows()
