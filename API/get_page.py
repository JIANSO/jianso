from flask import Flask, render_template, Blueprint, request, jsonify
import json
import API.module_collection as module_collection

get_page = Blueprint('get_page', __name__)
"""
inner page html만 전달하는 함수 모음
"""


@get_page.route('/get_prev_page', methods=['GET'])
def get_prev_page():
    essential_data = module_collection.get_essential_data()
    prev = request.args.get('prev', 'default_value')
    
    template_url = "david/paper/inner/inner_"+prev+".html"
    
    #인증 값 False의 경우 인증 화면
    if essential_data['auth'] == 'False' :
        template_url = "david/paper/inner/inner_recognition.html"

    return render_template(template_url, 
                           essential_data=essential_data)

@get_page.route('/get_next_page', methods=['GET'])
def get_next_page():

    essential_data = module_collection.get_essential_data()
    next = request.args.get('next', 'default_value')
    user_parameter = request.args.get('user_parameter', '')
    
    template_url = "david/paper/inner/inner_"+next+".html"
    
    #인증 값 False의 경우 인증 화면
    if essential_data['auth'] == 'False' :
        template_url = "david/paper/inner/inner_recognition.html"

    return render_template(template_url, 
                           essential_data=essential_data,
                           user_parameter=user_parameter)
