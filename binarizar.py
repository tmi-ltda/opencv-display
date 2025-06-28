import cv2 as cv
import numpy as np

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
contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)