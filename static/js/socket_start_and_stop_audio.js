<script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
/*
자바스크립트에서 웹 소켓으로 실시간으로 사용자 음성을 수집하여 
클라이언트 종료 버튼을 누르면 음성을 보내는 기술 연구
*/
    document.addEventListener('DOMContentLoaded', function () {
        var socket = io(); // 서버와의 Socket.IO 연결 초기화

        let mediaRecorder;
        let audioChunks = [];

        async function startRecording() {
          /*
           - recording 버튼 클릭 시 음성 수집
           - 한국어가 깨지는 문제가 있다.
          */
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = function (event) {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = function () {
                  const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                  const reader = new FileReader();
                  reader.onload = function () {
                      const buffer = this.result;
                      const bufferLength = buffer.byteLength;
                      const remainder = bufferLength % 2;
                      if (remainder !== 0) {
                          console.warn("The buffer length is not aligned. Adjusting the length.");
                      }
                      const alignedBuffer = buffer.slice(0, bufferLength - remainder);
                      
                      socket.emit('audio_data', { audio: alignedBuffer });
                  };
                  reader.readAsArrayBuffer(audioBlob);
              };

                mediaRecorder.start();
            } catch (error) {
                console.error('Error accessing audio devices.', error);
            }
        }

        function stopRecording() {
            if (mediaRecorder) {
                mediaRecorder.stop(); // Triggers the 'onstop' event
            }
        }

        // Start and stop recording buttons
        document.getElementById('start').addEventListener('click', startRecording);
        document.getElementById('stop').addEventListener('click', stopRecording);
    });
