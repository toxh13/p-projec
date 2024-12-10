from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from categorySelect import get_csv_path
import db

app = FastAPI()

# Pydantic 모델 정의
class UserDataRequest(BaseModel):
    userId: str
    gender: str
    stature: float
    weight: float
    top_style: Optional[str] = None
    bottom_style: Optional[str] = None

class RecommendationRequest(BaseModel):
    userId: str
    category: str
    exclude_indices: Optional[List[int]] = None

# 추천 데이터 처리 함수
def get_recommendation(gender, category, style, user_height, user_weight, exclude_indices=None):
    """
    추천 데이터를 처리하는 함수.
    """
    try:
        csv_path = get_csv_path(gender, category, style)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # CSV 파일 읽기 및 전처리
    try:
        data = pd.read_csv(csv_path).fillna("")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV 파일을 읽는 데 실패했습니다: {str(e)}")

    # 필터링 및 데이터 전처리
    data = data[(data['성별'] == gender) | (data['성별'] == "공용")]
    data['height'] = pd.to_numeric(data['평균 키'], errors='coerce')
    data['weight'] = pd.to_numeric(data['평균 몸무게'], errors='coerce')
    data = data.dropna(subset=['height', 'weight'])

    # 제외할 인덱스 처리
    if exclude_indices:
        data = data.drop(index=exclude_indices, errors='ignore')

    if data.empty:
        raise HTTPException(status_code=404, detail="추천 데이터가 부족합니다.")

    # KNN 모델을 사용한 추천
    try:
        knn_model = NearestNeighbors(n_neighbors=3, metric='euclidean')
        knn_model.fit(data[['height', 'weight']])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"KNN 모델 생성 중 오류 발생: {str(e)}")

    user_data = pd.DataFrame({'height': [user_height], 'weight': [user_weight]})
    distances, indices = knn_model.kneighbors(user_data)
    top_3_recommendations = data.iloc[indices[0]]

    return top_3_recommendations.reset_index(drop=True)

# 사용자 데이터 수집
@app.get("/clothing")
def get_clothing():
    """
    Clothing 테이블에서 모든 데이터를 가져오는 API.
    """
    clothing_data = db.get_clothing_data()
    if not clothing_data:
        raise HTTPException(status_code=404, detail="Clothing 데이터가 존재하지 않습니다.")
    return {"clothing_data": clothing_data}


# DB 상태 확인
@app.get("/db-status")
def db_status():
    """
    데이터베이스 연결 상태를 확인.
    """
    try:
        connection = db.create_connection()
        if connection and connection.is_connected():
            connection.close()
            return {"status": "success", "message": "DB 연결이 정상입니다."}
        else:
            return {"status": "failure", "message": "DB 연결에 실패했습니다."}
    except Exception as e:
        return {"status": "failure", "message": f"DB 연결에 실패했습니다. 오류: {str(e)}"}

# 추천 API
@app.post("/recommend")
def recommend(request: RecommendationRequest):
    """
    사용자 데이터를 기반으로 추천 결과를 반환.
    """
    # DB에서 사용자 데이터 조회
    user_info = db.get_user_data(request.userId)
    if not user_info:
        raise HTTPException(status_code=404, detail=f"User {request.userId} 데이터가 존재하지 않습니다.")

    gender = user_info["gender"]
    stature = user_info["stature"]
    weight = user_info["weight"]
    style = user_info.get(f"{request.category}_style")

    if not style:
        raise HTTPException(status_code=400, detail=f"{request.category} 스타일이 설정되지 않았습니다.")

    # 추천 데이터 생성
    recommendations = get_recommendation(
        gender, request.category, style, stature, weight, request.exclude_indices
    )
    if recommendations.empty:
        raise HTTPException(status_code=404, detail="추천 결과가 없습니다.")

    return recommendations.to_dict(orient="records")

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
