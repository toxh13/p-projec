from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from deepLearning import recommend_clothing, load_clothing_data
from typing import Optional
# FastAPI 앱 초기화
app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 요청 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# SQLAlchemy 설정
DB_CONFIG = {
    "host": "khs.uy.to",
    "port": 3306,
    "user": "toxh13",
    "password": "123123a",
    "database": "project_db",
}
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Pydantic 모델 정의
class RecommendationRequest(BaseModel):
    user_id: Optional[int] 
    height: int
    weight: int
    gender: str
    style: str
    clothingType: str

@app.post("/api/recommend")
async def recommend(request: RecommendationRequest):
    logger.info(f"Received request: {request.dict()}")  # 입력 로그 출력

    # Clothing 데이터 로드
    try:
        clothing_data = load_clothing_data()
    except Exception as e:
        logger.error(f"Error loading clothing data: {e}")
        raise HTTPException(status_code=500, detail="Failed to load clothing data")

    # 추천 실행
    try:
        recommendations = recommend_clothing(
            user_id=request.user_id,
            clothing_data=clothing_data,
            user_height=request.height,
            user_weight=request.weight,
            user_gender=request.gender,
            user_style=request.style,
            clothingType=request.clothingType,
            top_n=3
        )
        if not recommendations:
            logger.info("No recommendations found for the given criteria.")
            return {"recommendations": []}
        
        logger.info(f"Recommendations: {recommendations}")
        return {"recommendations": recommendations}

    except Exception as e:
        logger.error(f"Error during recommendation: {e}")
        raise HTTPException(status_code=500, detail="Error during recommendation")
