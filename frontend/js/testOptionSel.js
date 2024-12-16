let userInfo = {}; // 사용자 정보 저장
let selectedTop = null; // 선택한 상의
let selectedBottom = null; // 선택한 하의
let currentStep = ""; // 현재 단계 (상의 또는 하의 추천)

// 성별 선택 처리
function selectGender(gender) {
  // 해당 성별의 라디오 버튼 선택
  document.querySelector(
    `input[name="gender"][value="${gender}"]`
  ).checked = true;
}

// 섹션 이동 함수
function showSection(sectionId) {
  document.querySelectorAll(".option-section").forEach((section) => {
    section.classList.remove("active"); // 모든 섹션 숨김
  });
  document.getElementById(sectionId).classList.add("active"); // 선택된 섹션만 표시
}

// 다음 섹션으로 이동
function nextSection(nextSectionId) {
  const gender = document.querySelector('input[name="gender"]:checked'); // 선택된 성별

  // 성별 선택 확인
  if (nextSectionId === "heightWeightSection" && !gender) {
    alert("성별을 선택해주세요.");
    return;
  }

  // 키와 몸무게 입력 확인
  if (nextSectionId === "categorySection") {
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;

    if (!height || !weight) {
      alert("키와 몸무게를 입력해주세요.");
      return;
    }

    // 사용자 정보 저장
    userInfo.gender = gender.value;
    userInfo.height = height;
    userInfo.weight = weight;
  }

  // 스타일 카테고리 선택 확인
  if (nextSectionId === "itemTypeSelectionSection") {
    const category = document.getElementById("category").value;

    if (!category) {
      alert("스타일 카테고리를 선택해주세요.");
      return;
    }

    userInfo.category = category; // 사용자 정보에 스타일 카테고리 추가
  }

  showSection(nextSectionId); // 다음 섹션으로 이동
}

// 이전 섹션으로 이동
function prevSection(currentSectionId, previousSectionId) {
  showSection(previousSectionId); // 이전 섹션으로 이동
}

// AI 서버로 데이터 전송 및 추천받기
async function requestRecommendation(type) {
  currentStep = type; // 현재 단계 저장
  try {
    const response = await fetch("http://khs.uy.to:8000/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...userInfo, type }), // 사용자 정보와 추천 타입 전송
    });

    if (!response.ok) {
      throw new Error(`추천 실패: ${response.status}`);
    }

    const result = await response.json();
    displayRecommendations(result.recommendations, type); // 추천 결과 표시
  } catch (error) {
    console.error("추천 오류:", error.message);
    alert("AI 서버와 통신 중 오류가 발생했습니다.");
  }
}

// 추천 결과 표시
function displayRecommendations(items, type) {
  const container = document.getElementById("recommendationResults");
  container.innerHTML = items
    .map(
      (item, index) => `
          <div class="recommendation-item" onclick="selectItem('${type}', ${index})">
            <img src="${item.image}" alt="${item.name}" id="${type}-item-${index}" />
            <p>${item.name}</p>
          </div>`
    )
    .join("");

  showSection("recommendationSection"); // 추천 결과 섹션 표시
}
// 항목 선택 처리
function selectItem(type, index) {
  const items = document.querySelectorAll(`#recommendationResults img`);
  items.forEach((item) => item.classList.remove("selected")); // 이전 선택 해제

  const selectedItem = document.getElementById(`${type}-item-${index}`);
  selectedItem.classList.add("selected"); // 새로 선택된 항목 표시

  // 선택한 항목 저장
  if (type === "top") {
    selectedTop = index; // 상의 선택
  } else {
    selectedBottom = index; // 하의 선택
  }
}

// 선택 완료 후 다음 단계로 이동
function submitChoice() {
  // 상의를 선택했을 경우 하의 추천 요청
  if (currentStep === "top" && selectedTop !== null) {
    requestRecommendation("bottom");
  }
  // 하의를 선택했을 경우 최종 세트 표시
  else if (currentStep === "bottom" && selectedBottom !== null) {
    displayFinalSet();
  }
  // 항목 선택이 안 된 경우 경고
  else {
    alert("항목을 선택해주세요.");
  }
}

// 최종 세트 표시
function displayFinalSet() {
  const finalSetContainer = document.getElementById("finalSet");

  // 선택된 상의와 하의 가져오기
  const selectedTopItem = document.querySelector(`#top-item-${selectedTop}`);
  const selectedBottomItem = document.querySelector(
    `#bottom-item-${selectedBottom}`
  );

  // 최종 세트 내용 설정
  finalSetContainer.innerHTML = `
          <div>
            <h4>상의</h4>
            ${selectedTopItem ? selectedTopItem.outerHTML : "선택 안됨"}
          </div>
          <div>
            <h4>하의</h4>
            ${selectedBottomItem ? selectedBottomItem.outerHTML : "선택 안됨"}
          </div>
        `;

  showSection("resultSection"); // 최종 세트 섹션 표시
}

// 다시 시작
function restart() {
  userInfo = {}; // 사용자 정보 초기화
  selectedTop = null; // 선택한 상의 초기화
  selectedBottom = null; // 선택한 하의 초기화
  currentStep = ""; // 현재 단계 초기화
  showSection("genderSelectionSection"); // 성별 선택 섹션으로 이동
}
