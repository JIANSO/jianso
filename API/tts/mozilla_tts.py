import torch
from TTS.utils.io import load_config
from TTS.utils.audio import AudioProcessor
from TTS.models.tacotron2 import Tacotron2
from TTS.vocoder.utils.generic_utils import setup_generator
from TTS.utils.synthesizer import Synthesizer

# 모델 및 설정 로드
MODEL_PATH = "path_to_your_model.pth"
CONFIG_PATH = "path_to_your_config.json"
CONFIG = load_config(CONFIG_PATH)
audio_processor = AudioProcessor(**CONFIG.audio)

# 모델 설정
model = Tacotron2(CONFIG.audio)
cp = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
model.load_state_dict(cp['model'])
model.eval()

# 음성 합성
synthesizer = Synthesizer(model, audio_processor, None)
wav = synthesizer.tts("안녕하세요, 이것은 예제 음성입니다.")

# 결과 저장
audio_processor.save_wav(wav, "output_audio.wav")