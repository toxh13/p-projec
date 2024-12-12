import pandas as pd

clothing_data = pd.read_csv("Clothing_data.csv")
print(clothing_data.head())  # 데이터 상위 5개 확인
print(clothing_data.info())  # 필드와 데이터 유형 확인

user_height = 175
user_weight = 70
user_gender = "남성"
user_style = "캐주얼"
recommend_top = True  # True이면 상의를 먼저 추천, False이면 하의를 먼저 추천

filtered_data = clothing_data[
    (clothing_data['평균 키'] -  5) &
    (clothing_data['평균 키'] +  5) &
    (clothing_data['평균 몸무게'] - 5) &
    (clothing_data['평균 몸무게'] + 5)
]

print(clothing_data['성별'].unique())  # '남성', '여성' 등의 고유 값 확인
print(clothing_data['스타일'].unique())  # '캐주얼', '포멀' 등의 고유 값 확인

print(filtered_data)

if filtered_data.empty:
    print("필터링된 데이터가 없습니다.")
else:
    print("필터링된 데이터:")
    print(filtered_data[['브랜드', '상품명', '스타일', '성별']])  # 일부 열만 출력
