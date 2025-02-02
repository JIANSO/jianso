from flask import Flask, render_template, Blueprint, current_app, request
import API.db_connect as db_connect

anne_mng = Blueprint('anne_mng', __name__)
# MySQL configurations
    
@anne_mng.route('/main')
def manage_main():      
    
    return render_template("/anne/manage/mng_main.html")


@anne_mng.route('/insert_library', methods=['POST'])
def insert_library():      
    
   
    connection = db_connect.get_db_connection()
    try:
        media_date = request.form['media_date']
        depth1      = request.form['depth_1']
        depth2      = request.form['depth_2']
        depth3      = request.form['depth_3']
        title       = request.form['title']
        content     = request.form['content']
        image_addr  = request.form['image_addr']
        url_addr    = request.form['url_addr']
        media_date = request.form['media_date']
    except KeyError as e:        
        print(e)
     
    try : 
        with connection.cursor() as cursor:
           
            sql_txt = '''
                INSERT INTO media_list
                (
                    depth1, 
                    depth2, 
                    depth3, 
                    title, 
                    content, 
                    image_addr, 
                    url_addr, 
                    media_date
                ) 
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s)           
           '''
            cursor.execute(sql_txt, (depth1, depth2, depth3, title, content, image_addr, url_addr, media_date))
                                    
            connection.commit()
            cursor.close()
            connection.close()
        
    except Exception as e : 
        print("Error :", e)
    
    
    return render_template("/anne/manage/mng_main.html")