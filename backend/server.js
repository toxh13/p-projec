// 필요한 모듈을 불러옵니다
const express = require("express");
const bodyParser = require("body-parser");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const cors = require("cors");
const path = require("path");
const mysql = require('mysql2');
const session = require("express-session");
const axios = require("axios");
// Express 앱 생성
const app = express();
const PORT = 3000;

// 미들웨어 설정
app.use(cors());  // CORS 허용
app.use(bodyParser.json());  // JSON 요청 처리

// MySQL DB 연결 설정
const db = mysql.createConnection({
  host: 'db',  // DB 서버 주소
  user: 'toxh13',       // DB 사용자 이름
  password: '123123a',  // DB 비밀번호
  database: 'project_db'  // 사용할 DB 이름
});

// DB 연결
db.connect((err) => {
  if (err) {
    console.error('DB 연결 실패:', err);
    return;
  }
  console.log('DB에 연결되었습니다.');
});

// 기본 라우터
app.get('/', (req, res) => {
  res.send('서버가 작동 중입니다.');
});

// 로그인 요청을 처리하는 라우터
app.post('/api/login', (req, res) => {
  const { email, password } = req.body;

  // MySQL 쿼리로 사용자 정보 확인
  const query = 'SELECT * FROM Users WHERE email = ? AND password = ?';
  
  db.query(query, [email, password], (err, results) => {
    if (err) {
      console.error('DB 쿼리 실행 오류:', err);
      return res.status(500).json({ message: '서버 오류' });
    }

    if (results.length > 0) {
      // 로그인 성공 시, 사용자 정보 반환 및 토큰 생성
      return res.status(200).json({
        message: '로그인 성공',
        token: 'dummy_token',  // 실제 토큰을 JWT 등을 사용해 생성할 수 있습니다.
      });
    } else {
      // 로그인 실패 시
      return res.status(401).json({ message: '아이디나 비밀번호가 잘못되었습니다.' });
    }
  });
});
app.post('/api/signup', (req, res) => {
  const { email, password, username } = req.body;

  // 이메일 중복 확인
  const checkEmailQuery = 'SELECT * FROM Users WHERE email = ?';
  db.query(checkEmailQuery, [email], (err, results) => {
    if (err) {
      console.error('DB 쿼리 실행 오류:', err);
      return res.status(500).json({ message: '서버 오류' });
    }

    if (results.length > 0) {
      return res.status(400).json({ message: '이미 등록된 이메일입니다.' });
    }

    // 새로운 사용자 등록
    const query = 'INSERT INTO Users (email, password, username) VALUES (?, ?, ?)';
    db.query(query, [email, password, username], (err, result) => {
      if (err) {
        console.error('DB 쿼리 실행 오류:', err);
        return res.status(500).json({ message: '서버 오류' });
      }

      return res.status(201).json({ message: '회원가입 성공' });
    });
  });
});
app.get('/', (req, res) => {
  res.send('Hello World');
});

//성별 저장
app.post("/api/option/gender", (req, res) => {
  const { gender } = req.body;
  if (!gender || (gender !== "남성" && gender !== "여성")) {
    return res.status(400).json({ message: "유효하지 않은 성별입니다." });
  }
  req.session.gender = gender;
  res.status(200).json({ message: `성별 ${gender}이 저장되었습니다.` });
});

//신체정보(키 몸무게) 저장
app.post("/api/option/physical-info", (req, res) => {
  const { stature, weight } = req.body;
  if (!stature || stature <= 0 || isNaN(stature) || !weight || weight <= 0 || isNaN(weight)) {
    return res.status(400).json({ message: "유효하지 않은 신체정보입니다." });
  }
  req.session.physicalInfo = { stature, weight };
  res.status(200).json({ message: "신체 정보가 저장되었습니다." });
});

//상의/하의 선택 API
app.post('/optionTBSel.html', (req, res) => {
  const { userId, selection } = req.body;
  //selection은 'top' 또는 'bottom'
  if (!userId || !selection) {
    return res.status(400).json({ message: 'userId와 selection이 필요' });
  }

  topandbottom[userId] = selection;
  console.log(`[INFO] User(${userId}) top/bottom selected: ${selection}`);
  res.json({ message: '상의/하의 선택이 저장됨', data: topandbottom[userId] });
});

//상의 스타일 선택 API
app.post('/optionSelTop.html', (req, res) => {
  const { userId, style } = req.body;
  //style은 '캐주얼', '스트릿', '미니멀', ... 중 하나로 가정
  if (!userId || !style) {
    return res.status(400).json({ message: 'userId와 style이 필요' });
  }

  top_style[userId] = style;
  console.log(`[INFO] User(${userId}) top style selected: ${style}`);
  res.json({ message: '상의 스타일 선택이 저장됨', data: top_style[userId] });
});

//하의의 스타일 선택 API
app.post('/optionSelBottom.html', (req, res) => {
  const { userId, style } = req.body;
  //style은 '캐주얼', '스트릿', '미니멀', ... 중 하나
  if (!userId || !style) {
    return res.status(400).json({ message: 'userId와 style이 필요' });
  }

  top_style[userId] = style;
  console.log(`[INFO] User(${userId}) top style selected: ${style}`);
  res.json({ message: '하의 스타일 선택이 저장됨', data: bottom_style[userId] });
});

//저장한 성별, 신체정보(키,몸무게), 상하의 선택, 상의 및 하의 스타일 저장
app.get("/optionSelTop.html", (req, res) => {
  const userInfo = {
    gender: req.session.gender,
    physicalInfo: req.session.physicalInfo,
    topandbottom: req.session.topandbottom,
    top_style: req.session.top_style,
    bottom_style: req.session.bottom_style,
  };
  res.json(userInfo);
});
//해당 정보를 AI서버로 전달 및 결과를 프론트엔드로 전달 구현해야함


// 서버 시작
app.listen(PORT, () => {
  console.log(`서버가 ${PORT}번 포트에서 작동 중입니다.`);
});
