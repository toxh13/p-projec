// myPreset.js

document.addEventListener("DOMContentLoaded", () => {
    fetchPresets();
  });
  
  // 프리셋 데이터를 가져오기 위한 함수
  function fetchPresets() {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("로그인이 필요합니다.");
      window.location.href = "/login.html";
      return;
    }
  
    fetch("http://khs.uy.to:3000/api/clothing_presets", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP 상태 코드: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        const presets = Array.isArray(data) ? data : data.data;
        if (!presets || presets.length === 0) {
          renderNoPresets();
          return;
        }
        renderPresets(presets);
      })
      .catch((error) => {
        console.error("프리셋 데이터를 가져오는 중 오류:", error);
        alert(`프리셋을 불러오는 중 오류가 발생했습니다: ${error.message}`);
      });
  }
  
  // 프리셋 데이터를 렌더링
  function renderPresets(presets) {
    const container = document.getElementById("preset-container");
  
    container.innerHTML = presets
      .map(
        (preset) => `
          <div class="preset">
            <!-- 의류 정보 -->
            <div class="clothing-info">
              <div class="item">
                <img src="${preset.top_image_url || "#"}" alt="상의 이미지" />
                <div>
                  <div><strong>상품명:</strong> ${preset.top_name || "정보 없음"}</div>
                  <div><strong>브랜드:</strong> ${preset.top_brand || "정보 없음"}</div>
                   <div><strong>구매링크:</strong> ${
              preset.top_purchase
                ? `<a href="${preset.top_purchase}" target="_blank">구매하기</a>`
                : "정보 없음"
            }</div>
                </div>
              </div>
              <div class="item">
                <img src="${preset.bottom_image_url || "#"}" alt="하의 이미지" />
                <div>
                  <div><strong>상품명:</strong> ${preset.bottom_name || "정보 없음"}</div>
                  <div><strong>브랜드:</strong> ${preset.bottom_brand || "정보 없음"}</div>
                   <div><strong>구매링크:</strong> ${
              preset.bottom_purchase
                ? `<a href="${preset.bottom_purchase}" target="_blank">구매하기</a>`
                : "정보 없음"
            }</div>
                </div>
              </div>
              <div class="button-container">
                    <button class="button delete-button" onclick="deletePreset(${preset.user_closet_id})">
                      삭제
                    </button>
                    <button class="button" onclick="toggleDetails(${preset.user_closet_id}, '${preset.style}', ${preset.height}, ${preset.weight}, '${preset.sex}')">
                      세부정보
                    </button>
                  </div>
                </div>
            <!-- 세부 정보 (숨김 상태) -->
            <div id="details-box-${preset.user_closet_id}" class="details-box"></div>
          </div>`
      )
      .join("");
  }
  
  // 세부 정보 표시
  function toggleDetails(userClosetId, style, height, weight, sex) {
    const detailsBox = document.getElementById(`details-box-${userClosetId}`);
    detailsBox.style.display =
      detailsBox.style.display === "none" ? "block" : "none";
    if (detailsBox.style.display === "block") {
      detailsBox.innerHTML = `
        <h3>세부 정보</h3>
        <p><strong>스타일:</strong> ${style}</p>
        <p><strong>키:</strong> ${height}cm</p>
        <p><strong>몸무게:</strong> ${weight}kg</p>
        <p><strong>성별:</strong> ${sex}</p>
      `;
    }
  }
  
  // 프리셋이 없을 때 렌더링
  function renderNoPresets() {
    const container = document.getElementById("preset-container");
    container.innerHTML = "<p>저장된 프리셋이 없습니다.</p>";
  }
  
  // 삭제 API 호출 후 UI에서 삭제된 프리셋을 제거
  function deletePreset(userClosetId) {
    if (confirm("정말로 삭제하시겠습니까?")) {
      const token = localStorage.getItem("token");
      fetch(`http://khs.uy.to:3000/api/user_closets/${userClosetId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`삭제 실패 (HTTP 상태 코드: ${response.status})`);
          }
          alert("프리셋이 삭제되었습니다.");
          window.location.reload(); // 페이지 새로고침
        })
        .catch((error) => {
          console.error("삭제 중 오류 발생:", error);
          alert("삭제 중 오류가 발생했습니다.");
        });
    }
  }
  // 세부 정보 표시 (모달)
  function toggleDetails(userClosetId, style, height, weight, sex) {
    const modal = document.getElementById("modal");
    const modalDetails = document.getElementById("modal-details");

    modal.style.display = "flex"; // 모달을 표시
    modalDetails.innerHTML = `
          <h3>세부 정보</h3>
          <p><strong>스타일:</strong> ${style}</p>
          <p><strong>키:</strong> ${height}cm</p>
          <p><strong>몸무게:</strong> ${weight}kg</p>
          <p><strong>성별:</strong> ${sex}</p>
      `;
  }

  // 모달 닫기 함수
  function closeModal() {
    const modal = document.getElementById("modal");
    modal.style.display = "none"; // 모달 숨기기
  }

  // 모달 외부 클릭 시 닫기
  window.onclick = function (event) {
    const modal = document.getElementById("modal");
    if (event.target == modal) {
      closeModal(); // 모달이 외부 클릭 시 닫힘
    }
  };