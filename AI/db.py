import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    외부 MySQL 서버에 연결을 생성하는 함수.
    """
    try:
        connection = mysql.connector.connect(
            host="khs.uy.to",       # 외부 서버 주소
            port=3306,              # MySQL 기본 포트
            user="toxh13",          # 사용자 이름
            password="123123a",     # 비밀번호
            database="project_db"   # 데이터베이스 이름
        )
        return connection
    except Error as err:
        print(f"DB 연결 실패: {err}")
        return None

def get_clothing_data():
    """
    Clothing 테이블에서 모든 데이터를 가져오는 함수.
    """
    query = "SELECT * FROM Clothing"
    connection = create_connection()
    if not connection:
        return None

    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()  # 모든 데이터를 가져옵니다.
            return result
    except Error as err:
        print(f"데이터 조회 실패: {err}")
        return None
    finally:
        if connection and connection.is_connected():
            connection.close()

def save_clothing_data(data):
    query = """
    INSERT INTO Clothing (
        상품명, 브랜드, 품번, 성별, `이미지 URL`,
        `현재 가격`, `평균 키`, `평균 몸무게`,
        구매사이트, 부위, 스타일
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    connection = create_connection()
    if not connection:
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (
                data['상품명'], data['브랜드'], data['품번'], data['성별'], data['이미지 URL'],
                data['현재 가격'], data['평균 키'], data['평균 몸무게'],
                data['구매사이트'], data['부위'], data['스타일']
            ))
            connection.commit()
            return True
    except Error as err:
        print(f"데이터 저장 실패: {err}")
        return False
    finally:
        if connection and connection.is_connected():
            connection.close()
