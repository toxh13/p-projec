# 1. Node.js 이미지 사용
FROM node:16-alpine

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 의존성 파일을 복사
COPY package.json package-lock.json ./

# 4. 의존성 설치
RUN npm install

# 5. 애플리케이션 소스 코드 복사
COPY . .

# 6. 3000번 포트 오픈
EXPOSE 3000

# 7. 서버 실행 (서버 파일이 `server.js`라고 가정)
CMD ["node", "app.js"]
