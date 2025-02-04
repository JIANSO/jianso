import pyaudio
import numpy as np
import queue
from transformers import pipeline
import webrtcvad
import torch

"""
2025.01.23

1. Whisper 오픈 소스 사용
2. webrtcvad로 2초간 발화 없을 시 오픈소스에서 input모드 정지
3. 큐에 audio_stream, process_audio을 담아 실행
4. 추후 사용자 text를 llm과 연결
5. PyAudio 로 실시간 음성인식. 위스퍼는 원래 mp3를 번역하는 것에 더 특화 되었다고 함.

"""
class AudioProcessor:
    def __init__(self):
        # GPU가 사용 가능한지 확인
        if torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        # Whisper 모델 로드
        self.transcriber = pipeline(model="openai/whisper-large", 
                                    task="automatic-speech-recognition", 
                                    device=device)
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000  # 샘플링 레이트 설정
        self.chunk = 320
        self.record_seconds = 5
        self.audio_queue = queue.Queue()

    def audio_stream(self, q):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        vad = webrtcvad.Vad(1)  # VAD 모드 설정 (0~3, 3이 가장 엄격)
        frames = []
        
        silence_frames = 0
        while True:
            frame = stream.read(self.chunk, exception_on_overflow=False)  # 20 ms의 오디오 프레임 읽기
            is_speech = vad.is_speech(frame, self.rate)  # 현재 프레임에서 음성이 있는지 확인
            frames.append(frame)
            
            if is_speech:
                silence_frames = 0
            else:
            
                if silence_frames > 100:  # ~초간 음성이 없으면 중단
                    # 리소스 정리
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    break
                    
                silence_frames += 1

        q.put(frames)  # 전체 녹음된 프레임을 큐에 추가
        q.put(None)  # 녹음 종료를 알림


    def process_audio(self, q):
        frames = self.audio_queue.get()
        if frames is None:
            return

        buffer = np.concatenate([np.frombuffer(frame, dtype=np.int16) for frame in frames])  # 프레임들을 하나의 배열로 합침
        audio_float = buffer.astype(np.float32) / 32768  # 정규화
        try:
            result = self.transcriber({"raw": audio_float, "sampling_rate": self.rate})
            if result['text']:
                print("=====STT 결과::", result['text'])
        
        except Exception as e:
            print(f"Error processing audio: {e}")


    def get_client_audio(self, audio_float):
        """
        자바스크립트에서 받은 음성 파일 처리
        문제가 생겼다. 매우 느리다.
        TODO 내일 cuda로 다시 돌려보기
        """
        
        try:
            result = self.transcriber({"raw": audio_float, "sampling_rate": self.rate})
            if result['text']:
                print("=====STT 결과:", result['text'])
        
        except Exception as e:
            print(f"Error processing audio: {e}")


    def start_processing(self):
        self.audio_stream()
        self.process_audio()

