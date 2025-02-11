from flask import Flask, render_template, Blueprint, request, jsonify
import json

get_page = Blueprint('get_page', __name__)
"""
inner page html만 전달하는 함수 모음
"""

@get_page.route('/main')
def inner_main():
    return render_template("david/paper/inner/inner_main.html")

@get_page.route('/get_prev_page', methods=['GET'])
def get_prev_page():
    #데이터 출력
    prev = request.args.get('prev', 'default_value')
    
    return render_template("david/paper/inner/inner_"+prev+".html")

@get_page.route('/get_next_page', methods=['GET'])
def get_next_page():
   
    next = request.args.get('next', 'default_value')
    user_parameter = request.args.get('user_parameter', '')
    print("===user_parameter",user_parameter)
    
    return render_template("david/paper/inner/inner_"+next+".html", user_parameter=user_parameter)

@get_page.route('/get_service_data')
def get_service_data():
    #데이터 출력
    path = '/static/data/flow.json'
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return jsonify(data)

@get_page.route('/save_service_data', methods=['POST'])
def save_service_data():
    #데이터 입력
    data = request.get_json()
    path = '/static/data/flow.json'
    
    # 기존 데이터를 유지하고 새 데이터 추가
    try:
        # 기존 파일 읽기
        with open(path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
        # 새 데이터 추가
        existing_data.update(data)

    except FileNotFoundError:
        # 파일이 없는 경우 새 데이터로 시작
        existing_data = data

    # 변경된 데이터를 파일에 다시 쓰기
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
    
    return jsonify({"status": "success", "message": "Data saved successfully."})