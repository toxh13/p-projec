from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from categorySelect import get_csv_path

app = FastAPI()

class RecommendationRequest(BaseModel):
    gender: str
    category: str
    style: str
    height: float
    weight: float
    exclude_indices: list = None

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
        data = data.drop(exclude_indices, errors='ignore')

    knn_model = NearestNeighbors(n_neighbors=3, metric='euclidean')
    knn_model.fit(data[['height', 'weight']])

    user_data = pd.DataFrame({
        'height': [user_height],
        'weight': [user_weight]
    })

    distances, indices = knn_model.kneighbors(user_data)
    top_3_recommendations = data.iloc[indices[0]]

    return top_3_recommendations.reset_index(drop=True)

@app.post("/recommend")
def recommend(request: RecommendationRequest):
    recommendations = get_recommendation(
        request.gender, request.category, request.style,
        request.height, request.weight, request.exclude_indices
    )
    if recommendations is None or recommendations.empty:
        raise HTTPException(status_code=404, detail="No recommendations found")

    return recommendations.to_dict(orient='records')

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
