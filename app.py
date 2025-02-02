from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO, emit
#from API.anne_mng import anne_mng as anne_mng
#from API.bp_blog import bp_blog as bp_blog
#from API.bp_church import bp_church as bp_church
#import API.db_connect as db_connect

app = Flask(__name__)
# debug 모드 설정
app.config['DEBUG'] = True
socketio = SocketIO(app)

#app.register_blueprint(anne_mng, url_prefix='/anne_mng')
#app.register_blueprint(bp_blog, url_prefix='/bp_blog')
#app.register_blueprint(bp_church, url_prefix='/bp_church')

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


@app.route('/get_audio', methods=['POST'])
def get_audio():
    """
     2025.02.02
     클라이언트 음성 파일 처리
     sst / whisper 활용
    """

    audio_file = request.files['audioFile']  # input type="file"의 name과 일치해야 함
    
    frames = process_audio_file(audio_file, 16000)
    return "파일을 받았습니다!"

from pydub import AudioSegment
import numpy as np
def process_audio_file(audio_file, rate):
    """
    2025.02.02
    클라이언트 음성 파일 처리
    """
   
    # 오디오 파일을 AudioSegment 객체로 로드
    audio_segment = AudioSegment.from_file(audio_file)
    
    # 주어진 샘플링 레이트로 오디오를 변환
    audio_segment = audio_segment.set_frame_rate(rate)
    
    # numpy 배열로 데이터 추출
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.int16)
    
    from API.sst.whisper import AudioProcessor
    AudioProcessor.get_client_audio(samples)


from gtts import gTTS
@app.route('/tts')
def tts():
    
    """
    tts
    """
    text = "안녕하세요? 무엇을 도와드릴까요?"
    tts = gTTS(text=text, lang='ko')
    tts.save("hello.mp3")

    print("=====tts=====")

    return send_file("hello.mp3", as_attachment=True)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

from transformers import pipeline
import torch
@socketio.on('audio_data')
def handle_audio(data):
    print("======handle_audio 함수 시작")
    
    audio_data = data['audio']
    
    if len(audio_data) % 2 != 0:
        print("Received audio data length is not a multiple of element size. Adjusting.")
        audio_data = audio_data[:-1]  # 마지막 바이트를 잘라내어 조정

    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    
    audio_float = audio_array.astype(np.float32) / 32768  # -1.0 ~ 1.0 범위로 정규화

    print("======위스퍼 시작")
    # Whisper 모델에 전달
    try:
        # GPU가 사용 가능한지 확인
        if torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        # Whisper 모델 로드
        transcriber = pipeline(model="openai/whisper-small", task="automatic-speech-recognition", device=device)
        result = transcriber({"raw": audio_float, "sampling_rate": 16000})
        if result['text']:
            print("=====클라이언트 음성 결과:", result['text'])

    except Exception as e:
        print(f"Error processing audio: {e}")



############################################################


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
