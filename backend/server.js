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


// Express 앱 생성, 포트 설정
const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));

//선택한 정보들을 수집해서 AI서버에 전달 및 결과를 프론트엔드로 반환

const connection = mysql.createConnection({
  host: process.env.DB_HOST || 'db',  // Docker에서는 db 서비스 이름을 사용
  user: process.env.DB_USER || 'toxh13',
  password: process.env.DB_PASSWORD || '123123a',
  database: process.env.DB_NAME || 'project_db'
});


//데이터베이스 연결
connection.connect((err) => {
  if (err) {
    console.error('데이터베이스 연결 실패: ', err.stack);
    return;
  }
  console.log('데이터베이스에 연결');
});

//기본 라우터
app.get('/', (req, res) => {
    res.send('Hello World from the bkend srver!');
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

db.connect((err) => {
    if (err) {
      console.error('Database connection error:', err);
    } else {
      console.log('Connected to the database.');
    }
});


//로그인페이지
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/login.html'));
});

//POST: 로그인 요청 처리
app.post('/api/login', (req, res) => {
  const { user_id, password } = req.body;

  const query = 'SELECT * FROM users WHERE user_id = ?';
  db.query(query, [user_id], async (err, results) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Internal server error');
    }

    if (results.length === 0) {
      return res.status(404).send('User not found');
    }

    const user = results[0];
    try {
      const isMatch = await bcrypt.compare(password, user.password);
      if (isMatch) {
        const token = jwt.sign({ user_id: user.user_id }, 'your-secret-key', { expiresIn: '1h' });
        res.status(200).json({ message: 'Login successful', token });
      } else {
        res.status(401).send('Invalid user_id or password');
      }
    } catch (error) {
      console.error('Error during password comparison:', error);
      res.status(500).send('Internal server error');
    }
  });
});

//회원가입페이지
app.get('/join', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/join.html'));
});

// 회원가입 API
//password와 confirmpassword 일치여부, 중복된 아이디 여부, 중복된 이메일 여부 확인 후 회원가입
app.post('/join', async (req, res) => {
    const { user_id, password, confirmPassword, user_name, dob, email } = req.body;
  //아이디, 비번, 비번확인, 이름, 생년월일, 이메일
    //비밀번호 확인
    if (!user_id || !password || !confirmPassword || !user_name || !dob || !email) {
      return res.status(400).json({ message: "모든 정보를 입력해주세요." });
    }

    if (password !== confirmPassword) {
      return res.status(400).json({ message: "비밀번호가 일치하지 않습니다." });
    }

try {
  //ID 중복 확인
  const [idCheckResult] = await db.promise().query(
    "SELECT * FROM users WHERE user_id = ?",
    [user_id]
  );
  if (idCheckResult.length > 0) {
    return res.status(400).json({ message: "이미 존재하는 아이디입니다." });
  }

  // 이메일 중복 확인
  const [emailCheckResult] = await db.promise().query(
    "SELECT * FROM users WHERE email = ?",
    [email]
  );
  if (emailCheckResult.length > 0) {
    return res.status(400).json({ message: "이미 사용 중인 이메일입니다." });
  }

  //비밀번호 해시화
  const hashedPassword = await bcrypt.hash(password, 10);

  //사용자 데이터 저장
  const [insertResult] = await db.promise().query(
    "INSERT INTO users (user_id, password, user_name, dob, email) VALUES (?, ?, ?, ?, ?)",
    [user_id, hashedPassword, user_name, dob, email]
);

  console.log("회원가입 성공:", insertResult);
  res.status(201).json({ message: "회원가입 완료" });
} catch (err) {
  console.error("회원가입 실패:", err);
  res.status(500).json({ message: "실패" });
}
});




//서버 시작
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
