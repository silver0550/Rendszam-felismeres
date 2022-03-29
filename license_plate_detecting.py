import cv2 as cv
import numpy as np


class LicenceDet:
    'rendszám-tábla detektálása ( eredménynek a rendszám-táblát és sarokpontjait adja vissza )'
    def __init__(self, picture, size=(0.15, 0.15)):
        self.img = cv.imread(picture)
        self.config_picturesize = size
        self.img = cv.resize(self.img, None, fx=self.config_picturesize[0], fy=self.config_picturesize[1])

    # Default értékek beállítása
        self.img_orig = self.img
        self.config_bilfil = (3, 80, 150)
        self.config_canny = (100, 200)
        self.biggest_contour = None
        self.config_contours = None
        self.config_cubesize = (5, 5)
        self.config_sensitivity = 0.06
        self.config_corners = None

    def show_config(self):
        print('Szűrő:\t"Bilateral filter"\tbeállításai: ', self.config_bilfil)
        print('Éldetektálás:\t"Canny"\tbeállításai: ', self.config_canny)
        print('Sarok detektálás:\t "Harris"\tbeállításai: ', self.config_cubesize, self.config_sensitivity)

    # Méret
    def get_size(self):
        return self.config_picturesize

    def set_size(self, size):
        self.config_picturesize = size

    # Szürke árnyalat
    def gray(self):
        self.img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

    # Zajcsökkentés
    def get_billfil(self):
        return self.config_bilfil

    def set_billfil(self, sigmaC, sigmaS, dst):
        self.config_bilfil = (sigmaC, sigmaS, dst)

    def bilfil(self):
        self.img = cv.bilateralFilter(self.img, self.config_bilfil[0], self.config_bilfil[1], self.config_bilfil[2])

    # Éldetektálás
    def get_canny(self):
        return self.config_canny

    def set_canny(self, trash1, trash2):
        self.config_canny = (trash1, trash2)

    def canny(self):
        self.img = cv.Canny(self.img, self.config_canny[0], self.config_bilfil[1])

    # Contúrok detektálása
    def contour_detect(self):  # ! rendszámtábla tesztelése !

        self.config_contours, _ = cv.findContours(self.img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        conture_sizes = []

        # A talált alakzatok méret szerinti sorbarendezése
        for i in range(len(self.config_contours)):
            size = cv.contourArea(self.config_contours[i])
            conture_sizes.append((size, i))

        conture_sizes.sort(reverse=True)
        self.biggest_contour = conture_sizes[0][1]

    # Maszk készítése
    def mask(self):

        self.img_mask = np.ndarray(self.img.shape, np.uint8)
        self.img_mask.fill(0)
        cv.drawContours(self.img_mask, self.config_contours, self.biggest_contour, (255, 255, 255), -1)

        # Hibák vágása ( finomítás )
        kernel = np.ones((10, 10), np.uint8)
        self.img_mask = cv.morphologyEx(self.img_mask, cv.MORPH_OPEN, kernel)


    # Sarok detekktálás
    def get_corneratrib(self):
        return (self.config_cubesize, self.config_sensitivity)

    def set_corneratrib(self, cubesize, sensitivity):
        self.config_cubesize = cubesize
        self.config_sensitivity = sensitivity

    def corners(self):
        self.config_corners = cv.cornerHarris(self.img_mask, self.config_cubesize[0], self.config_cubesize[1],
                                              self.config_sensitivity)
    def get_corners(self):
        return self.config_corners

    def show_corners(self):
        try:
            self.img_orig[self.config_corners > 0] = [0, 0, 255]
        except:
            print('A sarkok nincsenek detektálva!\nFuttassa le a detektálást!')

    # Rendszámtábla kivágása
    def cut_the_mask(self):
        self.img_orig[self.img_mask < 255] = 0
        self.img = self.img_orig

    def get_img(self):
        return cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

    def show(self):
        cv.imshow('showLP', self.img)
        print('A kép méretei: ', self.img.shape)
        cv.waitKey()
        cv.destroyAllWindows()

    def do_it(self):
        self.gray()
        self.bilfil()
        self.canny()
        self.contour_detect()
        self.mask()
        self.corners()
        self.cut_the_mask()


if __name__ == "__main__":
    test1 = LicenceDet('rsz_test_3.jpg')
    test1.do_it()
    test1.show_corners()
    test1.showLP()
