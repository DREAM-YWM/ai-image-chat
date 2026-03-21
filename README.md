### 运行 AI 服务
1. 进入 `ai` 目录：`cd ai`
2. 安装依赖：`pip install -r requirements.txt`
3. 运行：`python app.py`
4. 接口：POST `/ai/ask`，请求体 JSON `{"image_url": "...", "question": "..."}`，返回 `{"answer": "..."}`