from flask import Flask, render_template,jsonify
from API.get_page import get_page

app = Flask(__name__)
app.register_blueprint(get_page, url_prefix='/get_page')

# debug 모드 설정
app.config['DEBUG'] = True


@app.route('/')
def home():
    """
    connection = db_connect.get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT VERSION()"
        cursor.execute(sql)
        result = cursor.fetchall() 
        print("=======Successfully connected to MySQL :: ", result)
        
        cursor.close()
        connection.close()
        """
    
    return render_template("/index.html")

@app.route('/start_recording')
def start_recording():
    from API.sst import sst
    result = sst.sst_module()

    return jsonify({"result": result['text']})

@app.errorhandler(Exception)
def handle_error(error):
    # 에러 페이지 렌더링
    print(error)
    return render_template('404-v1.html', error=error), 500

import os
if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 8888)
    print("===server start===")
    app.run(host=host, port=int(port), debug=True)
