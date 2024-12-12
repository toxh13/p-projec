let currentOptionIndex = 0;

function showNextOption() {
  if (currentOptionIndex < 8) {
    document.getElementById(`option${currentOptionIndex + 1}`).style.display = "block";
  }
}

function selectOption(optionId, selectedOption) {
  alert(selectedOption + "(을)를 선택하였습니다.");
  document.getElementById(optionId).style.display = "none";
  currentOptionIndex++;
  showNextOption();
}

function selectOptionInput(optionID) {
  const stature = document.getElementById("option_stature").value;
  const weight = document.getElementById("option_weight").value;

  if (!isNaN(stature) && !isNaN(weight) && stature !== "" && weight !== "") {
    alert(`키: ${stature}, 몸무게: ${weight}가 입력되었습니다.`);
    document.getElementById(optionID).style.display = "none";
    currentOptionIndex++;
    showNextOption();
  } else {
    alert("올바른 숫자를 입력해주세요.");
  }
}

function goBack(currentoptionID, previousoptionID) {
  document.getElementById(currentoptionID).style.display = "none";
  if (previousoptionID) {
    document.getElementById(previousoptionID).style.display = "block";
  }
  currentOptionIndex--;
}

window.onload = function () {
  showNextOption();
};
