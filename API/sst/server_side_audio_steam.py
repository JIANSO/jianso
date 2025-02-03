"""
Description :
자바스크립트에서 음성 파일을 받지 않고
자바스크립트에서는 서버를 싱행하고
서버에서 pyaudio로 stream을 받도록 하는 로직 연구
"""

@app.route('/start_recording')
def start_recording():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    
    for i in range(0, int(44100 / 1024 * 5)):  # 5초간 녹음
        data = stream.read(1024)
        frames.append(np.fromstring(data, dtype=np.int16))
    
    np_frames = np.hstack(frames)
    
    # 데이터 분석 또는 처리 로직
    # 예시: 최대 진폭 계산
    max_amplitude = np.max(np_frames)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return jsonify({"max_amplitude": int(max_amplitude)})