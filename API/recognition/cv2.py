from flask import Flask, render_template, Response
import cv2
import face_recognition

app = Flask(__name__)

# 기존에 저장된 얼굴 이미지 로드
known_image = face_recognition.load_image_file("known_face.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# 카메라 설정
camera = cv2.VideoCapture(0)  # 0은 기본 카메라

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # 얼굴 인식 로직
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
                if True in matches:
                    # 인증 성공
                    return render_template('next_page.html')

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
