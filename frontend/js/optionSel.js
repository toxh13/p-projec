//옵션선택페이지를 카운팅해주는 변수
let currentOptionIndex = 0;

// 페이지 로드 시 첫 번째 옵션 보여주기
window.onload = function () {
  showNextOption();
};

//다음 옵션으로 넘어가게끔 만듦
function showNextOption() {
  if (currentOptionIndex < 6) {
    document.getElementById(`option${currentOptionIndex + 1}`).style.display =
      "block";
  }
}

//선다형 선택창
function selectOption(optionId, selectedOption) {
  alert(selectedOption + "(을)를 선택하였습니다.");
  document.getElementById(optionId).style.display = "none"; // 선택한 옵션 숨기기
  currentOptionIndex++;
  showNextOption(); // 다음 옵션 보기
}

//키,몸무게 입력창
function selectOptionInput(optionID) {
  var stature = document.getElementById("option_stature").value;
  var weight = document.getElementById("option_weight").value;

  //입력값이 숫자인지 확인
  if (!isNaN(stature) && !isNaN(weight) && stature !== "" && weight !== "") {
    alert("키 : " + stature + ", 몸무게 : " + weight + "가 입력되었습니다.");
    document.getElementById(optionID).style.display = "none";
    currentOptionIndex++;
    showNextOption();
  } else {
    alert("올바른 숫자를 입력해주세요.");
  }
}

//뒤로가기 버튼
function goBack(currentoptionID, previousoptionID) {
  //현재옵션 숨기기
  document.getElementById(currentoptionID).style.display = "none";

  //이전 옵션 보이기
  if (previousoptionID) {
    document.getElementById(previousoptionID).style.display = "block";
  }
  currentOptionIndex--;
}

//상의
// 각 카테고리에 대한 상의 상품 목록
const products = {
  캐주얼: [
    { name: "캐주얼 상의 1", img: "image1.jpg" },
    { name: "캐주얼 상의 2", img: "image2.jpg" },
    { name: "캐주얼 상의 3", img: "image3.jpg" },
    { name: "캐주얼 상의 4", img: "image4.jpg" },
    { name: "캐주얼 상의 5", img: "image5.jpg" },
  ],
  스트릿: [
    { name: "스트릿 상의 1", img: "image1.jpg" },
    { name: "스트릿 상의 2", img: "image2.jpg" },
    { name: "스트릿 상의 3", img: "image3.jpg" },
    { name: "스트릿 상의 4", img: "image4.jpg" },
    { name: "스트릿 상의 5", img: "image5.jpg" },
  ],
  미니멀: [
    { name: "미니멀 상의 1", img: "image1.jpg" },
    { name: "미니멀 상의 2", img: "image2.jpg" },
    { name: "미니멀 상의 3", img: "image3.jpg" },
    { name: "미니멀 상의 4", img: "image4.jpg" },
    { name: "미니멀 상의 5", img: "image5.jpg" },
  ],
  워크웨어: [
    { name: "워크웨어 상의 1", img: "image1.jpg" },
    { name: "워크웨어 상의 2", img: "image2.jpg" },
    { name: "워크웨어 상의 3", img: "image3.jpg" },
    { name: "워크웨어 상의 4", img: "image4.jpg" },
    { name: "워크웨어 상의 5", img: "image5.jpg" },
  ],
};

// 각 카테고리에 대한 관련 하의 상품 목록
const relatedProducts = {
  캐주얼: [
    { name: "캐주얼 하의 1", img: "related1.jpg" },
    { name: "캐주얼 하의 2", img: "related2.jpg" },
    { name: "캐주얼 하의 3", img: "related3.jpg" },
  ],
  스트릿: [
    { name: "스트릿 하의 1", img: "related1.jpg" },
    { name: "스트릿 하의 2", img: "related2.jpg" },
    { name: "스트릿 하의 3", img: "related3.jpg" },
  ],
  미니멀: [
    { name: "미니멀 하의 1", img: "related1.jpg" },
    { name: "미니멀 하의 2", img: "related2.jpg" },
    { name: "미니멀 하의 3", img: "related3.jpg" },
  ],
  워크웨어: [
    { name: "워크웨어 하의 1", img: "related1.jpg" },
    { name: "워크웨어 하의 2", img: "related2.jpg" },
    { name: "워크웨어 하의 3", img: "related3.jpg" },
  ],
};

// 추천 상품을 보여주는 함수
function showRecommendations() {
  const category = document.getElementById("category").value;
  if (!category) return; // 카테고리가 선택되지 않으면 함수 종료

  // 선택한 카테고리에 따라 화면 전환
  document.getElementById("category-selection").classList.add("hidden");
  document.getElementById("recommendations").classList.remove("hidden");

  displayItems(products[category]); // 상품 목록 표시
}

// 상품 목록을 랜덤으로 표시하는 함수
function displayItems(itemList) {
  const itemsDiv = document.getElementById("items");
  itemsDiv.innerHTML = ""; // 이전 내용 초기화

  // 랜덤으로 3개의 상품 선택
  const randomItems = itemList.sort(() => 0.5 - Math.random()).slice(0, 3);
  randomItems.forEach((item) => {
    const itemDiv = document.createElement("div");
    itemDiv.className = "item";
    itemDiv.innerHTML = `<img src="${item.img}" alt="${item.name}" width="100"><br>${item.name}`;
    itemDiv.onclick = () => showRelatedRecommendations(item.name); // 클릭 시 관련 하의 추천
    itemsDiv.appendChild(itemDiv);
  });
}

// 재추천 기능
function reRecommend() {
  const category = document.getElementById("category").value;
  displayItems(products[category]); // 선택한 카테고리에서 상품 재추천
}

// 카테고리 선택 화면으로 돌아가는 함수
function goBackToCategory() {
  document.getElementById("recommendations").classList.add("hidden");
  document.getElementById("category-selection").classList.remove("hidden");
}

// 관련 하의 추천을 보여주는 함수
function showRelatedRecommendations(selectedItem) {
  const category = document.getElementById("category").value;

  //추천 상품 화면 숨기기
  document.getElementById("recommendations").classList.add("hidden");

  //관련 하의 추천 화면 표시
  document.getElementById("related-recommendations").classList.remove("hidden");

  displayRelatedItems(relatedProducts[category]); // 관련 하의 표시
}

// 하의 선택 시 이전 옵션 숨기고 option5로 이동하도록 수정
itemDiv.onclick = () => {
  document.getElementById("related-recommendations").style.display = "none"; // 하의 추천 숨기기
  // 여기에 맞춤 스타일 화면으로 이동하는 코드 추가
  document.getElementById("option5").style.display = "block"; // option5 보이기
  currentOptionIndex = 4; // 현재 옵션 인덱스 업데이트
};

// 관련 하의 목록을 랜덤으로 표시하는 함수
function displayRelatedItems(relatedItemList) {
  const relatedItemsDiv = document.getElementById("related-items");
  relatedItemsDiv.innerHTML = ""; // 이전 내용 초기화

  // 랜덤으로 3개의 관련 하의 선택
  const randomRelatedItems = relatedItemList
    .sort(() => 0.5 - Math.random())
    .slice(0, 3);
  randomRelatedItems.forEach((item) => {
    const itemDiv = document.createElement("div");
    itemDiv.className = "item";
    itemDiv.innerHTML = `<img src="${item.img}" alt="${item.name}" width="100"><br>${item.name}`;

    // 하의 선택 시 이전 옵션 숨기고 다음 옵션으로 이동
    itemDiv.onclick = () => {
      document.getElementById("related-recommendations").style.display = "none"; // 하의 추천 숨기기
      document.getElementById("option5").style.display = "block"; // option5 보이기
      currentOptionIndex = 4; // 현재 옵션 인덱스 업데이트
      //showNextOption(); // 다음 옵션으로 이동
    };

    relatedItemsDiv.appendChild(itemDiv);
  });
}

// 관련 하의 재추천 기능
function relatedReRecommend() {
  const category = document.getElementById("category").value;
  displayRelatedItems(relatedProducts[category]); // 선택한 카테고리에서 관련 하의 재추천
}

// 추천 상품 화면으로 돌아가는 함수
function goBackToRecommendations() {
  document.getElementById("related-recommendations").classList.add("hidden");
  document.getElementById("recommendations").classList.remove("hidden");
}
