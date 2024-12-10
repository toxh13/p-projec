// 필요한 모듈을 불러옵니다
const express = require("express");
const bodyParser = require("body-parser");
const jwt = require("jsonwebtoken");
const cors = require("cors");
const mysql = require("mysql2");

// Express 앱 생성
const app = express();
const PORT = 3000;
const SECRET_KEY = "your_secret_key"; // JWT 서명용 키

// 미들웨어 설정
app.use(cors());
app.use(bodyParser.json());

// MySQL DB 연결 설정
const db = mysql.createConnection({
  host: "db", // DB 서버 주소
  user: "toxh13", // DB 사용자 이름
  password: "123123a", // DB 비밀번호
  database: "project_db", // 사용할 DB 이름
});

// DB 연결
db.connect((err) => {
  if (err) {
    console.error("DB 연결 실패:", err);
    return;
  }
  console.log("DB에 연결되었습니다.");
});

// 기본 라우터
app.get("/", (req, res) => {
  res.send("서버가 작동 중입니다.");
});

// JWT 인증 미들웨어
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1]; // Bearer [token] 형태에서 토큰 추출

  if (!token) return res.status(401).json({ message: "토큰이 없습니다." });

  jwt.verify(token, SECRET_KEY, (err, user) => {
    if (err) return res.status(403).json({ message: "토큰이 유효하지 않습니다." });
    req.user = user; // 사용자 정보를 요청에 추가
    next();
  });
};

// 로그인 API
app.post("/api/login", (req, res) => {
  const { email, password } = req.body;

  // 사용자 조회 쿼리
  const query = "SELECT * FROM Users WHERE email = ? AND password = ?";
  db.query(query, [email, password], (err, results) => {
    if (err) {
      console.error("DB 쿼리 실행 오류:", err);
      return res.status(500).json({ message: "서버 오류" });
    }

    if (results.length === 0) {
      return res
        .status(401)
        .json({ message: "아이디 또는 비밀번호가 잘못되었습니다." });
    }

    const user = results[0];

    // JWT 토큰 생성
    const token = jwt.sign({ id: user.id, email: user.email }, SECRET_KEY, { expiresIn: "1h" });

    // 로그인 성공 응답
    res.status(200).json({
      message: "로그인 성공",
      username: user.username,
      token, // JWT 토큰
    });
  });
});

// 회원가입 API
app.post("/api/signup", (req, res) => {
  const { email, password, username } = req.body;

  // 이메일 중복 확인
  const checkEmailQuery = "SELECT * FROM Users WHERE email = ?";
  db.query(checkEmailQuery, [email], (err, results) => {
    if (err) {
      console.error("DB 쿼리 실행 오류:", err);
      return res.status(500).json({ message: "서버 오류" });
    }

    if (results.length > 0) {
      return res.status(400).json({ message: "이미 등록된 이메일입니다." });
    }

    // 새로운 사용자 등록
    const query = "INSERT INTO Users (email, password, username) VALUES (?, ?, ?)";
    db.query(query, [email, password, username], (err) => {
      if (err) {
        console.error("DB 쿼리 실행 오류:", err);
        return res.status(500).json({ message: "서버 오류" });
      }

      res.status(201).json({ message: "회원가입 성공" });
    });
  });
});

// 인증된 사용자 정보 조회 API
app.get("/api/user", authenticateToken, (req, res) => {
  const userId = req.user.id;

  const query = "SELECT id, email, username FROM Users WHERE id = ?";
  db.query(query, [userId], (err, results) => {
    if (err) {
      console.error("DB 쿼리 실행 오류:", err);
      return res.status(500).json({ message: "서버 오류" });
    }

    if (results.length === 0) {
      return res.status(404).json({ message: "사용자를 찾을 수 없습니다." });
    }

    res.status(200).json(results[0]);
  });
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`서버가 ${PORT}번 포트에서 작동 중입니다.`);
});
