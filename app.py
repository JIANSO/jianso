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
    import API.module_collection as module
    module.update_json({"data" :  {"auth" : "False"}, "path" : "auth"})

    return render_template("/index.html")

def get_command_by_page(audio_text, curr_page):
    """
    stt 결과 처리
    """

    # {next page : next 페이지로 가게할 명령어}
    # "start_step1" 의 경우.. 생각해 봐야함.
    commands_list = { 
        "manage" :{
            "start_step1"   : ["시작", "서비스해"],
            "end_step1"     : ["종료", "정료", "멈춰", "안해", "끝"],
            "data"          : ["관리", "정보"]
        }
        ,"start_step1" : {
            "start_step2&'활동보조'" : ["보조"]
            ,"start_step2&활동보조 2인이상" : ["2인","이상"]
            ,"start_step2&'방문목욕'" : ["목욕"]
            ,"start_step2&'방문간호'" : ["간호"]
            ,"start_step2&'방문간호지시서'" : ["지시", "지시서"]
            ,"manage" : ["이전", "취소"]
        }
        ,"start_step2" : {"start_step2" : ["확인", "시작", "끝"], "manage" : ["이전", "취소"]}
        ,"end_step1" : {"end_step1" : ["확인", "종료", "정료", "끝"],"manage" : ["이전", "취소"]}
        ,"data" : {"manage" : ["이전", "취소"]}
        
    }
    
    commands = commands_list[curr_page]
    return_result = ''
    found_keyword = None  # 찾은 키워드를 저장하기 위한 변수

    for next_url, keywords in commands.items():
        for keyword in keywords:
            if keyword in audio_text:
                found_keyword = keyword  # 찾은 키워드를 변수에 저장
                return_result = next_url
                break
        if found_keyword:  # 찾은 키워드가 있으면 루프 종료
            break

    #return_result{next : '', user_parameter : ''} 형태 갖추도록 수정하기.
    
    return return_result

@app.route('/start_stt', methods=['GET'])
def start_stt():
    audio_text = sst.audio_stream().sst_module(TRANSCRIBER)
    curr_page = request.args.get('curr_page', 'default_value')
    
    return_result = get_command_by_page(audio_text.replace(" ", ""), curr_page)
    
    return jsonify({"return_result": return_result, "audio_text" : audio_text })

@app.route('/stop_stt')
def stop_stt():
    """
    음성 인식 종료
    """

    sst.audio_stream().stream_stop()

    return jsonify({"return_result": 200})

face_recognition_instance = face_recognition_class()
@app.route('/start_face_recognition')
def start_face_recognition():
    
    return_result = None
    try : 
        return_result = face_recognition_instance.generate_frames()
    except Exception as e:
        print(f"An error occurred: {e}")
     

    return jsonify({"return_result": f"{return_result}" })
    

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
