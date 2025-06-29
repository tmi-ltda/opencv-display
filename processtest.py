import cv2 as cv
import imgprocess

imgs = [
  cv.imread('img/multimetro.jpg'),
  cv.imread('img/multimetro1.jpg'),
  cv.imread('img/multimetro2.jpg'),
  cv.imread('img/multimetro3.jpg'),
  cv.imread('img/multimetro4.jpg'),
  cv.imread('img/multimetro5.jpg'),
  cv.imread('img/multimetro6.jpg'),
  cv.imread('img/multimetro7.jpg'),
]

for i in range(len(imgs)):
  img = cv.resize(imgs[i], (500,500))
  device = imgprocess.getDeviceContour(img)

  if device is not None:
    device_w, device_h = device.shape[:2]
    display = imgprocess.getDisplayContour(device, (device_w * device_h) * 0.15)
    if display is not None:
      display_w, display_h = display.shape[:2]
      segments = imgprocess.getDigitRois(display, (display_w * display_h) * 0.05)
      cv.imshow('Display', display)
  k = cv.waitKey(0)
  if chr(k) == 'c': break
  cv.destroyAllWindows()
# cv.imshow('Device', device)
# cv.imshow('Display', display)