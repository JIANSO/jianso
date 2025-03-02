from flask import Flask, render_template, Blueprint, request, jsonify
import json
import API.module_collection as module_collection

get_page = Blueprint('get_page', __name__)
#########################################
# 이전/다음 페이지 호출용 py
#########################################


@get_page.route('/get_prev_page', methods=['GET'])
def get_prev_page():
    essential_data = module_collection.get_essential_data()
    prev = request.args.get('prev', 'default_value')
    template_url = "david/paper/inner/inner_"+prev+".html"
    
    #인증 값 False의 경우 인증 화면
    if essential_data['auth'] == 'False' :
        template_url = "david/paper/inner/inner_recognition.html"
    
    if(prev == 'first_gate') :
        import API.module_collection as module
        module.update_json({"data" :  {"auth" : "False"}, "path" : "auth"})

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
    
    if(next == 'first_gate') :
        import API.module_collection as module
        module.update_json({"data" :  {"auth" : "False"}, "path" : "auth"})

    return render_template(template_url, 
                           essential_data=essential_data,
                           user_parameter=user_parameter)
