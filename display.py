import cv2 as cv
import numpy as np
import binarizar

img_dir = binarizar.img_dir
img = binarizar.img
binary_img = binarizar.thresh

# Filtrar contornos através de uma aréa mínima para evitar pequenos ruídos
target_area = 162 * 97 # Número literal. Valores mais adequados precisam ser encontrados.
for cnt in binarizar.contours:
  area = cv.contourArea(cnt)
  # Verifica se a area do contorno está dentro das tolerâncias
  if area > target_area * 0.7 and area < target_area * 1.3:
      # Tenta aproximar o perimetro do contorno a um retângulo
      perimeter = cv.arcLength(cnt, True)
      approx = cv.approxPolyDP(cnt, 0.02 * perimeter, True)

      # Verifica se o contorno aproximado possui 
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
            cv.drawContours(img, [cnt], 0, (0, 255, 0), 3)

cv.imshow("Imagem binarizada", binary_img)
cv.imshow("Imagem com contorno", img)
k = cv.waitKey(0)

if chr(k) == 's':
  path = f'{img_dir}\\multimetro_demarcado.jpg'
  cv.imwrite(f'{img_dir}\\multimetro_demarcado.jpg', img)
  print(f'Imagem guardada em: {path}'.replace('.\\', ''))