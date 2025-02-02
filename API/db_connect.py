import pymysql

def get_db_connection() :

    connection = pymysql.connect(
            host= 'localhost',
            user= 'root',
            password= '619619Sja@!',
            db= 'bright_night',
            port= 3306,
            autocommit=True,
            cursorclass = pymysql.cursors.DictCursor
    )  
    
    return connection