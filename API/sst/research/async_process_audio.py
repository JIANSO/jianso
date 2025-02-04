import asyncio
import numpy as np
import pyaudio
from concurrent.futures import ThreadPoolExecutor
import webrtcvad
from transformers import pipeline
import torch

# Whisper 모델 로드
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

TRANSCRIBER = pipeline(model="openai/whisper-medium", 
                       task="automatic-speech-recognition", 
                       device=device
                       )

# 오디오 설정 변수
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = int(RATE / 50)  # 20ms

def capture_audio(queue):
    print("==============capture_audio=====================")
    """오디오 데이터를 계속 캡처하고 큐에 저장하는 함수"""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

    while True:
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        queue.append(data)
      
        if  (len(queue) > 500 ) :  # 버퍼 크기 제한
           
            queue.pop(0)

async def process_audio(executor, queue):
    print("==============process_audio=====================")
    """비동기로 오디오 데이터를 처리하는 함수"""
    
    while True:
        if len(queue) > 100:  # 충분한 데이터가 쌓이면 처리 시작
            # 큐에서 오디오 데이터 가져오기
            audio_data = b''.join(queue)
            buffer = np.frombuffer(audio_data, dtype=np.int16)  # 프레임들을 하나의 배열로 합침
            audio_float = buffer.astype(np.float32) / 32768  # 정규화
            
            # 비동기 실행을 위해 Executor 사용
            result = await loop.run_in_executor(executor, transcribe_audio, audio_float, RATE)
            
            print("======음성 인식 결과:", result['text'])
            queue.clear()  # 처리 후 큐 비우기

def transcribe_audio(audio_float, rate):
    print("==============transcribe_audio=====================")
    """오디오 데이터를 텍스트로 변환하는 함수"""
    result = TRANSCRIBER({"raw": audio_float, "sampling_rate": rate, "language":"ko"})
    return result

async def main():
    queue = []
    executor = ThreadPoolExecutor(max_workers=2)
    
    # 오디오 캡처 작업 시작
    capture_task = loop.run_in_executor(executor, capture_audio, queue)
    
    # 오디오 처리 작업 시작
    await process_audio(executor, queue)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
