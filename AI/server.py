from flask import Flask, request, jsonify
from deepRunning import recommend_clothing  # 모듈화한 추천 시스템 불러오기

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    # 사용자 입력 받기
    user_data = request.json
    user_height = int(user_data['user_height'])
    user_weight = int(user_data['user_weight'])
    user_gender = user_data['user_gender']
    user_style = user_data['user_style']
    recommend_top = user_data['recommend_top']

    # 추천 함수 호출
    recommend_top = True if recommend_top == "true" else False
    recommend_clothing(user_height, user_weight, user_gender, user_style, recommend_top, top_n=3)

    return jsonify({"status": "success", "message": "Recommendations processed!"})

if __name__ == '__main__':
    app.run(debug=True)
