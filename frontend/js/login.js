// 로그인 요청 처리 함수
async function handleLogin(event) {
    event.preventDefault(); // 기본 폼 제출 방지
  
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    // ID와 비밀번호가 입력되지 않은 경우 처리
    if (!email || !password) {
      document.getElementById("login_error_message").textContent =
        "ID와 비밀번호를 입력해주세요.";
      return;
    }
  
    const loginData = { email, password };
  
    try {
      // 서버에 로그인 요청 보내기
      const response = await fetch('http://khs.uy.to:3000/api/login', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginData),
      });
  
      const result = await response.json();
  
      if (response.status === 200) {
        console.log("서버 응답 확인:", result); // 서버 응답 로그 출력
      
        if (result.user_id && !isNaN(result.user_id)) {
          // 로그인 성공: 로컬스토리지에 저장
          localStorage.setItem("token", result.token);
          localStorage.setItem("username", result.username);
          localStorage.setItem("user_id", result.user_id);
      
          alert(`${result.username}님 환영합니다!`);
          window.location.href = "index.html"; // 메인 페이지로 이동
        } else {
          console.error("유효하지 않은 user_id:", result.user_id);
          document.getElementById("login_error_message").textContent =
            "로그인 처리 중 오류가 발생했습니다.";
        }
      } else {
        document.getElementById("login_error_message").textContent =
          result.message || "로그인 실패";
      }
      
    } catch (error) {
      // 요청 실패 시 에러 처리
      console.error("Error during login:", error);
      document.getElementById("login_error_message").textContent =
        "서버 오류가 발생했습니다.";
    }
  }
  
  // 로그인 버튼 클릭 시 로그인 처리
  document.getElementById("loginButton").addEventListener("click", handleLogin);
  