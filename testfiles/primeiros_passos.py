import cv2 as cv

img = cv.imread("img/display.png", cv.IMREAD_GRAYSCALE)
cv.imshow("Display window", img)
k = cv.waitKey(0)