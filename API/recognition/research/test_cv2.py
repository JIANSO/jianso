import cv2
#########################################
# shell에서 직접 실행 / 사용하지 않음
#########################################


# 얼굴 인식을 위한 Haar 캐스케이드 로드
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print("====cv2_simple====")
# 이미지 불러오기
img = cv2.imread('taya.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 얼굴 감지
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# 감지된 얼굴에 사각형 그리기
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

# 결과 이미지 표시
cv2.imshow('img', img)

# 'q' 키를 누를 때까지 기다리기
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print("====cv2_simple.finish====")