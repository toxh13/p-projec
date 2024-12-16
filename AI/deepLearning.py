import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import create_engine

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


def calculate_similarity_score(row, user_height, user_weight, user_style, user_gender):
    """
    각 의류 항목과 사용자의 유사도를 계산하는 함수
    """
    # 키와 몸무게에 기반한 거리 계산 (Euclidean)
    distance = np.sqrt((row['평균_키'] - user_height) ** 2 + (row['평균_몸무게'] - user_weight) ** 2)

    # 스타일 점수 (사용자 스타일과 불일치 시 패널티 추가)
    style_score = 0 if row['스타일'] == user_style else 5

    # 성별 점수 (성별이 일치하면 0점, 공용이면 2점, 불일치하면 10점)
    if row['성별'] == user_gender:
        gender_score = 0
    elif row['성별'] == "공용":
        gender_score = 2
    else:
        gender_score = 10

    # 총 점수 (거리 + 스타일 점수 + 성별 점수)
    total_score = distance + style_score + gender_score
    return total_score


def recommend_based_on_conditions(clothing_data, user_height, user_weight, user_gender, user_style, clothingType,
                                  top_n=3):
    """
    조건 기반 추천 함수: 키, 몸무게, 성별, 스타일에 따라 유사한 의류 추천
    """
    # 사용자 조건에 맞는 데이터 필터링
    filtered_data = clothing_data[
        (clothing_data['평균_키'] >= user_height - 5) &
        (clothing_data['평균_키'] <= user_height + 5) &
        (clothing_data['평균_몸무게'] >= user_weight - 5) &
        (clothing_data['평균_몸무게'] <= user_weight + 5) &
        ((clothing_data['성별'] == user_gender) | (clothing_data['성별'] == "공용")) &
        (clothing_data['스타일'] == user_style) &
        (clothing_data['부위'].str.strip().str.lower() == clothingType.strip().lower())
        ]

    if filtered_data.empty:
        return []

    # 복사본 생성 및 유사도 점수 계산
    filtered_data = filtered_data.copy()
    filtered_data.loc[:, 'similarity_score'] = filtered_data.apply(
        calculate_similarity_score,
        axis=1,
        args=(user_height, user_weight, user_style, user_gender)
    )

    # 무작위 가중치 추가
    random_weights = np.random.uniform(0, 3.0, size=len(filtered_data))  # 무작위 가중치 추가
    filtered_data.loc[:, 'random_score'] = filtered_data['similarity_score'] + random_weights

    # 유사도 점수와 무작위 가중치를 합산한 점수로 정렬하여 상위 top_n 항목 반환
    recommendations = filtered_data.nsmallest(top_n, 'random_score')
    return recommendations[['id', '상품명', '이미지_URL', 'random_score']].to_dict(orient='records')


def recommend_clothing(clothing_data, user_id, user_height, user_weight, user_gender, user_style, clothingType, top_n=3):
    """
    프리셋 기반 추천 또는 조건 기반 추천을 수행하는 함수
    """
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

            # 프리셋 기반 추천
            if not preset_items.empty:
                recommendations = recommend_based_on_conditions(
                    preset_items, user_height, user_weight, user_gender, user_style, clothingType, top_n
                )
                if len(recommendations) < top_n:  # 추천 결과가 부족한 경우
                    print("프리셋 기반 추천 결과가 충분하지 않습니다. 조건 기반 추천으로 전환합니다.")
                    return recommend_based_on_conditions(
                        clothing_data, user_height, user_weight, user_gender, user_style, clothingType, top_n
                    )
                return recommendations

    # 프리셋이 없거나 결과가 부족할 경우 조건 기반 추천
    print("프리셋 기반 추천이 부족하여 조건 기반 추천으로 전환합니다.")
    return recommend_based_on_conditions(clothing_data, user_height, user_weight, user_gender, user_style, clothingType, top_n)



# 실행
if __name__ == "__main__":
    # 데이터 로드
    clothing_data = load_clothing_data()

    # 사용자 정보
    user_id = 1  # 로그인된 사용자 ID (비로그인: None)
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
            print(f"ID: {rec['id']}, 상품명: {rec['상품명']}, 무작위 점수: {rec['random_score']}, 이미지 URL: {rec['이미지_URL']}")
    else:
        print("추천 결과가 없습니다.")
