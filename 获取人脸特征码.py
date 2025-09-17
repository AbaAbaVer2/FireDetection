import cv2 as cv
import face_recognition
import numpy as np

img = cv.imread("./img.jpg")
img1 = cv.imread("./img.jpg")
face_locations = face_recognition.face_locations(img)
print(face_recognition) #(top,right,bottom,left)
#获取人脸特征码
face_encodings = face_recognition.face_encodings(img)[0]
face_encodings1 = face_recognition.face_encodings(img1)[0]
print(face_encodings)
#计算欧式距离
distance = np.linalg.norm(face_encodings-face_encodings1)
print(distance)
threshold = 0.5
if distance <= threshold:
    print("same person")
else:
    print("different person")