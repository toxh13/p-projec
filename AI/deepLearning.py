import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import create_engine
import random
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


def recommend_clothing(clothing_data, user_id, user_height, user_weight, user_gender, user_style,
                                         clothingType, top_n=3):
    if user_id:
        preset = get_user_closet_preset(user_id)
        if not preset.empty:
            print("사용자의 이전 데이터(프리셋)가 존재합니다. 프리셋 기반으로 추천을 진행합니다.")

            if clothingType == "상의":
                preset_items = clothing_data[(clothing_data['id'] == preset['top_clothing_id'].iloc[0]) &
                                             (clothing_data['부위'] == "상의")]
            elif clothingType == "하의":
                preset_items = clothing_data[(clothing_data['id'] == preset['bottom_clothing_id'].iloc[0]) &
                                             (clothing_data['부위'] == "하의")]
            else:
                print(f"알 수 없는 clothingType: {clothingType}")
                return []

            # 추천 로직
            recommendations = []
            for _, item in preset_items.iterrows():
                features = clothing_data[['평균_키', '평균_몸무게']].values
                item_features = np.array([[item['평균_키'], item['평균_몸무게']]])
                knn = NearestNeighbors(n_neighbors=min(top_n, len(features)), metric='euclidean')
                knn.fit(features)
                distances, indices = knn.kneighbors(item_features)

                similar_items = clothing_data.iloc[indices[0]].copy()
                similar_items['distance'] = distances[0]
                similar_items = similar_items[similar_items['부위'] == clothingType]
                recommendations.append(similar_items)

            # 결과 병합
            all_recommendations = pd.concat(recommendations).drop_duplicates(subset='id')
            all_recommendations = all_recommendations.nsmallest(top_n, 'distance')

            # 프리셋 결과 부족 시 조건 기반 추천
            if all_recommendations.empty or len(all_recommendations) < top_n:
                print("프리셋 기반 추천 결과가 충분하지 않습니다. 조건 기반 추천으로 전환합니다.")
                return recommend_based_on_conditions(clothing_data, user_height, user_weight, user_gender, user_style, clothingType, top_n)

            return all_recommendations[['id', '상품명', '이미지_URL', 'distance']].to_dict(orient='records')

    # 이전 데이터가 없는 경우 조건 기반 추천
    return recommend_based_on_conditions(clothing_data, user_height, user_weight, user_gender, user_style, clothingType, top_n)


def recommend_based_on_conditions(clothing_data, user_height, user_weight, user_gender, user_style, clothingType, top_n=3):
    filtered_data = clothing_data[
        (clothing_data['평균_키'] >= user_height - 10) &
        (clothing_data['평균_키'] <= user_height + 10) &
        (clothing_data['평균_몸무게'] >= user_weight - 10) &
        (clothing_data['평균_몸무게'] <= user_weight + 10) &
        ((clothing_data['성별'] == user_gender) | (clothing_data['성별'] == "공용")) &
        (clothing_data['스타일'] == user_style) &
        (clothing_data['부위'].str.strip().str.lower() == clothingType.strip().lower())
    ]

    if filtered_data.empty:
        return []

    features = filtered_data[['평균_키', '평균_몸무게']].values
    user_features = np.array([[user_height, user_weight]])

    knn = NearestNeighbors(n_neighbors=min(top_n, len(features)), metric='euclidean')
    knn.fit(features)

    distances, indices = knn.kneighbors(user_features)
    recommendations = filtered_data.iloc[indices[0]].copy()
    recommendations['distance'] = distances[0]

    # 결과를 섞기
    recommendations = recommendations.sample(frac=1).reset_index(drop=True)

    return recommendations[['id', '상품명', '이미지_URL', 'distance']].to_dict(orient='records')


# 실행
if __name__ == "__main__":
    # 데이터 로드
    clothing_data = load_clothing_data()

    # 사용자 정보
    user_id = 3  # 로그인된 사용자 ID (비로그인: None)
    user_height = 175
    user_weight = 70
    user_gender = "남성"
    user_style = "캐주얼"
    clothingType = "상의"

    # 추천 수행
    recommendations = recommend_clothing(
        clothing_data, user_id, user_height, user_weight, user_gender, user_style, clothingType, top_n=3
    )

    # 결과 출력
    if recommendations:
        print("추천 결과:")
        for rec in recommendations:
            print(f"ID: {rec['id']}, 상품명: {rec['상품명']}, 거리: {rec['distance']}, 이미지 URL: {rec['이미지_URL']}")
    else:
        print("추천 결과가 없습니다.")

