
import webrtcvad
import pyaudio
import collections

def process_audio():
    audio = pyaudio.PyAudio()
    vad = webrtcvad.Vad(1)  # VAD 모드 설정 (0~3, 여기서는 1을 사용)
    sample_rate = 16000  # 샘플링 레이트
    frame_duration = 20  # 프레임 길이 (ms)
    frame_size = int(sample_rate * frame_duration / 1000)  # 프레임 크기 계산
    padding_duration = 1.0  # 감지할 최소 음성 지속 시간 (초)
    num_padding_frames = int(padding_duration / frame_duration)  # 필요한 패딩 프레임 수
    
    # 큐를 사용하여 음성이 지속되는지 여부를 판단
    ring_buffer = collections.deque(maxlen=num_padding_frames)
    
    # 오디오 스트림 열기
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=frame_size)
    
    print("Listening...")
    while True:
        frame = stream.read(frame_size)
        is_speech = vad.is_speech(frame, sample_rate)

        ring_buffer.append((frame, is_speech))
        
        # 음성이 연속해서 나타나는지 확인
        if len(ring_buffer) == ring_buffer.maxlen:
            num_voiced = len([f for f, speech in ring_buffer if speech])
            if num_voiced > 0.9 * ring_buffer.maxlen:  # 90% 이상이 음성으로 판단된 경우
                print("Detected speech.")
            else:
                print("Silence.")
    
    # 리소스 정리
    stream.stop_stream()
    stream.close()
    audio.terminate()
