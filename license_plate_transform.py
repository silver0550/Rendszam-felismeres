import cv2 as cv
import numpy as np

class LicenceTrans:
    """ Méretezi és pozícionálja a rendszámot """

    def __init__(self, lpimg, crns):
        self.masked_lplate = lpimg
        self.corners = np.where(crns > 0)       # sarkok helyének meghatározása
        self.error = (False, None, None)

    def create_point(self):
        """ Összepárosítja a koordinátákat """

        self.pair = []
        for i in range(len(self.corners[0])):
            pont = (self.corners[1][i], self.corners[0][i])
            self.pair.append(pont)

    def distance_p2p(self, pt1, pt2, max_d=-1):
        """ Igaz, ha a 2 pont között nagyobb a távolság mint max_d """

        distance = np.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)
        if max_d < 0:
            return distance
        else:
            return distance <= max_d

    def avg(self, pont_list):
        """ Pontokat tartalmazó lista átlagát adja eredményül """
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

    def group_corners(self):
        """Sarkok definiálása"""                                    # sarok csoportosítása

        self.before_transfer = []

        while True:
            ref_point = None
            point = []
            delete_list = []

            for i in self.pair:                                     # az egymáshoz közeli pontok csoportba rendezése
                if ref_point == None:
                    ref_point = self.pair[0]
                    point.append(ref_point)

                else:
                    if self.distance_p2p(ref_point, i, 20):
                        point.append(i)

                    else:
                        delete_list.append(i)

            self.pair = delete_list
            self.before_transfer.append(self.avg(point))            # 1 sarokhoz tartozó pontokból 1 pont kijelölése

            if len(self.pair) == 0:
                break


    def order_corners(self):
        """Sarkok sorba rendezése ( Top Left, Bottom Left, Top Right, Bottom Right )"""

        if len(self.before_transfer) != 4:  # ! hiba kezelése !
            self.error = (True, '! 4 Point error !', 'transform/order_corners')


        self.before_transfer.sort()

        if self.before_transfer[0][1] > self.before_transfer[1][1]:
            self.before_transfer[0], self.before_transfer[1] = self.before_transfer[1], self.before_transfer[0]

        if self.before_transfer[2][1] > self.before_transfer[3][1]:
            self.before_transfer[2], self.before_transfer[3] = self.before_transfer[3], self.before_transfer[2]

        self.before_transfer= np.float32(self.before_transfer)

    def new_points(self):
        """ Meghatározza a transofmáció utáni sarokpontokat """

        bigger_edge = []  # leghosszabb élek meghatározása     ! Szebb megoldást keresni !

        ab = self.distance_p2p(self.before_transfer[0], self.before_transfer[1])
        ac = self.distance_p2p(self.before_transfer[0], self.before_transfer[2])
        bd = self.distance_p2p(self.before_transfer[1], self.before_transfer[3])
        cd = self.distance_p2p(self.before_transfer[2], self.before_transfer[3])

        if ac > bd:
            bigger_edge.append(ac)
        else:
            bigger_edge.append(bd)
        if ab > cd:
            bigger_edge.append(ab)
        else:
            bigger_edge.append(cd)

        self.after_transfer = [(0, 0), (0, bigger_edge[1]), (bigger_edge[0], 0), (bigger_edge[0], bigger_edge[1])]
        self.after_transfer = np.float32(self.after_transfer)
        self.after_size = (int(bigger_edge[0]), int(bigger_edge[1]))

    def transform(self):
        """Transformálás végrehajtása"""

        matrix = cv.getPerspectiveTransform(self.before_transfer, self.after_transfer)          # perspektíva számolása
        self.result = cv.warpPerspective(self.masked_lplate, matrix, self.after_size)           # transformálás
        _, self.result = cv.threshold(self.result, 127, 255, cv.THRESH_BINARY)

    def get_img(self):
        return self.result

    def show(self):
        cv.imshow('show_transfer', self.result)
        cv.waitKey()
        cv.destroyAllWindows()

    def get_error(self):
        return self.error

    def do_it(self):
        self.create_point()                                     # koordináták párosítása tuplebe
        self.group_corners()                                    # sarokpontok csoporjának középpontja
        try:
            self.order_corners()                                # sarokpontok sorrendje
            self.new_points()                                   # pontok eltolt pozíciójának számolása
            self.transform()                                    # transformálás végrehajtása
        except:
            self.result= cv.imread('fail.jpg')



if __name__ == "__main__":
    import license_plate_detecting as lpd

    test = lpd.LicenceDet('rsz_test_1.jpg')
    test.do_it()
    #test.show_corners()
    sarok = test.get_corners()
    maszkolt = test.get_img()
    test.showLP()

    test2 = LicenceTrans(maszkolt, sarok)
    test2.do_it()
    test2.show_transfer()
