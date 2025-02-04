from google.cloud import speech

client = speech.SpeechClient()
"""
#특징

인증키 필요.
유료.
"""
audio = speech.RecognitionAudio(uri="gs://YOUR_BUCKET/YOUR_FILE.wav")

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="ko-KR"
)

response = client.recognize(config=config, audio=audio)

for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))
