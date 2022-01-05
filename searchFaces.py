import cv2 as cv
face_cascade = cv.CascadeClassifier("haar.xml")
while True:
    frame = cv.imread("tolpa-1.jpg")
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for(x, y, width, height) in faces:
        cv.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 2)
    cv.imshow('window', frame)
    key = cv.waitKey()
    if key == 27:
        break
cv.destroyAllWindows()