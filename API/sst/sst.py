from flask import jsonify
import numpy as np
import pyaudio
import webrtcvad

"""
[최종본]

"""


class audio_stream:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000  # 샘플링 레이트 설정
        self.chunk = 320
        self.is_active = False

    def stream_start(self):
        if not self.is_active:
            self.stream = self.audio.open(format=self.format, 
                                          channels=self.channels, 
                                          rate=self.rate, 
                                          input=True, 
                                          frames_per_buffer=self.chunk)
            self.is_active = True
            print("===Stream started.")

    def stream_stop(self):
        if self.is_active:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            self.is_active = False
            print("===Stream stopped.")    

    def sst_module(self, TRANSCRIBER) :
        frame_duration = 20  # 프레임 길이 (ms)
        frame_size = int(self.rate * frame_duration / 1000)  # 프레임 크기 계산
        
        #오디오 스트림 open 시작
        self.stream_start()
        vad = webrtcvad.Vad(3)  # VAD 모드 설정 (0~3, 3이 가장 엄격)

        frames = []
        silence_frames = 0
        speaking_frames = 0
        audio_data_collected = False
        print("========읽기 시작 :: ")
        result_text = ""
        
        try:
            while True:
                frame = self.stream.read(frame_size, exception_on_overflow=False)  # 20 ms의 오디오 프레임 읽기
                is_speech = vad.is_speech(frame, self.rate)  # 현재 프레임에서 음성이 있는지 확인
                frames.append(frame)
                if is_speech:     
                    print("========발화 o :: ", speaking_frames)
                    silence_frames = 0
                    speaking_frames += 1
                    audio_data_collected = True
                else :
                    print("========발화 x :: ", silence_frames)
                    silence_frames += 1
                    if speaking_frames > 10 and audio_data_collected and silence_frames > 50:  # 충분한 양의 음성 데이터 후 1초 이상의 침묵이 있으면 처리 시작
                        print("========출력 시작 :: ")
                        buffer = np.concatenate([np.frombuffer(frame, dtype=np.int16) for frame in frames])  # 프레임들을 하나의 배열로 합침
                        audio_float = buffer.astype(np.float32) / 32768  # 정규화
                        result = TRANSCRIBER({"raw": audio_float, 
                                                "sampling_rate": self.rate, 
                                                "LANGUAGE":"ko"})
                        
                        if result['text']:
                            print("=====STT 결과::", result['text'])
                            result_text = result['text']
                            break
                    elif silence_frames > 200 :            
                        print("=====음성 없음 및 종료::")
                        result_text = "404"
                        break
                    
        
        except Exception as e:
                print(f"Error processing audio: {e}")
                return jsonify({"result": '음성 인식에 실패했습니다.'})
                
        finally :    

            self.stream_stop()

        return result_text
