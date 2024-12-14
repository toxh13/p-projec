from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql
from fastapi.templating import Jinja2Templates
from fastapi import Request
from deepRunning import recommend_clothing, recommend_otherClothing  # deepRunning에서 recommend_clothing 함수를 불러옵니다.

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청 허용 (보안을 위해 특정 도메인을 명시적으로 설정 권장)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# HTML 템플릿을 위한 설정
templates = Jinja2Templates(directory="templates")

# Static 파일 서빙 (예: CSS, JS 등)
app.mount("/static", StaticFiles(directory="static"), name="static")

# MySQL 데이터베이스 설정
DB_CONFIG = {
    "host": "khs.uy.to",       # MySQL 서버 주소
    "port": 3306,                 # MySQL 포트
    "user": "toxh13",             # MySQL 사용자 이름
    "password": "123123a",        # MySQL 비밀번호
    "database": "project_db",     # 데이터베이스 이름
}

DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# SQLAlchemy 엔진 및 세션 생성
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 모델 정의
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)  # 예: "top", "bottom"
    name = Column(String)
    image = Column(String)

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)

# 의존성 주입을 위한 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HTML 파일을 렌더링하여 반환하는 라우트
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 추천 API 라우트
@app.post("/api/recommend")
async def recommend(user_height: int = Form(...), user_weight: int = Form(...),
                    user_gender: str = Form(...), user_style: str = Form(...),
                    clothingType: str = Form(...), db: SessionLocal = next(get_db())):

    # 받은 사용자 데이터를 출력 (디버깅용)
    print(f"User data received: Height: {user_height}, Weight: {user_weight}, Gender: {user_gender}, Style: {user_style}, Clothing Type: {clothingType}")

    # 추천을 위한 AI 함수 호출 (deepRunning.py에서 추천 결과를 가져옵니다)
    recommendations_from_ai = recommend_clothing(user_height, user_weight, user_gender,
                                                 user_style, clothingType)

    # 추천 결과가 비어있는지 확인
    if not recommendations_from_ai:
        raise HTTPException(status_code=404, detail="Recommendations not found")

    # 결과를 JSON 형식으로 변환하여 반환
    return {"recommendations": recommendations_from_ai}

# 재추천 요청 처리
@app.post("/api/recommend/refresh")
async def refresh_recommendations(
    user_height: int = Form(...),
    user_weight: int = Form(...),
    user_gender: str = Form(...),
    user_style: str = Form(...),
    clothingType: str = Form(...),
    excluded_items: list = Form(...)
):
    # 제외된 항목으로 새 추천 생성
    recommendations = recommend_clothing(
        user_height, user_weight, user_gender, user_style, clothingType, excluded_items=excluded_items
    )

    if not recommendations:
        raise HTTPException(status_code=404, detail="새로운 추천 결과가 없습니다.")

    return {"recommendations": recommendations}

@app.post("/api/recommend/other")
async def recommend_other(
    selected_item_name: str = Form(...),
    clothingType: str = Form(...),
    excluded_items: list = Form(...)
):
    """
    다른 부위 의류 추천 엔드포인트.
    :param selected_item_name: 사용자가 선택한 의류 이름.
    :param clothingType: 추천받을 의류 부위.
    :param excluded_items: 추천 제외 항목 리스트.
    """
    # SQLAlchemy로 데이터베이스 연결
    clothing_data_query = "SELECT * FROM Clothing"
    clothing_data = pd.read_sql(clothing_data_query, engine)

    # 다른 부위 추천 호출
    recommendations = recommend_otherClothing(
        selected_item_name, clothing_data, model, clothingType, excluded_items=excluded_items
    )

    if not recommendations:
        raise HTTPException(status_code=404, detail="추천 결과가 없습니다.")

    return {"recommendations": recommendations}

