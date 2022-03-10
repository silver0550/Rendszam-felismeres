import cv2

#kép megnyitása

img = cv2.imread('rszimg/rsz_test_1.jpg')
cv2.imshow('test', img)
cv2.waitKey(0)
