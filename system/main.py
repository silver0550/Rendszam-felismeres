import license_plate_detecting as lpd
import license_plate_transform as lpt
import tesseract as tess

def get_licence_plate(picture):
    detect = lpd.LicenceDet(picture)
    detect.do_it()

    lplate = detect.get_img()
    corners = detect.get_corners()

    transform = lpt.LicenceTrans(lplate, corners)
    transform.do_it()

    return tess.get_text(transform.get_img())


if __name__ == "__main__":
    picnbr= input('Kérem adja meg a leolvasandó kép sorszámát: ')
    lp = get_licence_plate('rszimg/rsz_test_'+str(picnbr)+'.jpg')
    print('A képen Látható rendszám: ', lp)
    img = lpd.LicenceDet('rszimg/rsz_test_'+str(picnbr)+'.jpg')
    img.show()

