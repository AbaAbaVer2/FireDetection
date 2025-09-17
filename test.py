import cv2 as cv
import face_recognition

img = cv.imread("./img.jpg")
face_locations = face_recognition.face_locations(img)
print(face_recognition) #(top,right,bottom,left)
#画出人脸区域
for (top,right,bottom,left) in face_locations:
    cv.rectangle(img,(left,top),(right,bottom),(0,255,0),2)
cv.imshow("img",img)
cv.waitKey(0)
cv.destroyAllWindows()