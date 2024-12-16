// utils.js

function printLocalStorage() {
    console.log("LocalStorage 데이터 확인:");
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      const value = localStorage.getItem(key);
      console.log(`${key}: ${value}`);
    }
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    console.log("페이지 로드 시 로컬스토리지 내용 확인:");
    printLocalStorage();
  });
  