

import torchaudio
from kospeech.models import DeepSpeech2



model = DeepSpeech2(pretrained_model_path='path_to_pretrained_model.pt')
model.eval()


def recognize():

    audio_file = request.files['audio']
    waveform, sample_rate = torchaudio.load(audio_file)
    transcript = model.recognize(waveform, sample_rate)
    
    print("결과::", transcript)


