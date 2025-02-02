from flask import Flask, render_template, Blueprint, current_app, request

bp_blog = Blueprint('bp_blog', __name__)
# MySQL configurations
    
@bp_blog.route('/main')
def blog_main():      
    
    return render_template("/anne/blog_main.html")

@bp_blog.route('/list', methods=['post'])
def get_list():
    
    type = request.form.get('type')  
    val = (type,)
    annedb = current_app.config['annedb']    
    cursor = annedb.cursor(dictionary=True)
    sql_text = "SELECT * FROM it_list where depth3 = %s"
    
    cursor.execute(sql_text, val)
    data = cursor.fetchall()
    
    print("=====data", data)
    
    # HTML 템플릿에 데이터 전달하기
    return render_template('/anne/inner/blog/inner_list.html', data=data)

@bp_blog.route('/detail', methods=['post'])
def get_detail():
    
    id_num = request.form.get('id_num')  
    val = (id_num,)
    annedb = current_app.config['annedb']    
    cursor = annedb.cursor(dictionary=True)
    sql_text = "SELECT * FROM it_detail where id_num = %s"
    
    cursor.execute(sql_text, val)
    data = cursor.fetchall()
    
    #TODO: 아직은 db insert기능이 없어서, 페이지를 그대로 꺼내오는 방법을 사용해야 할 듯하다.
    
    # HTML 템플릿에 데이터 전달하기
    return render_template('/anne/inner/blog/inner_detail.html', data=data)