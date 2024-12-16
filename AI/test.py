import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import create_engine
import os

# MySQL 연결 설정
DB_CONFIG = {
    "host": "khs.uy.to",
    "port": 3306,
    "user": "toxh13",
    "password": "123123a",
    "database": "project_db",
}

# SQLAlchemy 엔진 생성
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL)


# Clothing 데이터 로드
def load_clothing_data():
    try:
        with engine.connect() as conn:
            clothing_data = pd.read_sql("SELECT * FROM Clothing", conn)
        print("Clothing 데이터 로드 성공")
        # 필수 열 확인
        required_columns = ['평균_키', '평균_몸무게', '성별', '스타일', '부위']
        missing_columns = [col for col in required_columns if col not in clothing_data.columns]
        if missing_columns:
            raise ValueError(f"필수 열이 없습니다: {missing_columns}")
        # 결측값 처리
        clothing_data['평균_키'] = pd.to_numeric(clothing_data['평균_키'], errors='coerce').fillna(170)
        clothing_data['평균_몸무게'] = pd.to_numeric(clothing_data['평균_몸무게'], errors='coerce').fillna(60)
        return clothing_data
    except Exception as e:
        print(f"Clothing 데이터 로드 실패: {e}")
        raise


# 추천 함수
def get_user_closet_preset(user_id):
    """사용자의 최신 프리셋 가져오기"""
    query = f"""
    SELECT * FROM User_Closets
    WHERE user_id = {user_id}
    ORDER BY added_at DESC
    LIMIT 1;
    """
    with engine.connect() as conn:
        preset = pd.read_sql(query, conn)
    return preset


def recommend_clothing_with_preset_check(clothing_data, user_id, user_height, user_weight, user_sex, user_style,
                                         clothing_type, top_n=3):
    """이전 데이터 여부에 따라 추천"""
    if user_id:
        # 사용자 프리셋 가져오기
        preset = get_user_closet_preset(user_id)
        if not preset.empty:
            print("사용자의 이전 데이터(프리셋)가 존재합니다. 프리셋 기반으로 추천을 진행합니다.")

            # 프리셋 데이터 기반 추천
            top_id = preset['top_clothing_id'].iloc[0]
            bottom_id = preset['bottom_clothing_id'].iloc[0]
            preset_items = clothing_data[clothing_data['id'].isin([top_id, bottom_id])]

            # 각 아이템과 유사한 항목 추천
            recommendations = []
            for _, item in preset_items.iterrows():
                features = clothing_data[['평균_키', '평균_몸무게']].values
                item_features = np.array([[item['평균_키'], item['평균_몸무게']]])
                knn = NearestNeighbors(n_neighbors=top_n, metric='euclidean')
                knn.fit(features)
                distances, indices = knn.kneighbors(item_features)

                similar_items = clothing_data.iloc[indices[0]].copy()
                similar_items['distance'] = distances[0]
                recommendations.append(similar_items)

            all_recommendations = pd.concat(recommendations).drop_duplicates(subset='id')
            all_recommendations = all_recommendations.nsmallest(top_n, 'distance')
            return all_recommendations[['id', '상품명', '이미지_URL', 'distance']].to_dict(orient='records')
        else:
            print("사용자의 이전 데이터(프리셋)가 없습니다. 조건 기반 추천을 진행합니다.")

    # 이전 데이터가 없는 경우 또는 비로그인 사용자
    filtered_data = clothing_data[
        (clothing_data['평균_키'] >= user_height - 5) &
        (clothing_data['평균_키'] <= user_height + 5) &
        (clothing_data['평균_몸무게'] >= user_weight - 5) &
        (clothing_data['평균_몸무게'] <= user_weight + 5) &
        ((clothing_data['성별'] == user_sex) | (clothing_data['성별'] == "공용")) &
        (clothing_data['스타일'] == user_style) &
        (clothing_data['부위'] == clothing_type)
        ]

    if filtered_data.empty:
        return []

    # KNN 추천
    features = filtered_data[['평균_키', '평균_몸무게']].values
    user_features = np.array([[user_height, user_weight]])

    knn = NearestNeighbors(n_neighbors=top_n, metric='euclidean')
    knn.fit(features)

    distances, indices = knn.kneighbors(user_features)
    recommendations = filtered_data.iloc[indices[0]].copy()
    recommendations['distance'] = distances[0]
    recommendations = recommendations.nsmallest(top_n, 'distance')
    return recommendations[['id', '상품명', '이미지_URL', 'distance']].to_dict(orient='records')


# 실행
if __name__ == "__main__":
    # 데이터 로드
    clothing_data = load_clothing_data()

    # 사용자 정보
    user_id = 1  # 로그인된 사용자 ID (비로그인: None)
    user_height = 175
    user_weight = 70
    user_sex = "남성"
    user_style = "캐주얼"
    clothing_type = "하의"

    # 추천 수행
    recommendations = recommend_clothing_with_preset_check(
        clothing_data, user_id, user_height, user_weight, user_sex, user_style, clothing_type, top_n=3
    )

    # 결과 출력
    if recommendations:
        print("추천 결과:")
        for rec in recommendations:
            print(f"ID: {rec['id']}, 상품명: {rec['상품명']}, 거리: {rec['distance']}, 이미지 URL: {rec['이미지_URL']}")
    else:
        print("추천 결과가 없습니다.")

