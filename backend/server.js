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

const authenticateToken = (req, res, next) => {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1];

  if (!token) {
    console.error("[ERROR] 토큰이 없습니다.");
    return res.status(401).json({ message: "토큰이 없습니다." });
  }

  jwt.verify(token, SECRET_KEY, (err, user) => {
    if (err) {
      console.error("[ERROR] 토큰 검증 실패:", err);
      return res.status(403).json({ message: "토큰이 유효하지 않습니다." });
    }

    console.log("[INFO] 토큰 검증 성공, 사용자 정보:", user);
    req.user = user; // user 객체를 요청에 저장
    next();
  });
};




// 로그인 API
app.post("/api/login", (req, res) => {
  const { email, password } = req.body;

  const query = "SELECT * FROM Users WHERE email = ? AND password = ?";
  db.query(query, [email, password], (err, results) => {
    if (err) {
      console.error("DB 쿼리 실행 오류:", err);
      return res.status(500).json({ message: "서버 오류" });
    }

    if (results.length === 0) {
      return res.status(401).json({ message: "아이디 또는 비밀번호가 잘못되었습니다." });
    }

    const user = results[0];

    // JWT 토큰 생성
    const token = jwt.sign({ id: user.user_id, email: user.email }, SECRET_KEY, { expiresIn: "1h" });


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

  const checkEmailQuery = "SELECT * FROM Users WHERE email = ?";
  db.query(checkEmailQuery, [email], (err, results) => {
    if (err) {
      console.error("DB 쿼리 실행 오류:", err);
      return res.status(500).json({ message: "서버 오류" });
    }

    if (results.length > 0) {
      return res.status(400).json({ message: "이미 등록된 이메일입니다." });
    }

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
app.get("/api/clothing_presets", authenticateToken, (req, res) => {
  const userId = req.user.id; // 로그인된 사용자의 ID

  if (!userId) {
    console.error("[ERROR] 사용자 ID가 undefined 상태입니다.");
    return res.status(400).json({ message: "사용자 ID가 필요합니다." });
  }

  console.log(`[INFO] 사용자 ID(${userId})의 프리셋 요청 수신`);

  const query = `
    SELECT 
      user_closet_id,
      user_id,
      top_clothing_id,
      bottom_clothing_id,
      style,
      added_at AS created_at
    FROM User_Closets
    WHERE user_id = ? 
    ORDER BY added_at DESC;
  `;

  db.query(query, [userId], (err, results) => {
    if (err) {
      console.error("[ERROR] DB 조회 오류:", err);
      return res.status(500).json({ message: "DB 조회 오류" });
    }

    res.status(200).json({ message: "프리셋 조회 성공", data: results });
  });
});




// 프리셋 삭제 API (User_Closets 테이블 기반)
app.delete("/api/user_closets/:presetId", authenticateToken, (req, res) => {
  const presetId = req.params.presetId; // 삭제하려는 프리셋 ID
  const userId = req.user.id; // 로그인된 사용자의 ID

  console.log(`[INFO] 사용자 ID(${userId})의 프리셋 삭제 요청: presetId(${presetId})`);

  const query = `
    DELETE FROM User_Closets
    WHERE user_closet_id = ? AND user_id = ?;
  `;

  db.query(query, [presetId, userId], (err, result) => {
    if (err) {
      console.error("[ERROR] DB 삭제 오류:", err);
      return res.status(500).json({ message: "DB 삭제 오류" });
    }

    if (result.affectedRows === 0) {
      console.log(`[INFO] 삭제 실패: 사용자 ID(${userId})의 프리셋(${presetId})이 존재하지 않거나 권한 없음`);
      return res
        .status(404)
        .json({ message: "해당 프리셋을 찾을 수 없거나 삭제 권한이 없습니다." });
    }

    console.log(`[INFO] 사용자 ID(${userId})의 프리셋(${presetId})이 삭제되었습니다.`);
    res.status(200).json({ message: "프리셋이 삭제되었습니다." });
  });
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`서버가 ${PORT}번 포트에서 작동 중입니다.`);
});