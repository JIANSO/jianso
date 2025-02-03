from flask import Flask, render_template, send_file, request, jsonify
from flask_socketio import SocketIO, emit

from pydub import AudioSegment
import numpy as np
from gtts import gTTS

import pyaudio
import webrtcvad
from transformers import pipeline, WhisperForConditionalGeneration, WhisperTokenizer
import torch
import collections
#from API.anne_mng import anne_mng as anne_mng
#from API.bp_blog import bp_blog as bp_blog
#from API.bp_church import bp_church as bp_church
#import API.db_connect as db_connect

app = Flask(__name__)
# debug 모드 설정
app.config['DEBUG'] = True
socketio = SocketIO(app)

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
# Whisper 모델 로드
TRANSCRIBER = pipeline(model="openai/whisper-medium", 
                    task="automatic-speech-recognition", 
                    device=device)
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

############################################################
# stt 음성 file 처리
#
############################################################
@app.route('/get_audio', methods=['POST'])
def get_audio():
    """
     2025.02.02
     클라이언트 음성 파일 처리
     sst / whisper 활용
    """

    audio_file = request.files['audioFile']  # input type="file"의 name과 일치해야 함
    
    # 오디오 파일을 AudioSegment 객체로 로드
    audio_segment = AudioSegment.from_file(audio_file)
    
    # 주어진 샘플링 레이트로 오디오를 변환
    audio_segment = audio_segment.set_frame_rate(16000)
    
    # numpy 배열로 데이터 추출
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.int16)
    
    audio_float = samples.astype(np.float32) / 32768  # 정규화
    
    from API.sst.whisper import AudioProcessor
    
    AudioProcessor.get_client_audio(audio_float)
    
    return "파일을 받았습니다!"

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

############################################################
# socketio
#
############################################################

############################################################
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # 샘플링 레이트 설정
CHUNK = 320
RECORD_SECONDS = 5
"""
하드웨어 업그레이드: GPU를 사용하여 모델의 추론 속도를 높일 수 있습니다. 
GPU는 병렬 처리에 최적화되어 있어 더 빠른 성능을 제공합니다.

모델 크기 조정: openai/whisper-large 대신 
openai/whisper-medium이나 openai/whisper-small 모델을 사용할 수 있습니다. 
이 모델들은 크기가 작아 속도가 더 빠를 수 있지만, 
정확도는 다소 낮을 수 있습니다.

배치 처리: 여러 오디오 파일을 한 번에 처리하는 방식으로 
구현하면 전체 처리 시간을 단축할 수 있습니다. 
배치 처리는 I/O 대기 시간과 모델 로딩 시간을 줄여줍니다.

최적화된 설정 사용: 모델 호출 시에 최적화된 파
라미터 설정을 사용하여 처리 속도를 개선할 수 있습니다. 
예를 들어, num_beams나 early_stopping 같은 추론 파라미터를 조절하여 더 빠른 결과를 얻을 수 있습니다.
"""
@app.route('/start_recording')
def start_recording():
    
    frame_duration = 20  # 프레임 길이 (ms)
    frame_size = int(RATE * frame_duration / 1000)  # 프레임 크기 계산
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, 
                        channels=CHANNELS, 
                        rate=RATE, 
                        input=True, 
                        frames_per_buffer=frame_size)
    vad = webrtcvad.Vad(2)  # VAD 모드 설정 (0~3, 3이 가장 엄격)

    frames = []
    silence_frames = 0
    audio_data_collected = False
    print("========읽기 시작 :: ")
    try:
        while True:
            frame = stream.read(frame_size, exception_on_overflow=False)  # 20 ms의 오디오 프레임 읽기
            is_speech = vad.is_speech(frame, RATE)  # 현재 프레임에서 음성이 있는지 확인
            frames.append(frame)
            if is_speech:     
                print("========읽기 시작 :: ")
                silence_frames = 0
                audio_data_collected = True
            else :
                silence_frames += 1
                if audio_data_collected and silence_frames > 50:  # 충분한 양의 음성 데이터 후 1초 이상의 침묵이 있으면 처리 시작
                    print("========출력 시작 :: ")
                    buffer = np.concatenate([np.frombuffer(frame, dtype=np.int16) for frame in frames])  # 프레임들을 하나의 배열로 합침
                    audio_float = buffer.astype(np.float32) / 32768  # 정규화
                    result = TRANSCRIBER({"raw": audio_float, 
                                            "sampling_rate": RATE})
                    
                    if result['text']:
                        print("=====STT 결과::", result['text'])
                        break
                    
        
        """
        buffer = np.concatenate([np.frombuffer(frame, dtype=np.int16) for frame in frames])  # 프레임들을 하나의 배열로 합침
        audio_float = buffer.astype(np.float32) / 32768  # 정규화
        
        try:
            result = TRANSCRIBER({"raw": audio_float, 
                                "sampling_rate": RATE})
                                
            if result['text']:
                print("=====STT 결과::", result['text'])
        
        except Exception as e:
            print(f"Error processing audio: {e}")
        """
    finally :    

        stream.stop_stream()
        stream.close()
        audio.terminate()

    return jsonify({"result": result['text']})

@app.route('/start_recording_prev')
def start_recording_prev():
    """
    정신이 없지만 잘 따라갈 수 있길 ㅠㅠ 
    """
    print("=====서버 측 실시간 pyauido 실행 ")
    frame_duration = 20  # 프레임 길이 (ms)
    frame_size = int(RATE * frame_duration / 1000)  # 프레임 크기 계산
    padding_duration = 1.0  # 감지할 최소 음성 지속 시간 (초)
    num_padding_frames = int(padding_duration / frame_duration)  # 필요한 패딩 프레임 수
    
    ring_buffer = collections.deque(maxlen=num_padding_frames)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, 
                        channels=CHANNELS, 
                        rate=RATE, 
                        input=True, 
                        frames_per_buffer=CHUNK)
    vad = webrtcvad.Vad(0)  # VAD 모드 설정 (0~3, 3이 가장 엄격)
    frames = []
    
    silence_frames = 0
    while True:
        frame = stream.read(CHUNK, exception_on_overflow=False)  # 20 ms의 오디오 프레임 읽기
        is_speech = vad.is_speech(frame, RATE)  # 현재 프레임에서 음성이 있는지 확인
        
        ring_buffer.append((frame, is_speech))
        
        # 음성이 연속해서 나타나는지 확인
        if len(ring_buffer) == ring_buffer.maxlen:
            num_voiced = len([f for f, speech in ring_buffer if speech])
            if num_voiced > 0.9 * ring_buffer.maxlen:  # 90% 이상이 음성으로 판단된 경우
                print("Detected speech.")
            else:
                print("Silence.")
                break

        """
        frames.append(frame)

        if is_speech:
            print("=======발화 있음 :: ")
            silence_frames = 0
        else:
            print("=======발화 없음 :: ")
            if silence_frames > 100:  # ~초간 음성이 없으면 중단
                # 리소스 정리
                stream.stop_stream()
                stream.close()
                audio.terminate()
                break
                
            silence_frames += 1
        
        """
        
    stream.stop_stream()
    stream.close()
    audio.terminate()

    buffer = np.concatenate([np.frombuffer(frame, dtype=np.int16) for frame in frames])  # 프레임들을 하나의 배열로 합침
    audio_float = buffer.astype(np.float32) / 32768  # 정규화
    
    try:
        # GPU가 사용 가능한지 확인
        if torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        # Whisper 모델 로드
        transcriber = pipeline(model="openai/whisper-large", 
                               task="automatic-speech-recognition", 
                               device=device)
        
        result = transcriber({"raw": audio_float, 
                              "sampling_rate": 16000},
                              options={"language": 'ko', 
                                       "output_attentions": False}
                              )
        if result['text']:
            print("=====STT 결과::", result['text'])
    
    except Exception as e:
        print(f"Error processing audio: {e}")
    
    # 데이터 분석 또는 처리 로직
    # 예시: 최대 진폭 계산
    
    stream.stop_stream()
    stream.close()
   
    
    return jsonify({"max_amplitude": 0})

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
