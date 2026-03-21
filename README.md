# 项目名称

## 项目结构
- `ai/` - AI 图像识别服务（Flask 接口）
- `backend/` - 后端服务（待添加）
- `frontend/` - 前端页面（待添加）
- `requirements.txt` - 项目依赖

## 运行 AI 服务
1. 安装依赖：`pip install -r requirements.txt`
2. 进入 `ai` 目录：`cd ai`
3. 运行：`python app.py`
4. 接口：POST `/ai/ask`，请求体 JSON `{"image_url": "...", "question": "..."}`，返回 `{"answer": "..."}`。