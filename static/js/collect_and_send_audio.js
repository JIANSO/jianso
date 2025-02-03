async function collectAndSendAudio() {
/*
음성을 모아서 파이썬 서버에 전송하는 기술

*/

    let url = '/get_audio'
    
    const mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(mediaStream);
    const audioChunks = [];

    recorder.ondataavailable = function(event) {
      audioChunks.push(event.data);
    };

    recorder.onstop = async function() {
      console.log("=====자바스크립트 함수 테스트중::")
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('audioFile', audioBlob);

      try {
        const response = await fetch(url, {
          method: 'POST',
          body: formData
        });
        console.log('Audio sent successfully:', await response.text());
      } catch (error) {
        console.error('Failed to send audio:', error);
      }
    };

    recorder.start();

    // 예를 들어 녹음을 5초 후에 멈추고자 할 경우
    setTimeout(() => {
      recorder.stop();
    }, 3000);
}