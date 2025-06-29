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
  binary_img = getBinaryImage(img, (3, 3))
  # Encontrar contornos na imagem binarizada
  contours, _ = cv.findContours(binary_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  # Retornar o maior contorno encontrado
  if contours:
    cnt = max(contours, key=cv.contourArea)
    x, y, w, h = cv.boundingRect(cnt)
    return img[y:y+h, x:x+w], w, h
  return None

def getDisplayContour(img, target_area):
  # Obter a imagem binarizada
  binary_img = getBinaryImage(img, (3, 3))
  # Encontrar contornos na imagem binarizada
  contours, _ = cv.findContours(binary_img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

  for cnt in contours:
    area = cv.contourArea(cnt)
    if target_area * 0.3 <= area <= target_area * 1.5:
      # Aproximar o contorno para reduzir o número de pontos
      epsilon = 0.02 * cv.arcLength(cnt, True)
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
            return img[y + int(y * 0.05):y+h - int(h * 0.05), x + int(x * 0.5):x+w - int(w * 0.05)], w, h
  return None

def getSegmentContour(img, target_area):
  # Obter a imagem binarizada
  binary_img = getBinaryImage(img, (3, 3))
  # Encontrar contornos na imagem binarizada
  contours, _ = cv.findContours(binary_img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

  segments = []
  for cnt in contours:
    area = cv.contourArea(cnt)
    _, _, w, h, = cv.boundingRect(cnt)
    aspect_ratio = float(w) / h
    if target_area * 0.01 <= area <= target_area * 10 and 0.2 <= aspect_ratio <= 3:
      cv.drawContours(img, [cnt], -1, (0, 255, 0), 2)
      # Aproximar o contorno para reduzir o número de pontos
      epsilon = 0.02 * cv.arcLength(cnt, True)
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
            # cv.drawContours(img, [cnt], -1, (0, 255, 0), 2)
            segments.append(img[y:y+h, x:x+w])
  return segments if segments else None