from flask import Flask, render_template, Blueprint, request, jsonify
import json

module_collection = Blueprint('module_collection', __name__)
"""
inner page html만 전달하는 함수 모음
"""

@module_collection.route('/get_service_data')
def get_service_data():
    #데이터 출력
    path = '/static/data/flow.json'
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return jsonify(data)

@module_collection.route('/save_service_data', methods=['POST'])
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

@module_collection.route('/confirm_service_start', methods=['POST'])
def confirm_service_start():
    #데이터 저장 및 출력
    data = request.get_json()
    print("=====data ::", data)
    path = 'static/data/flow.json'
    
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

    return jsonify(data)