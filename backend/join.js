document.getElementById("joinForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const emailDomain = document.getElementById("emailDomain").value;
  const fullEmail = `${email}@${emailDomain}`;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;
  const username = document.getElementById("username").value;

  // 비밀번호 일치 확인
  if (password !== confirmPassword) {
    alert("비밀번호가 일치하지 않습니다.");
    return;
  }

  // 회원가입 데이터 전송
  fetch("http://khs.uy.to:3000/api/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: fullEmail,
      password: password,
      username: username,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === "회원가입 성공") {
        alert("회원가입이 완료되었습니다.");
        window.location.href = "login.html"; // 로그인 페이지로 리디렉션
      } else {
        alert(data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("서버 오류가 발생했습니다.");
    });
});
