import os
import sys
import urllib.request
import io
from pydub import AudioSegment
from pydub.playback import play
#########################################
# 사용하지 않음 x
# 네이버 클로바 코드 확인용
#########################################

client_id = "ncp_iam_BPAMKR3yYjST7PwLBOa8"
client_secret = "ncp_iam_BPKMKRaErbi7dwoQ2u3Nyy4up04Y0w0GKL"

encText = urllib.parse.quote("반갑습니다 테스트 화면입니다.")
data = "speaker=nara&volume=0&speed=0&pitch=0&format=mp3&text=" + encText;
url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
request = urllib.request.Request(url)
request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
request.add_header("X-NCP-APIGW-API-KEY",client_secret)
response = urllib.request.urlopen(request, data=data.encode('utf-8'))
rescode = response.getcode()

if(rescode==200):
    print("TTS mp3 저장")
    """
    response_body = response.read()
    with open('1111.mp3', 'wb') as f:
        f.write(response_body)
    """
    # 메모리에서 직접 오디오 데이터를 재생
    audio_data = io.BytesIO(response.content)
    song = AudioSegment.from_file(audio_data, format="mp3")
    play(song)
else:
    print("Error Code:" + rescode)