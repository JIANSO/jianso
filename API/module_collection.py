from flask import Flask, render_template, Blueprint, request, jsonify
import json

module_collection = Blueprint('module_collection', __name__)
"""

"""


def get_service_status():
    
    path = 'static/data/service_info.json'
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data['service_status']

@module_collection.route('/get_service_data', methods=['GET'])
def get_service_data():
    #데이터 출력
    path = 'static/data/service_info.json'
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return jsonify(data)

@module_collection.route('/save_service_data', methods=['POST'])
def save_service_data():
    #데이터 입력
    data = request.get_json()
    path = 'static/data/service_info.json'
    
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


@module_collection.route('/update_data', methods=['POST'])
def update_data():
    """
    서비스 시작 또는 종료 확정

    """
    
    client_json = request.get_json()
    return_value = update_json(client_json)

    return jsonify(return_value)

def update_json(client_json) :
    """
    client_json 구조는 {"data" : "", "path" : ""}
    
    """
    path = None
    data = client_json["data"]
    if (client_json["path"] == 'service_info') :
        path = 'static/data/service_info.json'

    elif (client_json["path"] == 'auth') :
        path = 'static/data/auth.json'

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
    
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    print("====json 변경 완료 ::", path)
    
    return data