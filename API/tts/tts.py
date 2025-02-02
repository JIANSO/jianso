from TTS.utils.synthesizer import Synthesizer

synthesizer = Synthesizer(model_name="tts_models/en/ljspeech/tacotron2-DDC")
wav = synthesizer.tts("Your text goes here")

#synthesizer.save_wav(wav, "output.wav")

import sounddevice as sd

# 오디오 재생 함수
def play_audio(audio_array, samplerate=22050):
    sd.play(audio_array, samplerate)
    sd.wait()  # 재생이 끝날 때까지 기다림

# TensorFlow TTS로부터 오디오 데이터 사용
# 예를 들어, 위에서 생성한 `audio` 배열을 사용할 수 있습니다.
play_audio(wav, 22050)