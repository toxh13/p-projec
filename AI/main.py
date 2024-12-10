from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from categorySelect import get_csv_path
import db

app = FastAPI()

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

# 추천 데이터 처리
def get_recommendation(gender, category, style, user_height, user_weight, exclude_indices=None):
    try:
        csv_path = get_csv_path(gender, category, style)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = pd.read_csv(csv_path).fillna("")
    data = data[(data['성별'] == gender) | (data['성별'] == "공용")]
    data['height'] = pd.to_numeric(data['평균 키'], errors='coerce')
    data['weight'] = pd.to_numeric(data['평균 몸무게'], errors='coerce')
    data = data.dropna(subset=['height', 'weight'])

    if exclude_indices is not None:
        data = data.drop(index=exclude_indices, errors='ignore')

    knn_model = NearestNeighbors(n_neighbors=3, metric='euclidean')
    knn_model.fit(data[['height', 'weight']])

    user_data = pd.DataFrame({'height': [user_height], 'weight': [user_weight]})
    distances, indices = knn_model.kneighbors(user_data)
    top_3_recommendations = data.iloc[indices[0]]

    return top_3_recommendations.reset_index(drop=True)

@app.post("/collect")
def collect_user_data(request: UserDataRequest):
    # DB에 유저 데이터 저장
    success = db.save_user_data(
        request.userId,
        request.gender,
        request.stature,
        request.weight,
        request.top_style,
        request.bottom_style
    )
    
    if success:
        return {"message": f"User {request.userId} 데이터가 저장되었습니다."}
    else:
        raise HTTPException(status_code=500, detail="유저 데이터 저장에 실패했습니다.")
@app.get("/db-status")
def db_status():
    try:
        connection = db.create_connection()
        if connection.is_connected():
            connection.close()
            return {"status": "success", "message": "DB 연결이 정상입니다."}
        else:
            return {"status": "failure", "message": "DB 연결에 실패했습니다."}
    except Exception as e:
        return {"status": "failure", "message": f"DB 연결에 실패했습니다. 오류: {str(e)}"}


@app.post("/recommend")
def recommend(request: RecommendationRequest):
    # DB에서 유저 데이터 조회
    user_info = db.get_user_data(request.userId)
    if not user_info:
        raise HTTPException(status_code=404, detail=f"User {request.userId} 데이터가 존재하지 않습니다.")
    
    gender = user_info["gender"]
    stature = user_info["stature"]
    weight = user_info["weight"]
    style = user_info.get(f"{request.category}_style")

    if not style:
        raise HTTPException(status_code=400, detail=f"{request.category} 스타일이 설정되지 않았습니다.")

    recommendations = get_recommendation(
        gender, request.category, style, stature, weight, request.exclude_indices
    )
    if recommendations.empty:
        raise HTTPException(status_code=404, detail="추천 결과가 없습니다.")

    return recommendations.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
