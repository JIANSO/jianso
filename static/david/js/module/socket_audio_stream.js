<script src="https://cdn.socket.io/socket.io-3.1.3.js"></script>
document.addEventListener('DOMContentLoaded', function () {
/*
자바스크립트에서 웹 소켓으로 실시간으로 사용자 음성을 수집하여 
1초 마다 서버로 음성을 보내는 기술 연구
*/
var socket = io.connect('http://localhost:5000');

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = function (e) {
            if (e.data.size > 0) {
                socket.emit('audio_data', { audio: e.data });
            }
        };
        mediaRecorder.start(1000);  // 매 1000ms마다 오디오 데이터 전송
    })
    .catch(error => console.error('Error accessing audio devices.', error));
});