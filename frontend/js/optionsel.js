let currentOptionIndex = 0;

// 옵션 보이기
function showNextOption() {
  const currentOption = document.getElementById(`option${currentOptionIndex + 1}`);
  if (currentOption) {
    currentOption.style.display = "block";
  }
}

// 옵션 선택
function selectOption(optionId, selectedOption) {
  alert(`${selectedOption}을 선택하셨습니다.`);
  document.getElementById(optionId).style.display = "none";
  currentOptionIndex++;
  showNextOption();
}

// 신체 정보 입력 확인
function selectOptionInput(optionID) {
  const stature = document.getElementById("option_stature").value;
  const weight = document.getElementById("option_weight").value;

  if (!isNaN(stature) && !isNaN(weight) && stature && weight) {
    alert(`키: ${stature}, 몸무게: ${weight}가 입력되었습니다.`);
    document.getElementById(optionID).style.display = "none";
    currentOptionIndex++;
    showNextOption();
  } else {
    alert("숫자만 입력해주세요.");
  }
}

// 뒤로 가기
function goBack(currentOptionId, previousOptionId) {
  document.getElementById(currentOptionId).style.display = "none";
  document.getElementById(previousOptionId).style.display = "block";
  currentOptionIndex--;
}

// 상의 스타일 선택
function showTopClothing(category) {
  const categoryButtons = document.getElementById("categoryButtons");
  const clothingOptions = document.getElementById("clothingOptions");

  categoryButtons.classList.add("hidden");
  clothingOptions.classList.remove("hidden");

  document.getElementById("selectedCategory").innerText = category;

  const clothingItems = {
    캐주얼: ["니트", "맨투맨", "후드티"],
    스트릿: ["오버사이즈 티셔츠", "조거 팬츠", "스니커즈"],
    미니멀: ["슬랙스", "니트", "셔츠"],
    워크웨어: ["작업복", "카고 팬츠", "부츠"],
    스포티: ["운동복", "레깅스", "스포츠 브라"],
    클래식: ["블레이저", "드레스 셔츠", "치노 팬츠"],
    시크: ["블랙 원피스", "가죽 자켓", "하이힐"],
    로맨틱: ["레이스 블라우스", "플레어 스커트", "샌들"],
    시티보이: ["후드 집업", "반바지", "캡"],
    레트로: ["빈티지 티셔츠", "데님 재킷", "와이드 팬츠"],
  };

  const items = clothingItems[category];
  const clothingDiv = document.getElementById("clothingItems");
  clothingDiv.innerHTML = ""; // 초기화

  items.forEach((item) => {
    const button = document.createElement("button");
    button.textContent = item;
    clothingDiv.appendChild(button);
  });
}

// 재추천
function recommend() {
  alert("추천 항목을 새로 제공합니다.");
}

// 페이지 로드 시 첫 번째 옵션 보여주기
window.onload = function () {
  showNextOption();
};
