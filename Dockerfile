# Step 1: Node.js 기본 이미지 사용
FROM node:16

# Step 2: 작업 디렉토리 설정
WORKDIR /app

# Step 3: package.json 복사 후 의존성 설치
COPY package.json .
RUN npm install

# Step 4: 애플리케이션 코드 복사
COPY ./src ./src

# Step 5: 포트 노출
EXPOSE 3000

# Step 6: 앱 실행
CMD ["node", "src/index.js"]
