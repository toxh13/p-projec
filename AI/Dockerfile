# 1. Python 기본 이미지 사용
FROM python:3.9-slim

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 필요한 패키지 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. 애플리케이션 코드 복사
COPY . .

# 5. 8000번 포트 오픈 (FastAPI 기본 포트)
EXPOSE 8000

# 6. FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
