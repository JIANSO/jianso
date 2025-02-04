from flask import Flask, render_template, Blueprint, request, current_app

get_page = Blueprint('get_page', __name__)

"""
inner page html만 전달하는 함수 모음
"""

@get_page.route('/main')
def inner_main():
   
    return render_template("david/paper/inner/inner_main.html")

@get_page.route('/start')
def inner_start():
   
    return render_template("david/paper/inner/inner_start.html")