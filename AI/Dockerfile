# Python 3.9-slim 이미지 사용
FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /app

# 요구사항 파일을 복사하여 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일을 복사
COPY . .

# FastAPI 애플리케이션 실행 (main.py 파일이 현재 /app 디렉터리에 있어야 함)
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
