import cv2 as cv
import imgprocess

img = cv.imread('img/multimetro.jpg')
img = cv.resize(img, (500, 500))
device = imgprocess.getDeviceContour(img)
display = imgprocess.getDisplayContour(device, 197 * 62)

cv.imshow('Device', device)
cv.imshow('Display', display)
cv.waitKey(0)