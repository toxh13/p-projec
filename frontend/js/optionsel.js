let userInfo = {}; // 사용자 정보 저장 객체 (성별, 키, 몸무게, 스타일 등 사용자 입력값 저장)
let selectedTop = null; // 선택한 상의 ID 저장
let selectedBottom = null; // 선택한 하의 ID 저장
let isTopFirst = true; // 추천 시작 순서 (true: 상의 먼저, false: 하의 먼저)

/**
 * 특정 섹션만 활성화하는 함수
 * @param {string} sectionId - 활성화하려는 섹션의 ID
 */
function showSection(sectionId) {
  document.querySelectorAll(".option-section").forEach((section) => {
    section.classList.remove("active");
  });
  document.getElementById(sectionId).classList.add("active");
}

/**
 * 입력값 유효성 검증 후 다음 섹션으로 이동
 * @param {string} nextSectionId - 이동할 섹션 ID
 */
function nextSection(nextSectionId) {
  if (nextSectionId === "heightWeightSection") {
    const gender = document.getElementById("gender").value;
    if (!gender) {
      alert("성별을 선택해주세요.");
      return;
    }
  } else if (nextSectionId === "styleSection") {
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    if (!height || !weight) {
      alert("키와 몸무게를 입력해주세요.");
      return;
    }
  } else if (nextSectionId === "recommendationOrderSection") {
    const style = document.getElementById("style").value;
    if (!style) {
      alert("스타일을 선택해주세요.");
      return;
    }
  }
  showSection(nextSectionId);
}

/**
 * 이전 섹션으로 돌아가기
 * @param {string} previousSectionId - 돌아갈 섹션 ID
 */
function previousSection(previousSectionId) {
  showSection(previousSectionId);
}

/**
 * 추천 시작 함수
 */
function startRecommendation() {
  const gender = document.getElementById("gender").value;
  const height = document.getElementById("height").value;
  const weight = document.getElementById("weight").value;
  const style = document.getElementById("style").value;
  const recommendationOrder = document.getElementById("recommendationOrder").value;

  if (!gender || !height || !weight || !style || !recommendationOrder) {
    alert("모든 정보를 입력해주세요.");
    return;
  }

  userInfo = { gender, height, weight, style };
  isTopFirst = recommendationOrder === "상의";
  requestRecommendation(isTopFirst ? "상의" : "하의");
}

/**
 * 추천 요청 함수
 * @param {string} type - 추천 요청 타입 ("상의" 또는 "하의")
 */
async function requestRecommendation(type) {
  const token = localStorage.getItem("token");
  const user_id = token ? parseInt(localStorage.getItem("user_id"), 10) : null;

  const payload = {
    user_id,
    gender: userInfo.gender,
    height: parseInt(userInfo.height, 10),
    weight: parseInt(userInfo.weight, 10),
    style: userInfo.style,
    clothingType: type,
  };

  try {
    const aiResponse = await fetch("http://khs.uy.to:8000/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!aiResponse.ok) {
      const errorMessage = await aiResponse.text();
      alert(`추천 요청 실패: ${errorMessage}`);
      return;
    }

    const aiData = await aiResponse.json();
    if (aiData.recommendations.length > 0) {
      displayRecommendations(aiData.recommendations, type);
    } else {
      alert("추천 결과가 없습니다.");
    }
  } catch (error) {
    alert("추천 요청 중 오류 발생.");
  }
}

/**
 * 추천 결과 표시 함수
 */
function displayRecommendations(items, type) {
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
  showSection("recommendationSection");
}

/**
 * 추천 아이템 선택 함수
 */
function selectItem(type, id) {
  document.querySelectorAll(".recommendation-item img").forEach((img) => {
    img.classList.remove("selected");
  });

  const selectedImage = document.querySelector(`.recommendation-item img[alt="${id}"]`);
  if (selectedImage) {
    selectedImage.classList.add("selected");
    if (type === "상의") {
      selectedTop = id;
    } else if (type === "하의") {
      selectedBottom = id;
    }
  }
}

/**
 * 선택 확인 및 다음 단계로 이동
 */
function confirmSelection() {
  if (isTopFirst) {
    if (!selectedTop) {
      alert("먼저 상의를 선택해주세요.");
      return;
    }
    if (!selectedBottom) {
      requestRecommendation("하의");
    } else {
      goToClothingSet();
    }
  } else {
    if (!selectedBottom) {
      alert("먼저 하의를 선택해주세요.");
      return;
    }
    if (!selectedTop) {
      requestRecommendation("상의");
    } else {
      goToClothingSet();
    }
  }
}

/**
 * 최종 결과 페이지로 이동
 */
function goToClothingSet() {
  if (!selectedTop || !selectedBottom) {
    alert("상의와 하의를 모두 선택해주세요.");
    return;
  }

  const url = `clothing_set.html?top=${encodeURIComponent(selectedTop)}&bottom=${encodeURIComponent(selectedBottom)}&gender=${encodeURIComponent(userInfo.gender)}&height=${encodeURIComponent(userInfo.height)}&weight=${encodeURIComponent(userInfo.weight)}&style=${encodeURIComponent(userInfo.style)}`;
  window.location.href = url;
}

/**
 * 초기화 및 재시작
 */
function restart() {
  userInfo = {};
  selectedTop = null;
  selectedBottom = null;
  isTopFirst = true;
  showSection("genderSection");
}
