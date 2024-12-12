import pandas as pd
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import requests
from io import BytesIO

# CSV 파일 읽기
df = pd.read_csv("Clothing_data.csv")

# 이미지 URL 가져오기
image_urls = df["이미지 URL"]

# ResNet50 모델 로드 (사전 훈련된 모델)
model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

# 이미지 특징 추출 함수
def extract_features(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            img = load_img(BytesIO(response.content), target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0  # 정규화
            features = model.predict(img_array)
            return features.flatten()
        else:
            print(f"Failed to download image: {image_url}")
            return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# 모든 이미지에 대해 특징 벡터 추출
image_features = []
for url in image_urls:
    features = extract_features(url)
    if features is not None:
        image_features.append(features)

# 벡터를 numpy 배열로 변환
image_features = np.array(image_features)

print("이미지 특징 벡터 추출 완료:", image_features.shape)

# 이미지 특징 벡터 저장
np.save("image_features.npy", image_features)
print("이미지 특징 벡터가 'image_features.npy'로 저장되었습니다.")
