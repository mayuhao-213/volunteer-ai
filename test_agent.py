import os
import shutil
import base64
import json
import mimetypes
from pathlib import Path
from dotenv import load_dotenv

# 导入智谱 SDK
from zhipuai import ZhipuAI 

# 加载环境变量
load_dotenv()
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

# 初始化 ZhipuAI 客户端
if not ZHIPU_API_KEY:
    raise ValueError("ZHIPU_API_KEY 未在 .env 文件中配置！")
client = ZhipuAI(api_key=ZHIPU_API_KEY)

# --- 待替换 ---
# TODO 1: 在这里填写你的测试文件路径
TEST_IMAGE_PATH = "uploads/test_photo.jpg" 
TEST_AUDIO_PATH = "uploads/test_audio.mp3"
# --- 待替换 ---


def file_to_base64(file_path: str) -> str | None:
    """将文件转换为 Base64 编码，并添加 Data URI Scheme（如：data:image/jpeg;base64,...）"""
    try:
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            print(f"警告：无法识别文件 MIME 类型: {file_path}")
            return None
        
        with open(file_path, "rb") as file:
            encoded_content = base64.b64encode(file.read()).decode('utf-8')
            return f"data:{mime_type};base64,{encoded_content}"
            
    except FileNotFoundError:
        print(f"错误：文件未找到: {file_path}")
        return None
    except Exception as e:
        print(f"Base64 转换失败: {e}")
        return None

def call_agent_multimodal(user_name: str, user_description: str, image_b64: str, audio_text: str) -> dict:
    """
    Agent 核心调用函数：接收图片、描述、音频转录文本，并输出结构化 JSON。
    """
    
    # ----------------------------------------------------
    # TODO 2: 核心 Prompt 调试区域
    # ----------------------------------------------------
    
    # 整合所有输入，准备发送给 Agent
    full_analysis_input = (
        f"用户姓名: {user_name}\n"
        f"用户自我描述: {user_description}\n"
        f"音频转录文本: {audio_text if audio_text else '（无音频转录文本）'}\n"
    )

    PROMPT_TEXT = f"""
    你是一个专业的、同理心强的**支教老师职业规划 Agent**。
    请结合用户上传的**图片、自我描述和音频文本转录**（三者必须全部纳入考量），
    为用户生成一份专业的分析报告，并严格按照要求的 JSON 格式输出。
    
    【核心分析要求】
    1. 性格画像：内容要求有同理心，必须结合图片中的**场景、人物状态**。
    2. 职业规划建议：给出具体的教育、心理或公益项目管理方向的建议。
    3. 爱好与潜能分析：从所有模态输入中推测其潜能。
    4. 三项能力得分：共情能力、抗压能力、沟通表达，分数在 80 到 99 之间。
    
    【输入数据】
    {full_analysis_input}
    
    请确保你的输出内容**只包含一个完整的 JSON 对象**，不要有任何多余的文字或解释。
    
    JSON 格式示例：
    {{
        "user_name": "{user_name}",
        "personality": "...",
        "career_advice": "...",
        "hobbies_analysis": "...",
        "scores": {{
            "empathy": 95,
            "resilience": 90,
            "communication": 88
        }}
    }}
    """
    # ----------------------------------------------------
    
    try:
        # 构建消息内容 (包含文本和图片)
        messages_content = [
            {"type": "text", "text": PROMPT_TEXT},
        ]
        if image_b64:
            messages_content.append({"type": "image_url", "image_url": {"url": image_b64}})

        print("正在调用 GLM-4V Agent 进行分析...")
        
        response = client.chat.completions.create(
            model="glm-4v", 
            messages=[
                {"role": "user", "content": messages_content}
            ],
            response_format={"type": "json_object"} 
        )
        
        json_string = response.choices[0].message.content
        return json.loads(json_string)
    
    except Exception as e:
        print(f"❌ GLM-4V Agent 调用失败: {e}")
        return {"error": str(e), "note": "请检查 API Key、模型权限或网络连接。"}

def main():
    """主调试函数"""
    print("--- 🔬 Agent 调试脚本启动 ---")
    
    # --- 待替换：硬编码的测试输入 ---
    TEST_USER_NAME = "王小美"
    TEST_DESCRIPTION = "我虽然是数学老师，但我发现自己对艺术和非虚构写作更感兴趣，在校期间组织过辩论社和乡村写生团。"
    TEST_AUDIO_TEXT = "（这里假装是 ASR 识别出的音频文本，例如：我在和学生交流时，声音总是很轻，但我表达的内容通常能被他们理解。）"
    # --- 待替换 ---

    # 1. 转换图片
    image_b64 = file_to_base64(TEST_IMAGE_PATH)
    if not image_b64:
        return
    
    # 2. 调用 Agent
    report = call_agent_multimodal(
        user_name=TEST_USER_NAME,
        user_description=TEST_DESCRIPTION,
        image_b64=image_b64,
        audio_text=TEST_AUDIO_TEXT
    )
    
    # 3. 打印结果
    print("\n--- ✅ Agent 分析结果 ---")
    print(json.dumps(report, indent=4, ensure_ascii=False))
    print("-------------------------")

if __name__ == "__main__":
    main()