from flask import Flask, request, jsonify
from ai_service import ask_ai

app = Flask(__name__)
# ✅ 关键配置：让 Flask JSON 响应不转义中文，直接返回可读中文
app.config['JSON_AS_ASCII'] = False


@app.route('/ai/ask', methods=['POST'])
def ai_ask():
    try:
        data = request.get_json()
        image_url = data.get("image_url")
        question = data.get("question")

        if not image_url or not question:
            return jsonify({"error": "缺少image_url或question参数"}), 400

        answer = ask_ai(image_url, question)
        return jsonify({"answer": answer}), 200

    except Exception as e:
        app.logger.error(f"AI调用失败: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)