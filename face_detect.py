import cv2

# Полный профиль лица не находит, нужен полупрофиль, часто пересекается с анфасом ((

# obj = 'haarcascade_profileface.xml'
obj = 'haarcascade_frontalface_default.xml'
face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades + obj)

img = cv2.imread("1.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade_db. \
    detectMultiScale(img, 1.1, 19)
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y),
                  (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('rez', img)
cv2.waitKey()

print(len(faces))
