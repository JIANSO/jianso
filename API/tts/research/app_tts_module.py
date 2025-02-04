from flask import Flask, render_template, Blueprint, current_app, request, send_file
app_tts = Blueprint('app_tts', __name__)

from gtts import gTTS

@app_tts.route('/')
def home():   
    
    return ""

@app_tts.route('/tts')
def tts():
    
    """
    tts
    """
    text = "안녕하세요? 무엇을 도와드릴까요?"
    tts = gTTS(text=text, lang='ko')
    tts.save("hello.mp3")

    print("=====tts=====")

    return send_file("hello.mp3", as_attachment=True)