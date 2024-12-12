// navbar.js: 네비게이션 동적 로드 및 상태 업데이트
document.addEventListener("DOMContentLoaded", async () => {
  const navContainer = document.getElementById("nav-container");

  // nav.html 로드
  try {
    const response = await fetch("nav.html");
    const navHtml = await response.text();
    navContainer.innerHTML = navHtml;

    // 네비게이션 상태 업데이트
    const navbarItems = document.getElementById("navbar_items");
    const token = localStorage.getItem("token"); // JWT 토큰
    const username = localStorage.getItem("username"); // 사용자 이름

    if (token && username) {
      // 로그인 상태
      navbarItems.innerHTML = `
        <li class="nav-item">
          <a class="nav-link" href="#" onclick="checkLoginAndRedirect('myPreset.html')">내스타일</a>
        </li>
        <li class="nav-item">
          <span class="nav-link">현재 로그인 정보:${username}</span>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" onclick="handleLogout()">로그아웃</a>
        </li>
      `;
    } else {
      // 비로그인 상태
      navbarItems.innerHTML = `
        <li class="nav-item">
          <a class="nav-link" href="#" onclick="checkLoginAndRedirect('myPreset.html')">내스타일</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="join.html">회원가입</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="login.html">로그인</a>
        </li>
      `;
    }
  } catch (error) {
    console.error("nav.html 로드 중 오류 발생:", error);
  }
});

// 로그아웃 처리
function handleLogout() {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  alert("로그아웃되었습니다.");
  window.location.href = "index.html"; // 메인 페이지로 리디렉션
}

// 로그인 확인 및 리디렉션 처리 (내스타일 전용)
function checkLoginAndRedirect(targetPage) {
  const token = localStorage.getItem("token");

  if (token) {
    // 로그인 상태
    window.location.href = targetPage;
  } else {
    // 비로그인 상태
    alert("로그인이 필요한 서비스입니다.");
    window.location.href = "login.html"; // 로그인 페이지로 리디렉션
  }
}