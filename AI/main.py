from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI 서버가 정상적으로 시작되었습니다."}
