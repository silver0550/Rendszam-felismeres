import license_plate_detecting as lpd
import license_plate_transform as lpt
import main

def step2step(number):
    for i in range(number):
        print(i+49)
        detect = lpd.LicenceDet('rszimg/rsz_test_' + str(i+49) + '.jpg')
        detect.do_it()
        #detect.show()

        lpimg = detect.get_img()
        crns = detect.get_corners()
        transf = lpt.LicenceTrans(lpimg, crns)
        transf.do_it()
        print(main.get_licence_plate('rszimg/rsz_test_' + str(i+49) + '.jpg'))
        transf.show()

def finaly_test(number):
    for i in range(number):
        text = main.get_licence_plate('rszimg/rsz_test_' + str(i+1) + '.jpg')
        if len(text) == 0:
            print('Sikertelen')
        else:
            print(text)

#step2step(66)
finaly_test(66)
