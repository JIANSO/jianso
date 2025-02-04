from flask import Flask, render_template, Blueprint, request, jsonify
app_stt = Blueprint('app_stt', __name__)


from pydub import AudioSegment
import numpy as np
import pyaudio
import webrtcvad
from transformers import pipeline
import torch
import collections

@app_stt.route('/')
def home():
    
    return ""

############################################################
# stt 음성 file 처리
#
############################################################
@app_stt.route('/get_audio', methods=['POST'])
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
    
    from API.sst.research.whisper import AudioProcessor
    
    AudioProcessor.get_client_audio(audio_float)
    
    return "파일을 받았습니다!"


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # 샘플링 레이트 설정
CHUNK = 320
RECORD_SECONDS = 5
@app_stt.route('/start_recording_prev')
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