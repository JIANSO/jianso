from flask import Flask, render_template,jsonify, request
from API.get_page import get_page
from API.module_collection import module_collection 
from API.sst import sst

from API.recognition.recognition import face_recognition_class
import torch
from transformers import pipeline
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
    
if torch.backends.mps.is_available():
    device = "mps"  # Apple Metal Performance Shaders

"""
속도 개선
pipeline을 사용하는 경우
whipser를 그대로 불러오는 경우
"""
# Whisper 모델 사전 로드
TRANSCRIBER = pipeline(model="openai/whisper-large-v3-turbo", 
                    task="automatic-speech-recognition", 
                    device=device
                    )

app = Flask(__name__)
app.register_blueprint(get_page, url_prefix='/get_page')
app.register_blueprint(module_collection, url_prefix='/module_collection')
# debug 모드 설정
app.config['DEBUG'] = True

@app.route('/')
def home():
   
    return render_template("/index.html")

@app.route('/start_stt')
def start_stt():
    audio_text = sst.audio_stream().sst_module(TRANSCRIBER)
   
    print("===app.py start_stt===")
     
    return_result = "없음"
    if "시작" in audio_text :
        return_result = "start"
    elif "종료" in audio_text :
        return_result = "end"
    elif "관리" in audio_text :
        return_result = "recognition"
    else :
        return_result = 0
    return jsonify({"return_result": return_result, "audio_text" : audio_text })

@app.route('/stop_stt')
def stop_stt():
    """
    음성 인식 종료
    """
    sst.audio_stream().stream_stop()
    print("===app.py stop_stt===")

    return jsonify({"return_result": 200})

face_recognition_instance = face_recognition_class()
@app.route('/start_face_recognition')
def start_face_recognition():
    
    return_result = None
    
    try : 
        
        return_result = face_recognition_instance.generate_frames()
        print(".......start_face_recognition")
        print(".......start_face_recognition", return_result)

        #json에게.. 결과를 알려줘야 하는데.. 값이 이동을 안하네 ^^;
        return jsonify({"return_result": f"{return_result}" })
    except Exception as e:
        print(f"An error occurred: {e}")
        return_result = None
    

@app.route('/stop_face_recognition')
def stop_face_recognition():
    
    face_recognition_instance.stop_camera()

    return  jsonify({"return_result": 200 })




##########################################################
@app.errorhandler(Exception)
def handle_error(error):
    # 에러 페이지 렌더링
    print(error)
    return render_template('404-v1.html', error=error), 500

import os
if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 8888)
    print("===server start===")
    app.run(host=host, port=int(port), debug=True)
