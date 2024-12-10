async function handleMyPresetClick(event) {
  event.preventDefault();

  const token = localStorage.getItem("token"); //토큰 가져오기

  if (!token) {
    alert("로그인 후 이용가능합니다.");
    window.location.href = "/login";
    return;
  }

  try {
    const response = await fetch("/myPreset", {
      method: "GET",
      headers: {
        Authorization: token,
      },
    });

    if (response.ok) {
      window.location.href = "/myPreset"; //내옷장 페이지로 이동
    } else if (response.status === 401 || response.status === 403) {
      alert("로그인 후 이용가능합니다.");
      window.location.href = "/login"; //로그인 페이지로 이동
    } else {
      alert("오류가 발생했습니다. 다시 시도해주세요.");
    }
  } catch (error) {
    console.error("내 옷장 요청 실패:", error);
    alert("오류가 발생했습니다. 다시 시도해주세요.");
  }
}
