import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Activation

# 예시: 이미지 특징 벡터를 로드
features = np.load('image_features.npy')  # 이미지 특징 벡터 (예: (N, 512))
labels = pd.read_csv('Clothing_data.csv')  # 라벨 데이터 로드

# 라벨 인코딩
label_map = {label: idx for idx, label in enumerate(labels['스타일'].unique())}
encoded_labels = labels['스타일'].map(label_map).values

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(features, encoded_labels, test_size=0.2, random_state=42)

# 라벨을 원-핫 인코딩
y_train_onehot = to_categorical(y_train, num_classes=len(label_map))
y_test_onehot = to_categorical(y_test, num_classes=len(label_map))



# 모델 설계
model = Sequential([
    Dense(256, input_dim=features.shape[1]),
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.5),

    Dense(128),
    BatchNormalization(),
    Activation('relu'),
    Dropout(0.5),

    Dense(len(label_map), activation='softmax')  # 출력 레이어
])

# 모델 컴파일
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 모델 요약
model.summary()
# 훈련
history = model.fit(
    X_train,
    y_train_onehot,
    validation_split=0.2,
    epochs=30,
    batch_size=32,
    verbose=1
)
    