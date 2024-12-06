# 1. Python 기본 이미지 사용
FROM python:3.9-slim

# 2. 작업 디렉터리 설정 (ai_server 폴더로 설정)
WORKDIR /app

# 3. requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt ./

# 4. 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 애플리케이션 파일을 컨테이너로 복사
COPY . .

# 6. FastAPI 서버 실행 (main.py 파일을 찾아서 실행)
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
