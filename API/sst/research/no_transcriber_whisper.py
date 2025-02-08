import numpy as np
import pyaudio
import webrtcvad
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
import io
from pydub import AudioSegment
import torchaudio

# 모델 및 프로세서 로드
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3-turbo")

if torch.cuda.is_available():
    model = model.cuda()

# 오디오 설정
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
frame_duration = 20  # 20ms
frame_size = int(RATE * frame_duration / 1000)


def transcribe(audio_buffer):
    # 오디오 버퍼를 오디오 세그먼트로 변환
    audio_segment = AudioSegment(
        data=audio_buffer,
        sample_width=2,  # pyaudio.paInt16 == 2 bytes
        frame_rate=RATE,
        channels=1
    )
    
    # 오디오 파일로 저장
    file_buffer = io.BytesIO()
    audio_segment.export(file_buffer, format="wav")
    file_buffer.seek(0)

    # torchaudio를 사용하여 오디오 파일에서 tensor로 음성 데이터 추출
    waveform, sample_rate = torchaudio.load(file_buffer)

    # 바이너리 데이터를 프로세서에 전달
    inputs = processor(waveform.squeeze(0), sampling_rate=RATE, return_tensors="pt", language="ko")
    input_features = inputs.input_features

    generated_ids = model.generate(inputs=input_features)
    transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print("=====변환 음성", transcription)
    
    file_buffer.close()
    
    return transcription

def sst_module () :
    # PyAudio 스트림 설정
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, 
                    channels=CHANNELS, 
                    rate=RATE, 
                    input=True, 
                    frames_per_buffer=frame_size)
    vad = webrtcvad.Vad(3)

    try:
        frames = []
        speaking_frames = 0
        silence_frames = 0
        audio_data_collected = False
        result_text = ""
        while True:
            frame = stream.read(frame_size, exception_on_overflow=False)
            if vad.is_speech(frame, RATE):
                frames.append(frame)
                speaking_frames += 1
                silence_frames = 0
                audio_data_collected = True
                print("========발화 o :: ", speaking_frames)

            else:
                silence_frames += 1
                print("========발화 x :: ", silence_frames)
                
                if speaking_frames > 0 and audio_data_collected and silence_frames > 15:
                    audio_buffer = b''.join(frames)
                    transcription = transcribe(audio_buffer)
                    result_text = transcription
                    break

                if silence_frames > 100:
                    print("=====음성 없음 및 종료::")
                    result_text = "음성 없음 및 종료"
                    break

    except Exception as e:
            print(f"Error processing audio: {e}")
            result_text = "음성 인식 실패"
            
    finally :    

        stream.stop_stream()
        stream.close()
        audio.terminate()

    return result_text
