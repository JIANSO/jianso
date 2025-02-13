import cv2
import face_recognition
import time
"""

얼굴 인증 완성본.
수정 가능.
taya 얼굴은 인식하는데 
내 얼굴은 못함.

return 시 성공, 실패 여부 전달할 예정
tccutil reset Camera
"""
# 기존에 저장된 얼굴 이미지 로드
# 추후 사용자 얼굴 저장
class face_recognition_class :
    def __init__(self):
        try:
            self.known_image = face_recognition.load_image_file("API/recognition/taya.png")
            self.known_face_encoding = face_recognition.face_encodings(self.known_image)[0]
            self.camera = None
        except Exception as e:
            print("오류 발생:", e)


    def start_camera(self):
        # 카메라 설정
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("===카메라를 열 수 없습니다.")
            exit()
        else :
            print("===카메라를 오픈합니다.")

    def stop_camera(self) :
        self.camera.release()
        cv2.destroyAllWindows()
        exit()

    def after_recognition(self, return_result) :
        

        #인증 여부 db 저장하기
        import API.module_collection as module_collection
        module_collection.update_json({"data" :  {"auth" : f"{return_result}"}, "path" : "auth"})
        
    def generate_frames(self):  # 5초 동안 인증 시도
        
        # 카메라 설정
        self.start_camera()
        start_time = time.time()
        attempts = 0
        max_attempts = 5  # 최대 5번 인증 시도

        return_result = False
        
        try:
            while True:
                if time.time() - start_time > 5:
                    print("===인증 시간 초과")
                    break

                if attempts >= max_attempts:
                    print("===최대 인증 시도 횟수 초과 및 종료")
                    break

                success, frame = self.camera.read()
                if not success:
                    print("===카메라에서 프레임을 읽을 수 없습니다.")
                    break

            
                face_locations = face_recognition.face_locations(frame)
               
                if not face_locations:
                    print("===감지된 얼굴 없음")
                    continue  # 얼굴이 감지되지 않으면 다음 프레임 시도

                face_encodings = face_recognition.face_encodings(frame, face_locations)

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces([self.known_face_encoding], face_encoding)
                    if True in matches:
                        print("====인증 성공====")
                        return_result =  True
                        break

                if return_result:
                    break
                
                """
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                """

                attempts += 1  # 인증 시도 횟수 증가

        except Exception as e:
            print(f"===예외 발생: {e}")

        finally:
            self.after_recognition(return_result)
            return return_result
        
        
      