import cv2 as cv
import license_plate_detecting as lpd
import license_plate_transform as lpt

test = lpd.LicenceDet('rszimg/rsz_test_1.jpg')
test.do_it()
test.showLP()
lplate = test.get_img()
corners = test.get_corners()

lplate = lpt.lp_transfer(lplate, corners, True)

