import pyaudio
import numpy as np
import torch
import speechbrain as sb
from speechbrain.pretrained import EncoderDecoderASR

# SpeechBrain 모델 로드
asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="pretrained_models/asr-crdnn-rnnlm-librispeech")

# PyAudio 설정
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

print("Recording...")
"""

사용자로부터 2초간 음성이 없을 때까지
음성을 받아서 저장한 다음 텍스트로 출력 수정 예정.
"""
# 실시간으로 오디오 스트림 처리
try:
    while True:
        data = stream.read(1024, exception_on_overflow=False)
        waveform = np.frombuffer(data, dtype=np.int16).copy()  # 복사본 생성
        waveform = torch.from_numpy(waveform).float() / 32768.0  # 정규화
        waveform = waveform.unsqueeze(0)  # 배치 차원 추가
        if waveform.shape[1] == 0:
            continue
        wav_lens = torch.tensor([waveform.shape[1] / 16000.0])  # 오디오 길이 계산
        transcription = asr_model.transcribe_batch(waveform, wav_lens)
        print("Transcription:", transcription)
except KeyboardInterrupt:
    print("Finished recording.")

# 스트림 종료
stream.stop_stream()
stream.close()
p.terminate()
