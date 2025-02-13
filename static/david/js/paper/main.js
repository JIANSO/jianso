function get_inner_page(next, user_parameter=''){
  /*
  TODO: 
  서비스 진행 중인지 아닌지 여부 파악 필요
  */
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
  // TODO: 서비스 진행중 여부를 항상 화면이 갖고 있도록 할까 고민중입니다.
  
  if(next == 'manage'){
    after_rendering_module.stt.start_stt();
  }else if(next == 'start_step1'){
  
    after_rendering_module.stt.start_stt();
    after_rendering_module.active_list();
  }else if(next == 'start_step2'){
  
    after_rendering_module.stt.start_stt();

    after_rendering_module.get_currunt_datetime('service_start_time');
  }else if(next == 'end_step1'){
    
    after_rendering_module.stt.start_stt();

    after_rendering_module.get_currunt_service_info(function(data){
      document.getElementById('service_status').innerText = data['service_status'];
      document.getElementById('service_type').innerText = data['service_type'];
      document.getElementById('service_start_time').innerText = data['service_start_time'];
      
      //종료 시간의 경우 현재 시간
      after_rendering_module.get_currunt_datetime('service_end_time');
    });
  }else if(next == 'recognition'){
    //추후 모든 모듈마다 붙일 것
    
    after_rendering_module.face_recognition.start_face_recognition(function(){
      document.getElementById('camera_guide').innerHTML = 
      `<div class="spinner-border" style="width: 3.5rem; height: 3.5rem;"></div>
       <div class="fs-sm">사용자 인증을 완료했습니다.</div>`
      after_rendering_module.face_recognition.stop_face_recognition();
    })
  }else if(next == 'data'){
    //after_rendering_module.stt.start_stt();
    after_rendering_module.get_currunt_service_info(function(data){
      document.getElementById('service_status').innerText = data['service_status'];
      document.getElementById('service_type').innerText = data['service_type'];
      document.getElementById('service_start_time').innerText = data['service_start_time'];
      document.getElementById('service_end_time').innerText = data['service_end_time'];
     
    });
  }
}

after_rendering_module = {
  stt : {
          start_stt: function() {
              /*
            실시간 음성 인식
            음성 인식으로 페이지 이동
            */
            
            // 아이콘 변경
            document.getElementById('speech_guide').innerHTML = `
            <div class="spinner-grow text-info" role="status"></div>
            <div class="fs-sm">말씀해 주세요</div>`
            //TODO 서버 음성 집어넣기

        
            fetch('/start_stt')
            .then(response => response.json())
            .then(data => {
                alert('페이지:: ' + data.return_result + '\n사용자 음성:: ' + data.audio_text);
        
                // llm 통과 후 다음 페이지 넘어갈 예정
                // 서버에서 처리 후 1,2,3 에 따라 페이지 넘길 예정 
                after_rendering_module.stt.stop_stt();
                if(data.return_result !== 0){
                  
                  //get_inner_page(data.return_result);
        
                }
            })
            .catch(error => console.error('Error:', error));
          },
          stop_stt: function(){
            fetch('/stop_stt')
            .then(response => response.json())
            .then(data => {
                document.getElementById('speech_guide').innerHTML = `
                <div class="speech_circle bg-info m-1" role="status" 
                onclick="after_rendering_module.stt.start_stt();">
                <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEgAAABICAYAAABV7bNHAAAAAXNSR0IArs4c6QAAA2dJREFUeF7tnAtu2zAMhtOTbT1Zt5OtPdkGFuGgGiH582U5KAMUbR1ZJj/+pOSH/HKbj0rgZfjoBAaQoZABNIByRWQUdFEF/bzdbvRDnx+Ljbzt/b7tY/mOtvH2nCwce5+pIHL+bQHjMPNL09/3/35FO/Ds1w2oCorkE8FqVVYXoG4wR2AEqkVRHYDIUEqlHZ9yUJWASDV/dlB5cMwyUFWAIqqh2kGj1Doy8d88mvFvYuBVZQmkCkAeOASAC2tEbFxnUFhpSFlAlFJrlLXRprqIooGhoLxGokH7ZAAhcLKKQfxCQIUhRQEhRlHUzpr5IgNEKN0igCw44WghcjHaWKp2Q/ICsuC4DSiAcuzCstGlbC+gv4pDV4DD5lmQYL/hhvepvDS87kwrKWZausHB9ADS1OPppyGrxC41m6FUQx3TJAsd6Ewqy7G00Q1SPQJIOwgs1U2A6LBaqpnBRQBp6kH238jm89ApFSEOSnn8DOpBRjWVgQXo2dWzqlcKtJpmUUBR9WijiicVLbsf9SXVIrVYWweqTq+dgLRaJHLQAIU6NGSwExCZ5k4zDZBUf6LppRnoSa/MZRopzUSfvhsgd9C/GyCpbIiFWgMkydGcfSr5srsGDSCjmJUCkqJtTQ00G3crSBsoHvqlOTuAjLsaU4MG0P9qMKPYHcXMg4xR7BRA0KVKwdDdo1gpoDlZBe7Nu89+L3w2H7r4Z036QheZLnqq4U4v5LJBR5p5L21UtQ9d/LMUpE3NM9eFqpxG+wmlF6Kg9H0l1IPmdiH1oIBS95WaHUe6T90VRlLsmVWUviuMArKe4EL7QSJe2Sb9wIXHMU2qmdl1JZC1r9Mff7HuSlxpVNvyABUBslLtCpAsOC4bPSnG8rUM2Jlu2x/iRCFRu8zdD29dspRN/bmUwwZEFMT7WtEKG+Wggy67Cqs6A8iaH61+hqJngLJSnXcPw0Fn0lZAUUNZUfQ7um4DVQzbnA5MVkGemnQEzWtPaTsvWTguh+KRkxb+IotmylVbBYhVgS5TslSZ/b5sgKgElFFTFkhZSh0N6QC0A1TbsqtOQFw/uLBWqWTtpw1MxTzI67B3OaXUfzuU9cDdCpKcXF9NQW349RTHV1PQd/x6itYXCEiG7gLkVd+29gPIQD+ABlAuO0dBo6Ccgv4BuBTlSVYNngwAAAAASUVORK5CYII="/>
                </div>
                <div class="fs-sm">음성지원 재시작</div>
                `

            })
            .catch(error => console.error('Error:', error));
          }
  }
  ,face_recognition :{
                        start_face_recognition : function(callback){
                        /*
                          cv2, face_recognition 얼굴 인증
                        */
                        
                        fetch('/start_face_recognition')
                        .then(response => response.json())
                        .then(data => {
                  
                            callback(data);
                            
                        })
                        .catch(error => console.error('Error:', error));
                      }
                      ,stop_face_recognition : function() {
                        // 카메라 종료, 수정 필요. 컴퓨터 카메라 종료가 되는지 확인해야함
                        fetch('/stop_face_recognition')
                        .then(response => response.json())
                        .then(data => {
                  
                            console.log("test")
                            
                        })
                        .catch(error => console.error('Error:', error));
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
    const year = now.getFullYear(); // 연도를 YYYY 형태로 반환
    const month = (now.getMonth() + 1).toString().padStart(2, '0'); // 월을 MM 형태로 반환 (getMonth()는 0부터 시작하므로 1을 더함)
    const day = now.getDate().toString().padStart(2, '0'); // 일을 DD 형태로 반환
    const hours = now.getHours().toString().padStart(2, '0');  // 시간을 두 자리 숫자로 표현
    const minutes = now.getMinutes().toString().padStart(2, '0');  // 분을 두 자리 숫자로 표현
    
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
    // 이전으로 돌아가기 후처리
    // 음성 종료, 재시작 예정
    // 카메라 종료 
    
  })
  .catch(error => console.error('Error loading the page: ', error));
}

function go_to_start_step2(){
  // 서비스 시작 시 서비스 유형 선택
  if (document.querySelector('div[name="service_type"] a.active')==null){
    alert("서비스 유형을 선택해 주세요");
    return
  }  

  get_inner_page('start_step2', user_parameter=document.querySelector('div[name="service_type"] a.active').innerText);
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
      document.getElementById("user_guide").innerHTML = `<b>활동지원 서비스가 시작되었습니다.</b>`
      document.getElementById("button_group").innerHTML  = `<button type="button" id="" class="btn btn-lg btn-secondary" 
      onclick="get_inner_page('main')">처음 화면</button>`
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
      document.getElementById("user_guide").innerHTML = `<b>활동지원 서비스가 종료되었습니다.</b>`
      document.getElementById("button_group").innerHTML  = `<button type="button" id="" class="btn btn-lg btn-secondary" 
      onclick="get_inner_page('main')">처음 화면</button>`
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
