const API_BASE_URL = "http://khs.uy.to:3000";

      // URL 파라미터에서 데이터 가져오기
      function getQueryParams() {
        const params = new URLSearchParams(window.location.search);
        return {
          top_clothing_id: params.get("top"),
          bottom_clothing_id: params.get("bottom"),
          gender: params.get("gender"),
          height: params.get("height"),
          weight: params.get("weight"),
          style: params.get("style"),
        };
      }

      const userSelection = getQueryParams();
      console.log("User Selection:", userSelection);

      function checkLoginStatus() {
        const token = localStorage.getItem("token");
        return !!token;
      }

      async function displayClothingSet(ids) {
        const container = document.getElementById("set-container");
        const saveButton = document.getElementById("save-preset-btn");

        if (checkLoginStatus()) {
          saveButton.classList.remove("hidden");
        }

        try {
          const [topResponse, bottomResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/api/clothing/${ids.top_clothing_id}`),
            fetch(`${API_BASE_URL}/api/clothing/${ids.bottom_clothing_id}`),
          ]);

          if (!topResponse.ok || !bottomResponse.ok) {
            throw new Error("의류 데이터를 가져오는 데 실패했습니다.");
          }

          const topData = await topResponse.json();
          const bottomData = await bottomResponse.json();

          const topItem = `
            <div class="item">
              <img src="${topData.image_url}" alt="${topData.name}" />
              <div class="item-info">
                <p class="custom-heading">상의: ${topData.name}</p>
                <p class="custom-body">${
                  topData.brand ? "브랜드: " + topData.brand : "브랜드 정보 없음"
                }</p>
                <p class="custom-body">가격: ${
                  topData.price ? topData.price + "원" : "가격 정보 없음"
                }</p>
              </div>
              <button class="link-button" onclick="window.open('${
                topData.purchase_link
              }', '_blank')">보러가기</button>
            </div>
          `;

          const bottomItem = `
            <div class="item">
              <img src="${bottomData.image_url}" alt="${bottomData.name}" />
              <div class="item-info">
                <p class="custom-heading">하의: ${bottomData.name}</p>
                <p class="custom-body">${
                  bottomData.brand
                    ? "브랜드: " + bottomData.brand
                    : "브랜드 정보 없음"
                }</p>
                <p class="custom-body">가격: ${
                  bottomData.price ? bottomData.price + "원" : "가격 정보 없음"
                }</p>
              </div>
              <button class="link-button" onclick="window.open('${
                bottomData.purchase_link
              }', '_blank')">보러가기</button>
            </div>
          `;

          container.innerHTML = `
            <h3>추천 스타일: ${userSelection.style || "알 수 없음"}</h3>
            ${topItem}
            ${bottomItem}
          `;

          saveButton.addEventListener("click", () =>
            savePreset(ids, userSelection.style)
          );
        } catch (error) {
          console.error("의류 데이터를 불러오는 중 오류 발생:", error);
          alert("의류 데이터를 가져오는 데 실패했습니다.");
        }
      }

      async function savePreset(ids, style) {
  const gender = userSelection.gender || "알 수 없음"; // 성별 기본값 설정
  console.log("Gender being sent to server:", gender); // 디버깅

  try {
    const response = await fetch(`${API_BASE_URL}/api/user_closets`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({
        top_clothing_id: ids.top_clothing_id,
        bottom_clothing_id: ids.bottom_clothing_id,
        style: style || "알 수 없음",
        weight: userSelection.weight,
        height: userSelection.height,
        gender, // 성별 추가
      }),
    });

    if (response.ok) {
      const result = await response.json();
      alert(`프리셋이 성공적으로 저장되었습니다! (Preset ID: ${result.presetId})`);
    } else {
      const error = await response.json();
      alert(`프리셋 저장 실패: ${error.message}`);
    }
  } catch (error) {
    console.error("프리셋 저장 중 오류 발생:", error);
    alert("프리셋 저장하는 중 문제가 발생했습니다.");
  }
}




function showUserSelection() {
  const { gender, height, weight, style, top_clothing_id, bottom_clothing_id } = userSelection;
  alert(
    `선택 정보:\n\n성별: ${gender}\n키: ${height}cm\n몸무게: ${weight}kg\n스타일: ${style}\n` +
    `상의 ID: ${top_clothing_id}\n하의 ID: ${bottom_clothing_id}`
  );
}

document
  .getElementById("view-selection-btn")
  .addEventListener("click", showUserSelection);

// 재추천 버튼 클릭 시 옵션 선택 페이지로 이동
document
  .getElementById("rercommend-btn")
  .addEventListener("click", () => {
    window.location.href = "optionSelect.html";
  });

// 페이지 로드 시 의류 세트 표시
window.onload = () => {
  if (!userSelection.top_clothing_id || !userSelection.bottom_clothing_id) {
    console.error("의류 ID가 설정되지 않았습니다.");
    return;
  }

  displayClothingSet({
    top_clothing_id: userSelection.top_clothing_id,
    bottom_clothing_id: userSelection.bottom_clothing_id,
  });
};
