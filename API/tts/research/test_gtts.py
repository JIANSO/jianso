from flask import Flask, send_file
from gtts import gTTS

#########################################
# 사용하지 않음 x
# gTTS 테스트용
#########################################
text = "안녕하세요? 무엇을 도와드릴까요?"
tts = gTTS(text=text, lang='ko')
tts.save("hello.mp3")

print("=====tts=====")

  