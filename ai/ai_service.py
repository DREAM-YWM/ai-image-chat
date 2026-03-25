import os
import dashscope
from dashscope import MultiModalConversation
from rag_utils import init_rag, get_rag_knowledge

# ========== 配置 ==========
API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-372806411bad428289fb6a0bfa24c426")
dashscope.api_key = API_KEY
dashscope.timeout = 60          # 超时时间，可根据网络调整

# 初始化 RAG（知识库）
rag_components = init_rag()
if rag_components is None:
    print("⚠️ RAG 加载失败，将使用无知识库模式")
# ==========================

def ask_ai(image_url: str, question: str) -> str:
    """
    给定图片 URL 和问题，返回 AI 回答（纯文本）
    """
    # 1. 获取 RAG 知识（如果可用）
    knowledge = ""
    if rag_components:
        try:
            knowledge = get_rag_knowledge(rag_components, question)
        except Exception as e:
            print(f"RAG 知识获取失败: {e}")

    # 2. 构建 prompt（知识作为上下文）
    if knowledge:
        enhanced_prompt = f"请结合以下建筑/户型专业知识，回答用户问题：\n{question}\n\n相关知识：{knowledge}"
    else:
        enhanced_prompt = question

    # 3. 构造多模态消息
    messages = [{
        "role": "user",
        "content": [
            {"image": image_url},
            {"text": enhanced_prompt}
        ]
    }]

    # 4. 调用千问模型
    try:
        response = MultiModalConversation.call(
            model="qwen-vl-plus",   # 根据实际模型调整
            messages=messages,
        )
        # ✅ 调试打印：查看模型原始返回（可删除）
        print("原始返回:", response.output.choices[0].message.content)
    except Exception as e:
        raise Exception(f"模型调用失败: {str(e)}")

    # 5. 提取回答
    if response is None or not hasattr(response, 'output') or response.output is None:
        raise Exception("模型返回空结果")

    reply = response.output.choices[0].message.content

    # 处理不同返回格式
    if isinstance(reply, list) and len(reply) > 0:
        reply = reply[0].get("text", "")
    elif isinstance(reply, str):
        pass
    else:
        reply = str(reply)

    # 6. 最终校验
    if not reply or not reply.strip():
        raise Exception("模型返回结果为空")

    # 直接返回（不需要额外 unicode 解码）
    return reply
