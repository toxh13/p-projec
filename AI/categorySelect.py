# gender_selector.py

def get_csv_path(gender: str, category: str, style: str) -> str:
    """
    성별, 의류 종류, 스타일에 따라 적절한 CSV 파일 경로를 반환합니다.

    Args:
        gender (str): 성별 ("남성" 또는 "여성")
        category (str): 의류 종류 ("상의" 또는 "하의")
        style (str): 스타일 ("고프코어", "레트로", "미니멀", "스트릿", "스포티", "워크웨어", "캐주얼", "클래식")

    Returns:
        str: 선택된 CSV 파일 경로
    """
    base_path = "C:\\Python\\의류데이터\\"
    styles = ["고프코어", "레트로", "미니멀", "스트릿", "스포티", "워크웨어", "캐주얼", "클래식"]

    # 입력 검증
    if gender not in ["남성", "여성"]:
        raise ValueError("성별은 '남성' 또는 '여성' 중 하나를 입력하세요.")
    if category not in ["상의", "하의"]:
        raise ValueError("의류 종류는 '상의' 또는 '하의' 중 하나를 입력하세요.")
    if style not in styles:
        raise ValueError(f"스타일은 다음 중 하나를 입력하세요: {', '.join(styles)}")

    # 경로 생성
    return f"{base_path}{gender}-{category}\\{gender}-{category}-{style}.csv"
