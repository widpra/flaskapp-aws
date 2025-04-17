import pymysql

def get_db_connection():
    return pymysql.connect(
        host='your-rds-endpoint',
        user='admin',
        password='yourpassword',
        database='formdb',
        cursorclass=pymysql.cursors.DictCursor
    )
