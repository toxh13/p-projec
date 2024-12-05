import pandas as pd
from sklearn.neighbors import NearestNeighbors
from categorySelect import get_csv_path

def get_recommendation(gender, category, style, user_height, user_weight, exclude_indices=None):
    # CSV 파일 경로 가져오기
    try:
        csv_path = get_csv_path(gender, category, style)
    except ValueError as e:
        print(e)
        return None

    # CSV 파일 읽기 (빈칸을 공백으로 채우기)
    data = pd.read_csv(csv_path).fillna("")

    # 키와 몸무게를 숫자로 변환
    data['height'] = pd.to_numeric(data['키'], errors='coerce')
    data['weight'] = pd.to_numeric(data['몸무게'], errors='coerce')

    # 유효한 데이터만 필터링
    data = data.dropna(subset=['height', 'weight'])

    if exclude_indices is not None:
        data = data.drop(exclude_indices, errors='ignore')

    # KNN 모델 적용
    knn_model = NearestNeighbors(n_neighbors=3, metric='euclidean')
    knn_model.fit(data[['height', 'weight']])

    # 사용자 입력을 데이터프레임 형태로 변환
    user_data = pd.DataFrame({
        'height': [user_height],
        'weight': [user_weight]
    })

    # 가장 가까운 데이터 3개 찾기
    distances, indices = knn_model.kneighbors(user_data)
    top_3_recommendations = data.iloc[indices[0]]

    return top_3_recommendations.reset_index(drop=True)

# 사용자 입력 받기
user_gender = input("성별을 선택하세요 (남성/여성): ").strip()
user_category = input("의류 종류를 선택하세요 (상의/하의): ").strip()
user_style = input("스타일을 선택하세요 (고프코어, 레트로, 미니멀, 스트릿, 스포티, 워크웨어, 캐주얼, 클래식): ").strip()

# 사용자 키와 몸무게 입력
user_height = float(input("사용자의 키(cm)를 입력하세요: "))
user_weight = float(input("사용자의 몸무게(kg)를 입력하세요: "))

# 1차 추천 (사용자가 선택한 카테고리)
top_3_recommendations = get_recommendation(user_gender, user_category, user_style, user_height, user_weight)
if top_3_recommendations is None:
    exit()

print("추천 의류 정보:")
for idx, row in top_3_recommendations.iterrows():
    print(f"{idx}: 브랜드명: {row['브랜드명']}, 상품명: {row['상품명']}, 가격: {row['가격']}")

selected_index = input("추천받은 의류 중 하나를 선택하세요 (0, 1, 2). 마음에 들지 않으면 'N'을 입력하세요: ").strip()
if selected_index.lower() == 'n':
    exclude_indices = top_3_recommendations.index
    print("다른 추천 의류를 찾는 중...")
    top_3_recommendations = get_recommendation(user_gender, user_category, user_style, user_height, user_weight, exclude_indices=exclude_indices)
    if top_3_recommendations is None or top_3_recommendations.empty:
        print("더 이상 추천할 의류가 없습니다. 프로그램을 종료합니다.")
        exit()

    print("새로운 추천 의류 정보:")
    for idx, row in top_3_recommendations.iterrows():
        print(f"{idx}: 브랜드명: {row['브랜드명']}, 상품명: {row['상품명']}, 가격: {row['가격']}")

    selected_index = input("추천받은 의류 중 하나를 선택하세요 (0, 1, 2): ").strip()

if not selected_index.isdigit() or int(selected_index) not in range(len(top_3_recommendations)):
    print("잘못된 선택입니다. 프로그램을 종료합니다.")
    exit()

selected_index = int(selected_index)
selected_item = top_3_recommendations.loc[selected_index]

# 선택한 의류 정보 저장
output_data = pd.DataFrame({
    '브랜드명': [selected_item['브랜드명']],
    '상품명': [selected_item['상품명']],
    '가격': [selected_item['가격']],
    '이미지 URL': [selected_item['이미지 URL']],
    '모델 이미지 URL': [selected_item['모델 이미지 URL']],
    '키': [selected_item['키']],
    '몸무게': [selected_item['몸무게']]
})

output_csv_path = "selected_item.csv"
output_data.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
print(f"선택한 의류 정보를 {output_csv_path} 파일에 저장했습니다.")

# 2차 추천 (반대 카테고리)
alternate_category = "하의" if user_category == "상의" else "상의"

print(f"{alternate_category} 추천을 진행합니다...")
top_3_alternate = get_recommendation(user_gender, alternate_category, user_style, user_height, user_weight)
if top_3_alternate is None:
    exit()

print("추천 의류 정보:")
for idx, row in top_3_alternate.iterrows():
    print(f"{idx}: 브랜드명: {row['브랜드명']}, 상품명: {row['상품명']}, 가격: {row['가격']}")

selected_index_alternate = input("추천받은 의류 중 하나를 선택하세요 (0, 1, 2). 마음에 들지 않으면 'N'을 입력하세요: ").strip()
if selected_index_alternate.lower() == 'n':
    exclude_indices = top_3_alternate.index
    print("다른 추천 의류를 찾는 중...")
    top_3_alternate = get_recommendation(user_gender, alternate_category, user_style, user_height, user_weight, exclude_indices=exclude_indices)
    if top_3_alternate is None or top_3_alternate.empty:
        print("더 이상 추천할 의류가 없습니다. 프로그램을 종료합니다.")
        exit()

    print("새로운 추천 의류 정보:")
    for idx, row in top_3_alternate.iterrows():
        print(f"{idx}: 브랜드명: {row['브랜드명']}, 상품명: {row['상품명']}, 가격: {row['가격']}")

    selected_index_alternate = input("추천받은 의류 중 하나를 선택하세요 (0, 1, 2): ").strip()

if not selected_index_alternate.isdigit() or int(selected_index_alternate) not in range(len(top_3_alternate)):
    print("잘못된 선택입니다. 프로그램을 종료합니다.")
    exit()

selected_index_alternate = int(selected_index_alternate)
selected_item_alternate = top_3_alternate.loc[selected_index_alternate]

# 선택한 반대 카테고리 의류 정보 저장
output_data_alternate = pd.DataFrame({
    '브랜드명': [selected_item_alternate['브랜드명']],
    '상품명': [selected_item_alternate['상품명']],
    '가격': [selected_item_alternate['가격']],
    '이미지 URL': [selected_item_alternate['이미지 URL']],
    '모델 이미지 URL': [selected_item_alternate['모델 이미지 URL']],
    '키': [selected_item_alternate['키']],
    '몸무게': [selected_item_alternate['몸무게']]
})

output_csv_path_alternate = "selected_alternate_item.csv"
output_data_alternate.to_csv(output_csv_path_alternate, index=False, encoding='utf-8-sig')
print(f"선택한 {alternate_category} 정보를 {output_csv_path_alternate} 파일에 저장했습니다.")