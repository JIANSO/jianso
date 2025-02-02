from flask import Flask, jsonify, render_template, Blueprint, current_app, request
import API.db_connect as get_db_connection

api_books = Blueprint('api_books', __name__)
# MySQL configurations
    


@api_books.route('/get_list', methods=['get'])
def get_list():
    """
        description : 책 목록 가져오기
        return : list (json)
    """
    
    #type = request.form.get('type')  
    #val = (type,)
    
    conn = get_db_connection()            
    with conn.cursor() as cursor:
        
        query = """                
            select * from db_books

            """
        cursor.execute(query, ())
        data = cursor.fetchall()   
        cursor.close()
        conn.close()     
    
    return jsonify({"result": data})
    
