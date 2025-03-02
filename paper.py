from flask import Flask, render_template,jsonify, request

app = Flask(__name__)

########################################################
# https://jianso.gabia.io/ 용 서버
########################################################
app.config['DEBUG'] = True

@app.route('/')
def home():

    return render_template("/paper.html")

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
