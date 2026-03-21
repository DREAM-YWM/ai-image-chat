import os
import dashscope
from dashscope import MultiModalConversation
from rag_utils import init_rag, get_rag_knowledge  # 恢复 RAG 导入

# ------------------- 配置 -------------------
API_KEY = "sk-372806411bad482289fb6a0bfa24c426"
dashscope.api_key = API_KEY
# ------------------- 配置 -------------------

if __name__ == "__main__":
    print("=== 千问V3图文对话机器人+RAG知识库 ===")
    print("用法：输入「图片URL]加载→再提问\n")

    current_image_url = None
    rag_components = init_rag()
    if rag_components is None:
        print("⚠️ RAG加载失败，将使用无知识库模式")

    while True:
        user_input = input("你：").strip()
        if not user_input:
            continue
        if user_input.lower() == "退出":
            break

        # 处理图片指令
        if user_input.startswith("图片"):
            parts = user_input.split(maxsplit=1)
            img_url = parts[1].strip() if len(parts) > 1 else ""
            if not img_url.startswith("http"):
                print("❌ 请输入有效的图片URL（以http/https开头）\n")
                current_image_url = None
                continue
            current_image_url = img_url
            print("✅ 图片URL加载成功！可以提问啦~\n")
            continue

        # 正常对话 + RAG
        try:
            # 获取 RAG 知识
            rag_knowledge = get_rag_knowledge(rag_components, user_input) if rag_components else ""
            if rag_knowledge:
                enhanced_prompt = f"""请结合以下建筑/户型专业知识，回答用户问题：
---
{rag_knowledge}
---
用户问题: {user_input}"""
            else:
                enhanced_prompt = f"用户问题: {user_input}"

            # 构造消息
            messages = []
            if current_image_url:
                messages.append({
                    "role": "user",
                    "content": [
                        {"image": current_image_url},
                        {"text": enhanced_prompt}
                    ]
                })
            else:
                messages.append({
                    "role": "user",
                    "content": [{"text": enhanced_prompt}]
                })

            # 调用千问图文模型
            response = MultiModalConversation.call(
                model="qwen-vl-plus",  # 使用正确的模型名
                messages=messages
            )

            if response is None or not hasattr(response, 'output') or response.output is None:
                print("❌ 模型返回空结果，请检查网络或URL有效性\n")
                continue

            reply = response.output.choices[0].message.content[0]["text"]
            print(f"机器人：{reply}\n")

        except Exception as e:
            print(f"❌ 出错：{str(e)}\n")