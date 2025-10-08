from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 设置OpenAI API密钥（建议你改为Render环境变量）
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    age = data.get("age")
    gender = data.get("gender")
    wall = data.get("wall")
    stone = data.get("stone")
    colic = data.get("colic")
    inflammation = data.get("inflammation")
    chronic = data.get("chronic")

    prompt = f"""
你是肝胆外科医生，请根据以下超声评估参数判断是否建议保胆，并用口语化中文说明理由：
- 年龄：{age}
- 性别：{gender}
- 胆囊壁厚度：{wall} mm
- 结石最大直径：{stone} mm
- 是否有胆绞痛：{colic}
- 是否半年内有胆囊炎：{inflammation}
- 慢性病史：{chronic}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "你是一个经验丰富的肝胆外科医生，擅长通俗易懂地解释保胆相关问题。"},
            {"role": "user", "content": prompt}
        ]
    )

    result = response["choices"][0]["message"]["content"]
    return jsonify({"result": result})

@app.route("/", methods=["GET"])
def home():
    return "AskDrLiu AI Flask 后端已启动"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)