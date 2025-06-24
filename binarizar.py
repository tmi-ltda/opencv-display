import cv2 as cv
import numpy as np
import os

# Carregar e redimensionar imagem
img_dir = r'.\img'
img = cv.imread(f"{img_dir}\\multimetro.jpg")
img = cv.resize(img, (500, 500))

# Converter imagem para preto e branco e aplicar filtro gaussiano
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blurred_img = cv.GaussianBlur(gray_img, (3, 3), 0)

# Binarizar imagem
_, thresh = cv.threshold(blurred_img, 120, 255, cv.THRESH_BINARY_INV)

# Encontrar contornos
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Filtrar contornos através de uma aréa mínima para evitar pequenos ruídos (carece de ajustes)
for cnt in contours:
  area = cv.contourArea(cnt)
  if area > 100 * 50:
      x, y, w, h = cv.boundingRect(cnt)
      cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv.imshow("Imagem binarizada", thresh)
cv.imshow("Imagem com contorno", img)
k = cv.waitKey(0)

if chr(k) == 's':
  print(f'Imagem salva em: {img_dir}\\display_binario.jpg'.replace('.\\', ''))
  cv.imwrite(f'{img_dir}\\display_binario.jpg', thresh)