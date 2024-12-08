from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from categorySelect import get_csv_path

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

user_data = {}  # 유저 데이터를 저장하는 메모리 저장소

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
    user_data[request.userId] = {
        "gender": request.gender,
        "stature": request.stature,
        "weight": request.weight,
        "top_style": request.top_style,
        "bottom_style": request.bottom_style,
    }
    return {"message": f"User {request.userId} 데이터가 저장되었습니다.", "data": user_data[request.userId]}

@app.post("/recommend")
def recommend(request: RecommendationRequest):
    user_info = user_data.get(request.userId)
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
