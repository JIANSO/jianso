import cv2
import face_recognition
import time
"""

얼굴 인증 완성본.
수정 가능.
taya 얼굴은 인식하는데 
내 얼굴은 못함.

return 시 성공, 실패 여부 전달할 예정

"""
# 기존에 저장된 얼굴 이미지 로드
# 추후 사용자 얼굴 저장


class face_recognition_class :
    def __init__(self):
        self.known_image = face_recognition.load_image_file("API/recognition/taya.png")
        self.known_face_encoding = face_recognition.face_encodings(self.known_image)[0]
        self.camera = None

    def start_camera(self):
        # 카메라 설정
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("===카메라를 열 수 없습니다.")
            exit()
    def stop_camera(self) :
        self.camera.release()
        cv2.destroyAllWindows()
        exit()

    def generate_frames(self, timeout=5):  # 10초 동안 인증 시도
        # 카메라 설정
        self.start_camera()
        
        start_time = time.time()
        attempts = 0
        max_attempts = 5  # 최대 5번 인증 시도

        return_result = False
        while True:
            if time.time() - start_time > timeout:
                print("===인증 시간 초과")
                break
                
            if attempts >= max_attempts:
                print("===최대 인증 시도 횟수 초과 및 종료")
                break

            success, frame = self.camera.read()
            if not success:
                print("===카메라에서 프레임을 읽을 수 없습니다.")
                break

            print("====인증 진행중====")
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([self.known_face_encoding], face_encoding)
                if True in matches:
                    print("====인증 성공====")
                    return_result =  True
                    break

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            attempts += 1  # 인증 시도 횟수 증가


        #인증 여부 db 저장하기
        import API.module_collection as module_collection
        module_collection.update_json({"data" :  {"auth" : "True"}, "path" : "auth"})
        
        print("=====카메라 인증 return_result ::", return_result)
        

        return return_result