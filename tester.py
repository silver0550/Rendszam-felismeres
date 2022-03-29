import license_plate_detecting as lpd
import license_plate_transform as lpt


tester = {}
i = 0
while True:
    i += 1
    try:
        detect = lpd.LicenceDet('rszimg/rsz_test_' + str(i) + '.jpg')
        #detect.set_corneratrib((5, 5), 0.1)
        detect.do_it()

        transform = lpt.LicenceTrans(detect.get_img(), detect.get_corners())
        transform.do_it()
        #transform.show()
        tester[i] = transform.get_error()

    except:
        break

errors = []
for i in tester:
    if tester[i][0]:
       errors.append(i)

print('hibák száma: ', len(errors))
if len(errors):
    print('Hibás átalakítások: ')
    for i in errors:
         print('rsz_test_'+str(i), '\tHiba típusa: ', tester[i][1])
