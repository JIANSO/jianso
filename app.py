from flask import Flask, render_template,jsonify
from API.get_page import get_page
from API.sst import sst
from API.sst.research import no_transcriber_whisper
import torch
from transformers import pipeline

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
"""
속도 개선
pipeline을 사용하는 경우
whipser를 그대로 불러오는 경우
"""
print("device ::", device)
# Whisper 모델 로드
TRANSCRIBER = pipeline(model="openai/whisper-medium", 
                    task="automatic-speech-recognition", 
                    device=device
                    )

app = Flask(__name__)
app.register_blueprint(get_page, url_prefix='/get_page')

# debug 모드 설정
app.config['DEBUG'] = True


@app.route('/')
def home():
    """
    connection = db_connect.get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT VERSION()"
        cursor.execute(sql)
        result = cursor.fetchall() 
        print("=======Successfully connected to MySQL :: ", result)
        
        cursor.close()
        connection.close()
        """
    
    return render_template("/index.html")

@app.route('/start_recording')
def start_recording():
    

    #audio_text = sst.sst_module(TRANSCRIBER)
    #아래 함수 속도 때문에 테스트 중
    print("===app.py start_recording===")
    audio_text = no_transcriber_whisper.sst_module()
    return_result = "없음"

    if "시작" in audio_text :
        return_result = "시작"
    elif "종료" in audio_text :
        return_result = "종료"
    elif "관리" in audio_text :
        return_result = "관리"
    else :
        return_result = "없음"


    return jsonify({"return_result": return_result, "audio_text" : audio_text })

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
