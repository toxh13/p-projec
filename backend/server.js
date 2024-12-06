// 필요한 모듈을 불러옵니다.
const express = require('express');

// Express 앱 생성
const app = express();

// 포트 설정
const PORT = process.env.PORT || 3000;

// 기본 라우터 설정
app.get('/', (req, res) => {
  res.send('Hello World from the backend server!');
});

// 서버 실행
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
