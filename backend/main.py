from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# 예시로 /recommendation 엔드포인트 추가
@app.get("/recommendation")
def get_recommendation():
    return {"recommendation": "상품 추천 정보"}
