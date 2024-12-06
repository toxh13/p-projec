// 필요한 모듈을 불러옵니다
const express = require("express");
const bodyParser = require("body-parser");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const cors = require("cors");
const path = require("path");

// Express 앱 생성, 포트 설정
const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));

//선택한 정보들을 수집해서 AI서버에 전달 및 결과를 프론트엔드로 반환

let gender = {}; //성별 저장 변수
let physicalInfo = {};//신체정보(키, 몸무게)저장 변수
let topandbottom = {};//상, 하의 선택 저장 변수
let top_style = {};//상의 스타일 저장 변수
let bottom_style = {};//하의 스타일 저장 변수
//프론트엔드에서 사용자가 선택한 정보를 서버에 POST 요청으로 전달하여 저장하도록 변경해야함

app.get('/', (req, res) => {
    res.send('Hello World from the backend server!');
});

//성별 저장
app.post('/optionDecision.html', (req, res) => {
    const { gender } = req.body;
  
    if (!gender) {
      return res.status(400).json({ message: '성별이 선택되지 않았습니다.' });
    }
    console.log(`성별: ${selectedGender}`);
    gender = selectedGender;
    res.status(200).json({ message: `성별 ${selectedGender}이 저장되었습니다.` });
});

//키, 몸무게 저장
app.post("/optionPhyInfo.html", (req, res) => {
    const { stature, weight } = req.body;
  
    if (!stature || !weight || isNaN(stature) || isNaN(weight)) {
      return res.status(400).json({ message: "숫자만 입력 가능합니다." });
    }
  
    physicalInfo = { stature, weight };
  
    res.status(200).json({ message: "신체 정보가 저장되었습니다.", physicalInfo });
});

//저장한 성별, 신체정보(키,몸무게), 상하의 선택, 상의OR하의 스타일 저장
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

//서버 시작
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
