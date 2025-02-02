from flask import Flask, render_template, Blueprint, request, current_app
import API.db_connect as db_connect


bp_church = Blueprint('bp_church', __name__)

@bp_church.route('/main')
def bible_verse_card():
    return render_template("/anne/church_main.html")


@bp_church.route('/contents/bible_verse_card', methods=['post'])
def youtube_library():
    return render_template("/anne/inner/inner_bible_verse_card.html")

@bp_church.route('/contents/youtube', methods=['post'])
def contents_youtube():
    
    type = request.form.get('type')        
    page = request.form.get("page", default=1, type=int)
              
    connection = db_connect.get_db_connection()
    with connection.cursor() as cursor:   
            
        sql_text = f"""
        SELECT 
            depth3, 
            image_addr, 
            url_addr, 
            media_date,
            title, 
            content 
        FROM 
            media_list 
        where depth2 = %s
        order by media_date desc
        LIMIT 5 OFFSET %s
        """
        cursor.execute(sql_text, (type, (page-1)*10))
        data = cursor.fetchall()
        
        cursor.close()
        connection.close()
    
    return render_template('/anne/inner/inner_youtube_library.html', data=data)