from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Activation
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import numpy as np

# 데이터 준비 (이미 features와 encoded_labels 준비된 상태라고 가정)
features = np.load("image_features.npy")  # 이미지 특징 파일 경로
encoded_labels = np.array([...])  # 라벨 데이터 배열

# 라벨 매핑
label_map = {label: idx for idx, label in enumerate(set(encoded_labels))}
encoded_labels = np.array([label_map[label] for label in encoded_labels])

# 데이터 샘플 수 정렬
min_samples = min(len(features), len(encoded_labels))
features = features[:min_samples]
encoded_labels = encoded_labels[:min_samples]

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(features, encoded_labels, test_size=0.2, random_state=42)
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
    Dense(len(label_map), activation='softmax')
])

# 모델 컴파일
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 모델 훈련
model.fit(X_train, y_train_onehot, validation_split=0.2, epochs=20, batch_size=32, verbose=1)

# 모델 저장
model.save("clothing_model.h5")
