def get_csv_path(gender: str, category: str, style: str) -> str:
    base_path = "C:\\Python\\의류데이터\\의류데이터\\"
    styles = ["미니멀", "스트릿", "워크웨어", "캐주얼"]

    # 입력 검증
    if gender not in ["남", "여"]:
        raise ValueError("성별은 '남', '여' 중 하나를 입력하세요.")
    if category not in ["상의", "하의"]:
        raise ValueError("의류 종류는 '상의' 또는 '하의' 중 하나를 입력하세요.")
    if style not in styles:
        raise ValueError(f"스타일은 다음 중 하나를 입력하세요: {', '.join(styles)}")

    # 경로 생성
    return f"{base_path}{category}-{style}.csv"
