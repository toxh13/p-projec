import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sqlalchemy import create_engine

# MySQL 설정
DB_CONFIG = {
    "host": "khs.uy.to",
    "port": 3306,
    "user": "toxh13",
    "password": "123123a",
    "database": "project_db",
}
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL)

# h5 모델 로드
model = load_model("clothing_model.h5")

# 추천 함수
def recommend_clothing(user_height, user_weight, user_gender, user_style, clothingType, top_n=3, excluded_items=None):
    clothing_data_query = "SELECT * FROM Clothing"
    clothing_data = pd.read_sql(clothing_data_query, engine)

    clothing_data['평균_키'] = pd.to_numeric(clothing_data['평균_키'], errors='coerce')
    clothing_data['평균_몸무게'] = pd.to_numeric(clothing_data['평균_몸무게'], errors='coerce')

    filtered_data = clothing_data[
        (clothing_data['평균_키'] >= user_height - 5) &
        (clothing_data['평균_키'] <= user_height + 5) &
        (clothing_data['평균_몸무게'] >= user_weight - 5) &
        (clothing_data['평균_몸무게'] <= user_weight + 5) &
        ((clothing_data['성별'] == user_gender) | (clothing_data['성별'] == "공용")) &
        (clothing_data['스타일'] == user_style) &
        (clothing_data['부위'] == clothingType)
    ]

    if excluded_items:
        filtered_data = filtered_data[~filtered_data['상품명'].isin(excluded_items)]

    if filtered_data.empty:
        return []

    predictions = []
    user_features = np.array([[user_height, user_weight]])

    for _, row in filtered_data.iterrows():
        item_features = np.array([[float(row['평균_키']), float(row['평균_몸무게'])]])
        combined_features = np.zeros((1, features.shape[1]))
        combined_features[:, :user_features.shape[1] + item_features.shape[1]] = np.concatenate(
            [user_features, item_features], axis=1
        )
        prediction = model.predict(combined_features, verbose=0).flatten()
        predictions.append(prediction[0])

    predictions = np.array(predictions)

    if len(predictions) == len(filtered_data):
        filtered_data['score'] = predictions
    else:
        return []

    top_recommendations = filtered_data.nlargest(top_n, 'score')
    return top_recommendations[['상품명', '이미지_URL', 'score']].to_dict(orient='records')
