/*
Description :
자바스크립트에서 음성 파일을 받지 않고
자바스크립트에서는 서버를 싱행하고
서버에서 pyaudio로 stream을 받도록 하는 로직 연구
*/
function startRecording() {
fetch('/start_recording')
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = 'Max Amplitude: ' + data.max_amplitude;
    })
    .catch(error => console.error('Error:', error));
}
