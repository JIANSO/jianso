from flask import Flask, render_template, Blueprint, request, current_app

get_page = Blueprint('get_page', __name__)

"""
inner page html만 전달하는 함수 모음
"""

@get_page.route('/main')
def inner_main():
   
    return render_template("david/paper/inner/inner_main.html")

@get_page.route('/get_next_page', methods=['GET'])
def get_next_page():
   
    next = request.args.get('next', 'default_value')
    
    return render_template("david/paper/inner/inner_"+next+".html")

@get_page.route('/get_prev_page', methods=['GET'])
def get_prev_page():
   
    prev = request.args.get('prev', 'default_value')
    
    return render_template("david/paper/inner/inner_"+prev+".html")