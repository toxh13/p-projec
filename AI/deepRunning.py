import numpy as np
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Activation
import os
import json
import pymysql
from sqlalchemy import create_engine

# MySQL 연결 설정
DB_CONFIG = {
    "host": "khs.uy.to",  # MySQL 서버 주소
    "port": 3306,  # MySQL 포트
    "user": "toxh13",  # MySQL 사용자 이름
    "password": "123123a",  # MySQL 비밀번호
    "database": "project_db",  # 데이터베이스 이름
    "cursorclass": pymysql.cursors.DictCursor,  # 딕셔너리 형태로 결과 반환
}

# MySQL 연결
connection = pymysql.connect(
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    database=DB_CONFIG["database"],
    cursorclass=DB_CONFIG["cursorclass"]
)

# SQL 쿼리로 의류 데이터 로드
clothing_data_query = "SELECT * FROM Clothing_data"
clothing_data = pd.read_sql(clothing_data_query, connection)

# 스타일별로 고유한 숫자 값을 매핑하여 라벨 데이터를 숫자로 변환.
label_map = {label: idx for idx, label in enumerate(clothing_data['스타일'].unique())}
encoded_labels = clothing_data['스타일'].map(label_map).values

# 이미지 특징 벡터 데이터 로드
# 이미지 특징 벡터 데이터. 각 벡터는 이미지를 나타내는 고차원 특징 벡터입니다.
features_path = os.path.join("..", "AI", "image_features.npy")
features = np.load(features_path)

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
    BatchNormalization(),  # 배치 정규화를 추가하여 학습 안정성 향상.
    Activation('relu'),  # ReLU 활성화 함수.
    Dropout(0.5),  # 과적합 방지를 위한 드롭아웃.

    Dense(128),  # 두 번째 Dense 레이어: 128 노드.
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.5),  # 과적합 방지 드롭아웃.

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
    X_train,  # 학습 데이터.
    y_train_onehot,  # 학습 라벨 (One-hot 인코딩된 값).
    validation_split=0.2,  # 검증 데이터로 학습 데이터의 20% 사용.
    epochs=20,  # 학습 반복 횟수
    batch_size=32,  # 배치 크기.
    verbose=1  # 학습 진행 상황을 출력.
)


# 추천 시스템 함수
def recommend_clothing(user_height, user_weight, user_gender, user_style, clothingType, top_n=3, excluded_items=None):
    # 의류 데이터를 MySQL에서 로드
    clothing_data_query = "SELECT * FROM Clothing_data"
    clothing_data = pd.read_sql(clothing_data_query, connection)

    # 평균 키와 몸무게를 숫자로 변환 (오류 데이터 처리)
    clothing_data['평균 키'] = pd.to_numeric(clothing_data['평균 키'], errors='coerce')
    clothing_data['평균 몸무게'] = pd.to_numeric(clothing_data['평균 몸무게'], errors='coerce')

    # 필터링 조건 설정
    filtered_data = clothing_data[
        (clothing_data['평균 키'] >= user_height - 5) &
        (clothing_data['평균 키'] <= user_height + 5) &
        (clothing_data['평균 몸무게'] >= user_weight - 5) &
        (clothing_data['평균 몸무게'] <= user_weight + 5) &
        ((clothing_data['성별'] == user_gender) | (clothing_data['성별'] == "공용")) &
        (clothing_data['스타일'] == user_style) &
        (clothing_data['부위'] == clothingType)
    ]

    # 이전 추천 항목 제외
    if excluded_items:
        filtered_data = filtered_data[~filtered_data['상품명'].isin(excluded_items)]

    # 필터링된 데이터가 없는 경우 처리
    if filtered_data.empty:
        return []

    # 사용자 입력과 의류 데이터를 기반으로 추천 점수 계산
    predictions = []
    user_features = np.array([[user_height, user_weight]])

    for _, row in filtered_data.iterrows():
        item_features = np.array([[float(row['평균 키']), float(row['평균 몸무게'])]])
        combined_features = np.zeros((1, features.shape[1]))
        combined_features[:, :user_features.shape[1] + item_features.shape[1]] = np.concatenate(
            [user_features, item_features], axis=1
        )
        prediction = model.predict(combined_features, verbose=0).flatten()
        predictions.append(prediction[0])

    predictions = np.array(predictions)

    # 추천 점수 추가
    if len(predictions.flatten()) == len(filtered_data):
        filtered_data['score'] = predictions
    else:
        return []

    # 점수 기준 상위 추천 반환
    top_recommendations = filtered_data.nlargest(top_n, 'score')
    return top_recommendations[['상품명', '이미지 URL', 'score']].to_dict(orient='records')

def recommend_otherClothing(selected_item_name, clothing_data, model, clothingType, top_n=3, excluded_items=None):
    """
    다른 부위 의류 추천 함수.

    :param selected_item_name: 사용자가 선택한 의류의 이름.
    :param clothing_data: 의류 데이터프레임.
    :param model: TensorFlow 모델.
    :param clothingType: 추천받을 의류 부위.
    :param top_n: 추천받을 의류 개수.
    :param excluded_items: 추천 제외 항목 리스트.
    :return: 추천 의류 목록 (상품명, 이미지 URL, 점수).
    """
    # 선택된 항목의 데이터 가져오기
    selected_item = clothing_data[clothing_data['상품명'] == selected_item_name]
    if selected_item.empty:
        return []

    selected_item = selected_item.iloc[0]  # 첫 번째 행 선택
    user_height = selected_item['평균 키']
    user_weight = selected_item['평균 몸무게']
    user_gender = selected_item['성별']
    user_style = selected_item['스타일']

    # 추천 대상 필터링 (다른 부위의 항목만)
    target_data = clothing_data[clothing_data['부위'] != clothingType]
    target_data = target_data[
        ((target_data['성별'] == user_gender) | (target_data['성별'] == "공용")) &
        (target_data['스타일'] == user_style)
    ]

    # 제외된 항목 제거
    if excluded_items:
        target_data = target_data[~target_data['상품명'].isin(excluded_items)]

    if target_data.empty:
        return []

    # 사용자 특징 데이터 생성
    user_features = np.array([[user_height, user_weight]])
    predictions = []

    # 모델을 사용해 점수 예측
    for _, row in target_data.iterrows():
        item_features = np.array([[float(row['평균 키']), float(row['평균 몸무게'])]])
        combined_features = np.zeros((1, features.shape[1]))
        combined_features[:, :user_features.shape[1] + item_features.shape[1]] = np.concatenate(
            [user_features, item_features], axis=1
        )
        prediction = model.predict(combined_features, verbose=0).flatten()
        predictions.append(prediction[0])

    predictions = np.array(predictions)

    # 추천 점수 추가
    if len(predictions) == len(target_data):
        target_data = target_data.copy()
        target_data['score'] = predictions
    else:
        return []

    # 상위 추천 항목 반환
    top_recommendations = target_data.nlargest(top_n, 'score')
    return top_recommendations[['상품명', '이미지 URL', 'score']].to_dict(orient='records')


recommend_clothing(user_height, user_weight, user_gender, user_style, clothingType, top_n=3)
recommend_otherClothing(selected_item_name, clothing_data, model, clothingType, top_n=3, excluded_items=None)

# def save_recommendations_to_json(recommendations, json_path):
#     """
#     JSON 파일에 추천 의류 정보를 저장합니다.
#
#     :param recommendations: 추천 의류 데이터프레임
#     :param json_path: JSON 파일 경로
#     """
#     # 추천 데이터를 딕셔너리로 변환
#     data_to_save = recommendations[['상품명', '이미지 URL']].to_dict(orient='records')
#
#     # JSON 파일 쓰기
#     with open(json_path, 'w', encoding='utf-8') as json_file:
#         json.dump(data_to_save, json_file, ensure_ascii=False, indent=4)

# 예시 사용자 입력
# user_height = 175
# user_weight = 70
# user_gender = "남"
# user_style = "캐주얼"
# clothingType = "상의"
