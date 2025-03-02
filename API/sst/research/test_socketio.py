#########################################
# 사용하지 않음 x
# 실시간 Client, Server 소켓 통신 테스트
#########################################

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
    
    audio_data = data['audio']
    
    if len(audio_data) % 2 != 0:
        print("Received audio data length is not a multiple of element size. Adjusting.")
        audio_data = audio_data[:-1]  # 마지막 바이트를 잘라내어 조정

    audio_array = np.frombuffer(audio_data, dtype=np.int16) 
    audio_float = audio_array.astype(np.float32) / 32768  # -1.0 ~ 1.0 범위로 정규화

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
