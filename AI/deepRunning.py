import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Activation
import os
import json

# 예시: 이미지 특징 벡터를 로드
# 이미지 특징 벡터 데이터. 각 벡터는 이미지를 나타내는 고차원 특징 벡터입니다.
features = np.load("C:\\Work\\dbServer\\image_features.npy")

# 라벨 데이터 로드. 각 의류 항목의 정보가 포함된 CSV 파일.
labels = pd.read_csv("C:/Work/dbServer/Clothing_data.csv")

# 라벨 인코딩
# 스타일별로 고유한 숫자 값을 매핑하여 라벨 데이터를 숫자로 변환.
label_map = {label: idx for idx, label in enumerate(labels['스타일'].unique())}
encoded_labels = labels['스타일'].map(label_map).values

# 데이터 분할
# 데이터를 학습용과 테스트용으로 나누는 과정. 학습: 80%, 테스트: 20%.
X_train, X_test, y_train, y_test = train_test_split(features, encoded_labels, test_size=0.2, random_state=42)

# 라벨을 원-핫 인코딩
# 숫자로 변환된 라벨 데이터를 One-hot 형식으로 변환.
y_train_onehot = to_categorical(y_train, num_classes=len(label_map))
y_test_onehot = to_categorical(y_test, num_classes=len(label_map))

# 모델 설계
# 다층 신경망 모델을 설계. 각 층은 Dense, BatchNormalization, Dropout으로 구성됨.
model = Sequential([
    Dense(256, input_dim=features.shape[1]),  # 첫 번째 Dense 레이어: 입력 차원은 특징 벡터의 크기.
    BatchNormalization(),                     # 배치 정규화를 추가하여 학습 안정성 향상.
    Activation('relu'),                       # ReLU 활성화 함수.
    Dropout(0.5),                             # 과적합 방지를 위한 드롭아웃.

    Dense(128),                               # 두 번째 Dense 레이어: 128 노드.
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.5),

    Dense(len(label_map), activation='softmax')  # 출력 레이어: 클래스 개수만큼 노드 생성.
])

# 모델 컴파일
# 손실 함수와 최적화 알고리즘, 평가 지표를 설정.
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 모델 요약
# 모델의 구조를 출력.
model.summary()

# 훈련
# 데이터를 사용해 모델을 학습.
history = model.fit(
    X_train,              # 학습 데이터.
    y_train_onehot,       # 학습 라벨 (One-hot 인코딩된 값).
    validation_split=0.2, # 검증 데이터로 학습 데이터의 20% 사용.
    epochs=1,             # 학습 반복 횟수. -> 나중에 증가시켜야 함
    batch_size=32,        # 배치 크기.
    verbose=1             # 학습 진행 상황을 출력.
)

def save_recommendations_to_json(recommendations, json_path):
    """
    JSON 파일에 추천 의류 정보를 저장합니다.

    :param recommendations: 추천 의류 데이터프레임
    :param json_path: JSON 파일 경로
    """
    # 추천 데이터를 딕셔너리로 변환
    data_to_save = recommendations[['상품명', '이미지 URL']].to_dict(orient='records')

    # JSON 파일 쓰기
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)

# 추천 시스템 함수
def recommend_clothing(user_height, user_weight, user_gender, user_style, recommend_top, top_n=3):
    # 의류 데이터를 로드
    clothing_data = pd.read_csv("C:/Work/dbServer/Clothing_data.csv")
    # JSON 저장 경로 설정
    json_path = os.path.join("..", "frontend", "JSON", "images.json")

    # 평균 키와 몸무게를 숫자로 변환 (오류 데이터 처리)
    clothing_data['평균 키'] = pd.to_numeric(clothing_data['평균 키'], errors='coerce')
    clothing_data['평균 몸무게'] = pd.to_numeric(clothing_data['평균 몸무게'], errors='coerce')

    # 사용자가 상의를 추천받고자 하는 경우
    if recommend_top:
        filtered_data = clothing_data[
            (clothing_data['평균 키'] >= user_height - 5) &
            (clothing_data['평균 키'] <= user_height + 5) &
            (clothing_data['평균 몸무게'] >= user_weight - 5) &
            (clothing_data['평균 몸무게'] <= user_weight + 5) &
            ((clothing_data['성별'] == user_gender) |
             (clothing_data['성별'] == "공용")) &
            (clothing_data['스타일'] == user_style) &
            (clothing_data['부위'] == "상의")
        ]
    else:
        # 사용자가 하의를 추천받고자 하는 경우
        filtered_data = clothing_data[
            (clothing_data['평균 키'] >= user_height - 5) &
            (clothing_data['평균 키'] <= user_height + 5) &
            (clothing_data['평균 몸무게'] >= user_weight - 5) &
            (clothing_data['평균 몸무게'] <= user_weight + 5) &
            ((clothing_data['성별'] == user_gender) |
             (clothing_data['성별'] == "공용")) &
            (clothing_data['스타일'] == user_style) &
            (clothing_data['부위'] == "하의")
        ]

    # 필터링된 데이터가 없는 경우 처리
    if filtered_data.empty:
        print("필터링된 데이터가 없습니다.")
        return

    # 필터링된 데이터 출력
    print("필터링된 데이터:")
    print(filtered_data[['브랜드', '상품명', '스타일', '성별']].head(3))

    # 사용자 특징 데이터 생성
    user_features = np.array([[user_height, user_weight]])
    predictions = []  # 예측 점수를 저장할 리스트

    # 필터링된 데이터에 대해 모델 예측 수행
    for _, row in filtered_data.iterrows():
        # 각 의류 항목의 평균 키와 몸무게를 특징으로 사용
        item_features = np.array([[float(row['평균 키']), float(row['평균 몸무게'])]])

        # 사용자 데이터와 의류 데이터를 결합하여 모델 입력 생성
        combined_features = np.zeros((1, features.shape[1]))
        combined_features[:, :user_features.shape[1] + item_features.shape[1]] = np.concatenate(
            [user_features, item_features], axis=1)

        # 모델을 사용해 예측 수행
        prediction = model.predict(combined_features, verbose=0).flatten()
        predictions.append(prediction[0])  # 예측 값 저장

    predictions = np.array(predictions)

    # 예측 값과 데이터 크기가 맞는지 확인 후 점수 추가
    if len(predictions.flatten()) == len(filtered_data):
        filtered_data = filtered_data.copy()
        filtered_data['score'] = predictions
    else:
        print("추천 점수 계산에 문제가 발생했습니다. 데이터 길이를 확인하세요.")
        return

    # 상위 추천 항목 반복
    isGood = False
    remaining_items = filtered_data.copy()
    while not isGood:
        # 추천 점수 기준 상위 항목 추출
        top_recommendations = remaining_items.nlargest(top_n, 'score')

        if top_recommendations.empty:
            print("추천할 의류가 더 이상 없습니다.")
            break

        # 추천 결과 출력
        print("추천 의류 상위 항목:")
        print(top_recommendations[['상품명', '이미지 URL']])

        # JSON 파일에 추천 항목 저장
        save_recommendations_to_json(top_recommendations, json_path)
        print(f"추천 결과가 JSON 파일에 저장되었습니다: {json_path}")

        # 사용자 피드백 받기
        user_input = input("추천된 의류 중 마음에 드는 것이 있습니까? (yes/no): ").strip().lower()
        if user_input == "yes":
            print("추천을 완료합니다.")
            isGood = True
        else:
            # 선택된 항목을 제외하고 남은 항목만 유지
            remaining_items = remaining_items.drop(top_recommendations.index)

            if remaining_items.empty:
                print("추천할 의류가 더 이상 없습니다.")
                break

def recommend_otherClothing(selected_item_index, clothing_data, image_features, recommend_top=True, top_n=3):
    user_height = selected_item['평균 키']
    user_weight = selected_item['평균 몸무게']
    user_gender = selected_item['성별']
    user_style = selected_item['스타일']

    # 추천 대상 필터링
    if recommend_top:
        target_data = clothing_data[clothing_data['부위'] == '하의']
    else:
        target_data = clothing_data[clothing_data['부위'] == '상의']

    if target_data.empty:
        print("추천할 대상 의류가 없습니다.")
        return

    # TensorFlow 모델 입력 데이터 생성
    user_features = np.array([[user_height, user_weight]])
    user_features_scaled = (user_features - np.mean(user_features, axis=0)) / np.std(user_features, axis=0)

    # 모델로 점수 예측
    predictions = model.predict(user_features_scaled)

    # 추천 점수 추가
    target_data = target_data.copy()
    target_data['score'] = predictions.flatten()  # 예측 점수 추가

    # 추천 반복
    isGood = False
    remaining_items = target_data.copy()

    while not isGood:
        # 유사도가 높은 상위 N개 항목 선택
        top_recommendations = remaining_items.nlargest(top_n, 'score')

        if top_recommendations.empty:
            print("추천할 의류가 더 이상 없습니다.")
            break

        # 출력 (이미지 URL과 상품명만)
        print("추천 의류 상위 항목:")
        print(top_recommendations[['상품명', '이미지 URL']])  # 이미지 URL과 상품명만 출력

        # 사용자 피드백 받기
        user_input = input("추천된 의류 중 마음에 드는 것이 있습니까? (yes/no): ").strip().lower()
        if user_input == "yes":
            print("추천을 완료합니다.")
            isGood = True
        else:
            # 이미 추천된 항목 제외
            remaining_items = remaining_items.drop(top_recommendations.index)

            # 더 이상 추천할 항목이 없는 경우 종료
            if remaining_items.empty:
                print("추천할 의류가 더 이상 없습니다.")
                break

# 예시 사용자 입력
user_height = 175
user_weight = 70
user_gender = "남성"
user_style = "캐주얼"
recommend_top = True  # True이면 상의를 먼저 추천, False이면 하의를 먼저 추천

recommend_clothing(user_height, user_weight, user_gender, user_style, recommend_top, top_n=3)
# recommend_otherClothing(selected_item_index, clothing_data, image_features, recommend_top, top_n=3)
