function get_inner_page(next, user_parameter=''){

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

function after_rendering(curr){
  
  if(curr == 'first_gate'){
    /* 모든 파이썬 라이브러리 종료 */
    after_rendering_module.stt.stop_stt(curr);
    after_rendering_module.face_recognition.stop_face_recognition();
  }else if(curr == 'manage'){
    after_rendering_module.stt.start_stt(curr);
  }else if(curr == 'start_step1'){
    after_rendering_module.stt.start_stt(curr);
    after_rendering_module.active_list();
  }else if(curr == 'start_step2'){
    after_rendering_module.stt.start_stt(curr);
    after_rendering_module.get_currunt_datetime('service_start_time');
  }else if(curr == 'end_step1'){
    after_rendering_module.stt.start_stt(curr);
    after_rendering_module.get_currunt_service_info(function(data){
      document.getElementById('service_status').innerText = data['service_status'];
      document.getElementById('service_type').innerText = data['service_type'];
      document.getElementById('service_start_time').innerText = data['service_start_time'];
      
      after_rendering_module.get_currunt_datetime('service_end_time');
    });
  }else if(curr == 'recognition'){
    after_rendering_module.face_recognition.start_face_recognition()
  }else if(curr == 'data'){
    /* 서비스 관리 */
    after_rendering_module.get_currunt_service_info(function(data){
      document.getElementById('service_status').innerText = data['service_status'];
      document.getElementById('service_type').innerText = data['service_type'];
      document.getElementById('service_start_time').innerText = data['service_start_time'];
      document.getElementById('service_end_time').innerText = data['service_end_time'];
     
    });
  }
}

after_rendering_module = {
  /* 페이지 이동 시 실행되는 기능들 */
  stt : {
          start_stt: function(curr_page) {
            
            /* 음성 인식 html 변경 */
            document.getElementById('speech_guide').innerHTML = `
            <div class="spinner-grow text-info" role="status"></div>
            <div class="fs-sm">말씀해 주세요</div>`

            fetch('/start_stt?curr_page='+curr_page)
            .then(response => response.json())
            .then(data => {
                
                  /*
                  어떤 페이지에서 발화했는지 중요!
                  서비스 시작, 서비스 종료의 경우는
                  다음 페이지가 아니라
                  confirm_service
                  */
                  after_rendering_module.stt.stop_stt(curr_page);

                  if(data.return_result !== ''){
                    // 음성 인식 성공
                    if( data.return_result.includes('&')){
                      let next = data.return_result.match(/^(.*?)&/)[1];
                      let user_parameter = data.return_result.match(/&(.*)/)[1];
                      get_inner_page(next, user_parameter)
                    }else{
                      if(curr_page == 'start_step2'){
                        
                        confirm_service('start');
                        
                      }else if(curr_page == 'end_step1'){
                        
                        confirm_service('end');
                        
                      }else{
                        get_inner_page(data.return_result)
                      }
                    }
                    
                  }else{
                    // 음성 인식 실패
                    document.getElementById('speech_guide').innerHTML = `
                        <div class="speech_circle bg-warning" 
                        onclick="after_rendering_module.stt.start_stt('${curr_page}');">
                          <img src="static/david/img/play-circle-regular-36.png" /> 
                        </div>
                        <div class="fs-sm mt-1">음성지원 재시작</div>
                        `
                  }
            })
            .catch(error => console.error('Error:', error));
          },
          stop_stt: function(curr_page){
            fetch('/stop_stt')
            .then(response => {
              if(document.getElementById('speech_guide') !== null){
                document.getElementById('speech_guide').innerHTML = `
                <div class="speech_circle bg-warning" 
                onclick="after_rendering_module.stt.start_stt('${curr_page}');">
                  <img src="static/david/img/play-circle-regular-36.png" /> 
                </div>
                <div class="fs-sm mt-1">음성지원 재시작</div>
                `
              }
              
          })
            
            .catch(error => console.error('Error:', error));
          }
  }
  ,face_recognition :{
                        start_face_recognition : function(){
                              /*
                                cv2, face_recognition 얼굴 인증
                              */

                              //카메라 인증 진행 html
                              document.getElementById('camera_guide').innerHTML =  
                              `
                                <div class="spinner-border" style="width: 3.5rem; height: 3.5rem;"></div>
                                <div class="fs-sm mt-1">카메라 인증을 진행합니다.</div>`;

                              fetch('/start_face_recognition')
                              .then(response => response.json())
                              .then(data => { 
                                after_rendering_module.face_recognition.after_face_recognition(data['return_result']);
                                  
                              })
                              .catch(error => console.error('Error:', error));
                      }
                      ,stop_face_recognition : function() {
              
                            fetch('/stop_face_recognition')
                            .then(response => response.json())
                            .then(data => {
                              console.log("===stop_face_recognition:: "+data);
                            })
                            .catch(error => console.error('Error:', error));
                        }
                      , after_face_recognition : function(result){
                              after_rendering_module.face_recognition.stop_face_recognition();
                              if(result == 'True'){
                                document.getElementById('camera_guide').innerHTML = 
                                                `<div class="d-inline-block" >
                                                    <img src="static/david/img/user-check-regular-36.png"/>
                                                </div>
                                                <div class="fs-sm mt-1">사용자 인증에 성공했습니다.</div>`
                                
                                 get_inner_page('manage'); //관리 페이지 이동
                                
                              }else if(result == 'False'){
                                document.getElementById('camera_guide').innerHTML = 
                                                `<div class="d-inline-block" >
                                                  <img src="static/david/img/user-x-solid-36.png"/>
                                                </div>
                                                <div class="fs-sm mt-1">사용자 인증에 실패했습니다.</div>
                                                <button type="button" 
                                                class="btn btn-lg btn-warning mt-1" 
                              onclick="after_rendering_module.face_recognition.start_face_recognition();">
                              재인증 요청하기
                              </button>`
                        }
                        
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
  , get_currunt_datetime : function(time_id){
    const now = new Date();
    const year = now.getFullYear(); 
    const month = (now.getMonth() + 1).toString().padStart(2, '0'); 
    const day = now.getDate().toString().padStart(2, '0'); 
    const hours = now.getHours().toString().padStart(2, '0'); 
    const minutes = now.getMinutes().toString().padStart(2, '0');
    
    //해당 id에 값 고정
    document.getElementById(time_id).innerText = `${year}-${month}-${day} ${hours}:${minutes}`;
    
  }
  , get_currunt_service_info : function(callback){
    /* db 에서 현재 정보를 가져오는 함수 */
    fetch('module_collection/get_service_data')
     .then(response => response.json())
     .then(data => {
         callback(data);
     })
     .catch(error => console.error('Error:', error));
  }
}

function get_prev_page(prev, curr){
  //미완성. 이전으로 돌아가기 
  console.log("====get_prev_page===")

  fetch('get_page/get_prev_page?prev='+prev)
  .then(response => response.text())  
  .then(html => {
    document.getElementById('inner-content').innerHTML = html;
    after_rendering(prev);
    
  })
  .catch(error => console.error('Error loading the page: ', error));
}


function confirm_service(type=""){
  /* 
    -서비스 최종 결정
  */
  let body_data = null;
  let callback = null;
  if(type=="start"){
    body_data = {
      "path" : "service_info"
      ,"data" :{
        "service_type" : document.getElementById("service_type")?document.getElementById("service_type").innerText:""
        ,"service_status" : "서비스 진행중"
        ,"service_start_time" : document.getElementById("service_start_time").innerText
        ,"service_end_time" : document.getElementById("service_end_time")?document.getElementById("service_end_time").innerText:""
      
      }
     }

    callback = function(){
      document.getElementById('speech_guide').innerHTML = '';
      document.getElementById("user_guide").innerHTML = `<b>활동지원 서비스가<br/>시작되었습니다.</b>`
      document.getElementById("button_group").innerHTML  = `<button type="button" id="" class="btn btn-lg btn-secondary" 
      onclick="get_inner_page('first_gate')">처음 화면</button>`
    }
  }else if(type=="end"){
    body_data = {
      "path" : "service_info"
      ,"data" :{
          "service_type" : ""
          ,"service_status" : "서비스 없음"
          ,"service_start_time" : ""
          ,"service_end_time" : ""
      }
      
    }

    callback = function(){
      document.getElementById('speech_guide').innerHTML = '';
      document.getElementById("user_guide").innerHTML = `<b>활동지원 서비스가<br/>종료되었습니다.</b>`
      document.getElementById("button_group").innerHTML  = `<button type="button" id="" class="btn btn-lg btn-secondary" 
      onclick="get_inner_page('first_gate')">처음 화면</button>`
    }
  }else{
    alert("관리자에게 문의해 주세요.");
    return;
  }
  
  update_data(body_data, callback);
}

function check_auth(){
  /* 사용자 인증 결과 */
}

function update_data(body_data, callback){
    fetch('module_collection/update_data', {  
      method: 'POST', 
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(body_data) 
    })
    .then(response => response.json())  
    .then(data => {
        // 데이터 렌더링 예정
        console.log(data);
        callback();
      })
    .catch((error) => {
        console.error('Error:', error);
    });
}
