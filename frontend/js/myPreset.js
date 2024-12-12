document.addEventListener("DOMContentLoaded", () => {
  fetchPresets();
});

// 프리셋 데이터를 가져오기 위한 함수
function fetchPresets() {
  /*
  const token = localStorage.getItem("token");
  if (!token) {
    alert("로그인이 필요합니다.");
    window.location.href = "/login.html";
    return;
  }
  */

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
      // 응답 데이터가 배열인지 객체인지 확인
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
          <div class="preset-header">
            <div>저장한 날짜: ${new Date(
              preset.created_at
            ).toLocaleString()}</div>
            <div>
              <button class="button settings-button" onclick="openSettings(${
                preset.user_closet_id
              })">설정정보</button>
              <button class="button delete-button" onclick="deletePreset(${
                preset.user_closet_id
              })">삭제</button>
            </div>
          </div>
          <div class="item">
            <div>스타일: ${preset.style}</div>
            <div>상의 ID: ${preset.top_clothing_id}</div>
            <div>하의 ID: ${preset.bottom_clothing_id}</div>
          </div>
        </div>`
    )
    .join("");
}

// 프리셋이 없을 때 렌더링
function renderNoPresets() {
  const container = document.getElementById("preset-container");
  container.innerHTML = "<p>저장된 프리셋이 없습니다.</p>";
}

// 프리셋 삭제
function deletePreset(userClosetId) {
  if (confirm("정말로 삭제하시겠습니까?")) {
    const token = localStorage.getItem("token");
    fetch(`http://khs.uy.to:3000/api/clothing_presets/${userClosetId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("삭제에 실패했습니다.");
        }
        alert("프리셋이 삭제되었습니다.");
        fetchPresets(); // 데이터 갱신
      })
      .catch((error) => {
        console.error("삭제 중 오류 발생:", error);
        alert("삭제 중 오류가 발생했습니다.");
      });
  }
}

// 설정 정보 보기
function openSettings(userClosetId) {
  alert(`프리셋 ID ${userClosetId}의 설정 정보를 여기에 표시합니다.`);
}
