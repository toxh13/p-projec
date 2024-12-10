# db.py
import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="db_host",  # DB 서버 주소
            user="root",     # DB 사용자
            password="password",  # DB 비밀번호
            database="your_database"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"DB 연결 실패: {err}")
        return None

def save_user_data(user_id, gender, stature, weight, top_style, bottom_style):
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO users (user_id, gender, stature, weight, top_style, bottom_style)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, gender, stature, weight, top_style, bottom_style))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"데이터 저장 실패: {err}")
        return False
    finally:
        if connection:
            connection.close()

def get_user_data(user_id):
    connection = create_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        print(f"데이터 조회 실패: {err}")
        return None
    finally:
        if connection:
            connection.close()
