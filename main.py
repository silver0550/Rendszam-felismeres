import license_plate_detecting as lpd
import license_plate_transform as lpt

detect = lpd.LicenceDet('rszimg/rsz_test_1.jpg')

detect.do_it()

lplate = detect.get_img()
corners = detect.get_corners()

transform = lpt.LicenceTrans(lplate, corners)
transform.do_it()
transform.show()



