let userInfo = {}; // 사용자 정보 저장 객체
let selectedTop = null; // 선택한 상의 ID
let selectedBottom = null; // 선택한 하의 ID
let isTopFirst = true; // 추천 시작 순서 판단 (true: 상의 먼저, false: 하의 먼저)

function showSection(sectionId) {
  // 모든 옵션 섹션 비활성화
  document.querySelectorAll(".option-section").forEach((section) => {
    section.classList.remove("active");
  });
  // 지정된 섹션 활성화
  document.getElementById(sectionId).classList.add("active");
}

function nextSection(nextSectionId) {
  // 각 입력값 유효성 검사
  if (nextSectionId === "heightWeightSection") {
    const gender = document.getElementById("gender").value;
    if (!gender) {
      alert("성별을 선택해주세요."); // 성별 입력 체크
      return;
    }
  } else if (nextSectionId === "styleSection") {
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    if (!height || !weight) {
      alert("키와 몸무게를 입력해주세요."); // 키와 몸무게 입력 체크
      return;
    }
  } else if (nextSectionId === "recommendationOrderSection") {
    const style = document.getElementById("style").value;
    if (!style) {
      alert("스타일을 선택해주세요."); // 스타일 입력 체크
      return;
    }
  }

  // 유효성 검사를 통과하면 다음 섹션으로 이동
  showSection(nextSectionId);
}

function previousSection(previousSectionId) {
  // 이전 섹션으로 이동
  showSection(previousSectionId);
}

function startRecommendation() {
  // 사용자 정보 수집
  const gender = document.getElementById("gender").value;
  const height = document.getElementById("height").value;
  const weight = document.getElementById("weight").value;
  const style = document.getElementById("style").value;
  const recommendationOrder = document.getElementById("recommendationOrder").value;

  // 모든 정보 입력 체크
  if (!gender || !height || !weight || !style || !recommendationOrder) {
    alert("모든 정보를 입력해주세요.");
    return;
  }

  // 사용자 정보를 객체에 저장
  userInfo = { gender, height, weight, style, recommendationOrder };

  // 선택한 순서에 따라 추천 시작
  requestRecommendation(recommendationOrder);
}

async function requestRecommendation(type) {
  // 사용자 ID를 로컬 스토리지에서 가져옴
  const token = localStorage.getItem("token");
  const user_id = token ? parseInt(localStorage.getItem("user_id"), 10) : null;
  // 서버에 보낼 데이터 설정
  const payload = {
    user_id: user_id,
    gender: userInfo.gender,
    height: parseInt(userInfo.height, 10),
    weight: parseInt(userInfo.weight, 10),
    style: userInfo.style,
    clothingType: type,
  };

  console.log("Payload sent to the server:", payload); // 확인용 로그

  try {
    // 추천 요청을 서버에 전송
    const aiResponse = await fetch("http://khs.uy.to:8000/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    // 응답 상태 체크
    if (!aiResponse.ok) {
      const errorMessage = await aiResponse.text();
      console.error("추천 요청 실패:", errorMessage);
      alert(`추천 요청 실패: ${errorMessage}`);
      return;
    }

    // 추천 결과 처리
    const aiData = await aiResponse.json();
    console.log("추천 결과:", aiData);

    if (aiData.recommendations.length > 0) {
      displayRecommendations(aiData.recommendations, type); // 추천 데이터 표시
    } else {
      alert("추천 결과가 없습니다."); // 추천 결과가 없을 경우 경고
    }
  } catch (error) {
    console.error("추천 요청 중 오류 발생:", error.message);
    alert("추천 요청 중 오류 발생."); // 요청 중 오류 발생 시 경고
  }
}

function displayRecommendations(items, type) {
  // 추천 결과를 화면에 표시
  const container = document.getElementById("recommendationResults");
  container.innerHTML = items
    .map(
      (item) => `
                  <div class="recommendation-item" onclick="selectItem('${type}', '${item.id}')">
                    <img src="${item.이미지_URL}" alt="${item.id}" />
                    <p>${item.상품명}</p>
                  </div>`
    )
    .join("");
  // 추천 섹션으로 이동
  showSection("recommendationSection");
}

function selectItem(type, id) {
  // 기존 선택 상태 초기화
  document.querySelectorAll(".recommendation-item img").forEach((img) => {
    img.classList.remove("selected");
  });

  // 선택한 항목 강조 표시
  const selectedImage = document.querySelector(`.recommendation-item img[alt="${id}"]`);
  if (selectedImage) {
    selectedImage.classList.add("selected");

    // 선택한 아이템 ID 저장
    if (type === "상의") {
      selectedTop = id; // 상의 ID 저장
      userInfo.recommendationOrder = "하의"; // 다음 추천은 하의
      console.log("Selected Top ID:", selectedTop);
    } else if (type === "하의") {
      selectedBottom = id; // 하의 ID 저장
      userInfo.recommendationOrder = "상의"; // 다음 추천은 상의
      console.log("Selected Bottom ID:", selectedBottom);
    }
  } else {
    console.error("선택한 항목을 찾을 수 없습니다."); // 선택한 항목이 없을 경우 에러 로그
  }
}

function confirmSelection() {
  if (isTopFirst) {
    // 상의를 먼저 추천받은 경우
    if (!selectedTop) {
      alert("먼저 상의를 선택해주세요."); // 상의 선택 체크
      return;
    }
    if (!selectedBottom) {
      console.log("상의 선택 완료. 하의 추천 시작.");
      requestRecommendation("하의"); // 하의 추천 요청
    } else {
      goToClothingSet(); // 최종 결과를 표시하는 함수 호출
    }
  } else {
    // 하의를 먼저 추천받은 경우
    if (!selectedBottom) {
      alert("먼저 하의를 선택해주세요."); // 하의 선택 체크
      return;
    }
    if (!selectedTop) {
      console.log("하의 선택 완료. 상의 추천 시작.");
      requestRecommendation("상의"); // 상의 추천 요청
    } else {
      goToClothingSet(); // 최종 결과를 표시하는 함수 호출
    }
  }
}

function restart() {
  // 모든 변수 초기화
  userInfo = {};
  selectedTop = null;
  selectedBottom = null;
  isTopFirst = true;
  showSection("genderSection"); // 성별 섹션으로 이동
}

function goToClothingSet() {
  // 상의와 하의를 모두 선택했는지 체크
  if (!selectedTop && !selectedBottom) {
    alert("상의와 하의를 모두 선택해주세요."); // 선택 체크
    return;
  }

  // 최종 결과 페이지로 이동
  const url = `clothing_set.html?top=${encodeURIComponent(
    selectedTop
  )}&bottom=${encodeURIComponent(selectedBottom)}&gender=${encodeURIComponent(
    userInfo.gender
  )}&height=${encodeURIComponent(userInfo.height)}&weight=${encodeURIComponent(
    userInfo.weight
  )}&style=${encodeURIComponent(userInfo.style)}`;
  window.location.href = url; // 결과 페이지로 이동
}
