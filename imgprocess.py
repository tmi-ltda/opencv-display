import cv2 as cv
import numpy as np

# Função para binarizar a imagem
def getBinaryImage(img, gaussian_ksize):
  # Converter a imagem para cinza
  gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  # Aplicação do filtro gaussiano
  blurred_img = cv.GaussianBlur(gray_img, gaussian_ksize, 0)
  # Binarização da imagem
  binary_img = cv.adaptiveThreshold(blurred_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 23, 2)

  return binary_img

def getDeviceContour(img):
  # Obter a imagem binarizada
  binary_img = getBinaryImage(img, (5, 5))
  # Encontrar contornos na imagem binarizada
  contours, _ = cv.findContours(binary_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  # Retornar o maior contorno encontrado
  if contours:
    cnt = max(contours, key=cv.contourArea)
    x, y, w, h = cv.boundingRect(cnt)
    return img[y:y+h, x:x+w]
  return None

def getDisplayContour(img, target_area):
  # Obter a imagem binarizada
  binary_img = getBinaryImage(img, (3, 3))
  # Encontrar contornos na imagem binarizada
  # cv.imshow('Binary Image', binary_img)
  contours, _ = cv.findContours(binary_img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

  for cnt in contours:
    area = cv.contourArea(cnt)
    if target_area * 0.3 <= area <= target_area * 1.4:
      # Aproximar o contorno para reduzir o número de pontos
      epsilon = 0.0420 * cv.arcLength(cnt, True)
      approx = cv.approxPolyDP(cnt, epsilon, True)
      if len(approx) == 4 and cv.isContourConvex(approx):
        angles = []
        for i in range(4):
          p1 = approx[i][0]
          p2 = approx[(i + 1) % 4][0]
          p3 = approx[(i + 2) % 4][0]

          v1 = p1 - p2
          v2 = p3 - p2
          cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
          angle = np.degrees(np.arccos(cos_angle))
          angles.append(angle)

          if all(a >= 85 and a <= 95 for a in angles):
            x, y, w, h = cv.boundingRect(cnt)
            # cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv.imshow('Display contour', img)

            margin_y = int(h * 0.05)
            return img[y + margin_y:y+h - margin_y, x:x+w]
  return None

def getDigitRois(img, target_area):
  # Obter a imagem binarizada
  binary_img = getBinaryImage(img, (3, 3))

  # Eliminar contornos muito pequenos ou muito grandes antes de aplicar morfologia
  contours, _ = cv.findContours(binary_img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

  kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 4))
  binary_img = cv.erode(binary_img, kernel, iterations=1)

  for cnt in contours:
    area = cv.contourArea(cnt)

    if area < target_area * 0.09:
      x, y, w, h = cv.boundingRect(cnt)
      cv.rectangle(binary_img, (x, y), (x + w, y + h), (0, 0, 0), -1)
      
  # Aplicar transformações morfológicas para melhorar a detecção
  kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 3))
  binary_img = cv.dilate(binary_img, kernel, iterations=1)
  kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
  binary_img = cv.dilate(binary_img, kernel, iterations=1)
  binary_img = cv.morphologyEx(binary_img, cv.MORPH_CLOSE, kernel)

  # Encontrar contornos novamente após as transformações morfológicas
  contours, _ = cv.findContours(binary_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

  # Eliminar contornos pequenos remanescentes
  for cnt in contours:
    area = cv.contourArea(cnt)
    if area < target_area * 0.325:
      x, y, w, h = cv.boundingRect(cnt)
      cv.rectangle(binary_img, (x, y), (x + w, y + h), (0, 0, 0), -1)

  # Dilatar segmentos
  kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
  binary_img = cv.dilate(binary_img, kernel, iterations=1)

  contours, _ = cv.findContours(binary_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

  # Eliminar contornos com aspecto de linhas horizontais
  for cnt in contours:
    x, y, w, h = cv.boundingRect(cnt)
    aspect_ratio = float(w) / h
    if aspect_ratio > h / float(w) * 3:
      cv.rectangle(binary_img, (x, y), (x + w, y + h), (0, 0, 0), -1)

  # Unir os segmentos
  kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 7))
  binary_img = cv.dilate(binary_img, kernel, iterations=1)
  # cv.imshow('Morphed Image', binary_img)

  # Encontrar contornos dos digitos
  contours, _ = cv.findContours(binary_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

  digit_rois = []
  for cnt in contours:
    area = cv.contourArea(cnt)
    x, y, w, h = cv.boundingRect(cnt)
    aspect_ratio = float(w) / h
    if target_area * 0.7 <= area <= target_area * 5 and aspect_ratio < h / float(w):
      digit_rois.append(img[y:y+h, x:x+w])
      # cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
  return digit_rois if digit_rois else None