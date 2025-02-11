function get_inner_page(next, user_parameter=''){
    console.log("====get_inner_page===");

    if(user_parameter == ''){
      url_paramter = 'next='+next;
    }else{
      url_paramter = 'next='+next+'&user_parameter='+user_parameter;
    }
    
    fetch('get_page/get_next_page?'+url_paramter)
    .then(response => response.text())  
    .then(html => {
      //페이지 렌더링
      document.getElementById('inner-content').innerHTML = html;
      //페이지 렌더링 후 후처리
      after_rendering(next);
    })
    .catch(error => console.error('Error loading the page: ', error));
}

function after_rendering(next){
  // TODO: 1초 후 시작
  // TODO: next에 따라서 start_recoding을 하고 안하고 결정하기.
  
  if(next == 'manage'){
    //after_rendering_module.stt.start_stt();
  }else if(next == 'start_step1'){
   //after_rendering_module.stt.start_stt();
    after_rendering_module.active_list();
    
  }else if(next == 'start_step2'){
    after_rendering_module.get_currunt_datetime();
    
  }else if(next == 'end'){
    //after_rendering_module.stt.start_stt();
  }else if(next == 'recognition'){
   //after_rendering_module.face_recognition.start_face_recognition();
  }
}

after_rendering_module = {
  stt : {
   start_stt: function() {
      /*
     실시간 음성 인식
     음성 인식으로 페이지 이동
     */
     console.log("====음성 인식 시작=====")
     //TODO 서버 음성 집어넣기
 
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
   },
   stop_stt: function(){
     fetch('/stop_stt')
     .then(response => response.json())
     .then(data => {
         console.log('===음성 인식 종료 완료===')
     })
     .catch(error => console.error('Error:', error));
   }
  }
  ,face_recognition :{
    camera_stream : function() {
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
   ,start_face_recognition : function(){
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
   ,stop_face_recognition : function() {
     // 카메라 종료, 수정 필요. 컴퓨터 카메라 종료가 되는지 확인해야함
     // ajax로 파이썬 카메라 종료하기
     document.getElementById('video').srcObject.getTracks().forEach(function(track) {
           track.stop();
       });
   }
  }
  , active_list: function() {
    /* 자바스크립트 list active */
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
  , get_currunt_datetime : function(){
    const now = new Date();
    const year = now.getFullYear(); // 연도를 YYYY 형태로 반환
    const month = (now.getMonth() + 1).toString().padStart(2, '0'); // 월을 MM 형태로 반환 (getMonth()는 0부터 시작하므로 1을 더함)
    const day = now.getDate().toString().padStart(2, '0'); // 일을 DD 형태로 반환
    const hours = now.getHours().toString().padStart(2, '0');  // 시간을 두 자리 숫자로 표현
    const minutes = now.getMinutes().toString().padStart(2, '0');  // 분을 두 자리 숫자로 표현
    
    //해당 id에 값 고정
    document.getElementById('service_start_time').innerText = `${hours}:${minutes}`;
    document.getElementById('service_date').innerText =`${year}-${month}-${day}`;
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

function check_service_type(){
  // 서비스 시작 시 서비스 유형 선택
    let service_type = document.querySelector('div[name="service_type"] a.active').innerText;
    if (service_type==undefined){
      alert("서비스 유형을 선택해 주세요");
      return
    }
    get_inner_page('start_step2', user_parameter=service_type);
  }

  function confirm_service_start(){
    /* 
    서비스 최종 시작 
    post 방식으로 데이터 보내기
    */
    data = {}
    fetch('/confirm_service_start', {  // POST 요청을 보낼 서버의 엔드포인트
        method: 'POST',   // HTTP 메소드
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) 
    })
    .then(response => response.json())  
    .then(data => {
        // 데이터 렌더링예정
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    
  }
