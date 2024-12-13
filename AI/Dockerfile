# Python 3.9-slim 이미지 사용
FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pandas
RUN pip install scikit-learn
# 애플리케이션 파일 복사
COPY . .

# FastAPI 애플리케이션 실행 (main.py가 /app 디렉터리에 있어야 함)
EXPOSE 8000
CMD ["uvicorn", "ai_server:app", "--host", "0.0.0.0", "--port", "8000"]
