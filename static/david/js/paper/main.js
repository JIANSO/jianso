function get_inner_page(next, user_paramter=''){
    console.log("====get_inner_page===");

    if(user_paramter!= ''){
      url_paramter= 'next='+next;
    }else{
      url_paramter= 'next='+next+'&user_paramter='+user_paramter;
    }
    
    fetch('get_page/get_next_page?'+url_paramter)
    .then(response => response.text())  
    .then(html => {
      //페이지 렌더링
      document.getElementById('inner-content').innerHTML = html;
      
      //페이지 렌더링 후 후처리
      after_page_rendering(next);
    })
    .catch(error => console.error('Error loading the page: ', error));
}

function after_page_rendering(){
  // TODO: 1초 후 시작
  // TODO: next에 따라서 start_recoding을 하고 안하고 결정하기.
  
  if(next == 'manage'){
    start_stt();
  }else if(next == 'start'){
    start_stt();
  }else if(next == 'start_check'){
    active_list();
  }else if(next == 'end'){
    start_stt();
  }else if(next == 'recognition'){
    camera_stream();
  }
}

function get_prev_page(prev, curr){
  //이전으로 돌아가기 
  console.log("====get_prev_page===")

  fetch('get_page/get_prev_page?prev='+prev)
  .then(response => response.text())  
  .then(html => {
    document.getElementById('inner-content').innerHTML = html;
    // 이전으로 돌아가기 후처리
    // 음성 종료, 재시작 예정
    // 카메라 종료 
    if(curr == 'recognition'){
      stop_face_recognition();
    }
    
  })
  .catch(error => console.error('Error loading the page: ', error));
}

function start_stt(){
  /*
  실시간 음성 인식
  음성 인식으로 페이지 이동
  */
  console.log("====음성 인식 시작=====")
  fetch('/start_stt')
  .then(response => response.json())
  .then(data => {
      alert('페이지:: ' + data.return_result + '\n사용자 음성:: ' + data.audio_text);

      // llm 통과 후 다음 페이지 넘어갈 예정
      // 서버에서 처리 후 1,2,3 에 따라 페이지 넘길 예정 
      if(data.return_result !== 0){
        stop_stt();
        get_inner_page(data.return_result);

      }
  })
  .catch(error => console.error('Error:', error));
}

function stop_stt(){
  fetch('/stop_stt')
  .then(response => response.json())
  .then(data => {
      console.log('===음성 인식 종료 완료===')
  })
  .catch(error => console.error('Error:', error));
}

function camera_stream(){
  /*
  자바스크립트 화면 카메라 반사
  */
  
  let video = document.getElementById('video');
  
  if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
          video.srcObject = stream;
          start_face_recognition();
      })
      .catch(function(error) {
          console.error("===카메라 접근에 실패했습니다:", error);
      });
  } else {
      alert('===getUserMedia를 지원하지 않는 브라우저입니다.');
  }
}

function start_face_recognition(){
  /*
  파이썬 cv2 얼굴 인증
  */
  console.log("====camera_recognition=====")
  fetch('/start_face_recognition')
  .then(response => response.json())
  .then(data => {
      alert('결과:: ' + data.return_result);

      stop_face_recognition();
  })
  .catch(error => console.error('Error:', error));
}

// 카메라 종료, 수정 필요. 컴퓨터 카메라 종료가 되는지 확인해야함
function stop_face_recognition() {
  // ajax로 파이썬 카메라 종료하기
  document.getElementById('video').srcObject.getTracks().forEach(function(track) {
        track.stop();
    });
 
}

function check_service_type(){
    let service_type = document.querySelector('div[name="service_type"] a.active').innerText;
    if (service_type==undefined){
      alert("서비스 유형을 선택해 주세요");
      return
    }

    get_inner_page('start_check', user_parameter=service_type);
  }

  function active_list(){
    let listGroup = document.querySelector('.list-group');
    
    listGroup.addEventListener('click', function(event) {
        if (event.target.tagName === 'A') {
            // 모든 'a' 태그에서 'active' 클래스 제거
            const items = listGroup.querySelectorAll('.list-group-item');
            items.forEach(item => {
                item.classList.remove('active');
            });

            // 클릭된 'a' 태그에만 'active' 클래스 추가
            event.target.classList.add('active');
        }
    });
  }