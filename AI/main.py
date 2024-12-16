import pandas as pd
from sqlalchemy import create_engine

# MySQL 연결 설정
DB_CONFIG = {
    "host": "khs.uy.to",
    "port": 3306,
    "user": "toxh13",
    "password": "123123a",
    "database": "project_db"
}

# SQLAlchemy 엔진 생성
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL)

# Clothing 테이블의 상위 5개 데이터 가져오기
clothing_data_query = "SELECT * FROM Clothing LIMIT 5"
try:
    clothing_data = pd.read_sql(clothing_data_query, con=engine)
    print("Clothing 테이블의 상위 데이터 5개:")
    print(clothing_data)
except Exception as e:
    print(f"데이터 로드 실패: {e}")
