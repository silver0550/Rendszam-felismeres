import cv2 as cv
import license_plate_detecting as lpd
import license_plate_transform as lpt


if __name__ == "__main__":
    for i in range(1):
        lplate, corners = lpd.get_lplate('rszimg/rsz_test_'+str(i+1)+'.jpg',True)
        lplate = lpt.lp_transfer(lplate, corners, True)

