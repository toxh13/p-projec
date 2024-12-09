# 1. Node.js 이미지 사용
FROM node:18

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 의존성 파일을 복사
COPY package*.json ./ 

# 4. 의존성 설치
RUN npm install
RUN npm install bcrypt --build-from-source
RUN npm install express

# 5. 애플리케이션 소스 코드 복사
COPY . .

# 6. 3000번 포트 오픈
EXPOSE 3000

# 7. 서버 실행
CMD ["node", "server.js"]
