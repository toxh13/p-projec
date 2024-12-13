from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청 허용 (보안을 위해 특정 도메인을 명시적으로 설정 권장)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.post("/api/recommend")
async def recommend(data: dict):
    # 임시로 조건에 맞는 데이터 반환
    recommendations = {
        "top": [
            {"name": "상의1", "image": "https://example.com/top1.jpg"},
            {"name": "상의2", "image": "https://example.com/top2.jpg"},
            {"name": "상의3", "image": "https://example.com/top3.jpg"},
        ],
        "bottom": [
            {"name": "하의1", "image": "https://example.com/bottom1.jpg"},
            {"name": "하의2", "image": "https://example.com/bottom2.jpg"},
            {"name": "하의3", "image": "https://example.com/bottom3.jpg"},
        ],
    }

    response = recommendations[data.get("type", "top")]
    return {"recommendations": response}
