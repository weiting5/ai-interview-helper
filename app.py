import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompt_builder import build_prompt
from utils import call_deepseek, save_history


# =========================
# 1. 读取环境变量
# =========================
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    st.error("没有读取到 DEEPSEEK_API_KEY，请检查 .env 文件位置和写法。")
    st.stop()


# =========================
# 2. 初始化 DeepSeek 客户端
# =========================
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)


# =========================
# 3. 页面基础设置
# =========================
st.set_page_config(
    page_title="AI 面试题生成器",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 AI 面试题生成器")
st.write("输入岗位信息，自动生成面试题、参考答案、自我介绍和复习计划。")


# =========================
# 4. 页面说明
# =========================
st.markdown("""
这个工具可以根据你的岗位目标、公司类型和个人基础，自动生成适合实习生或初级岗位的面试准备内容。

适合用于：
- 面试前快速准备
- 梳理高频问题
- 生成自我介绍
- 优化项目表达
""")


# =========================
# 5. 页面输入区
# =========================
with st.sidebar:
    st.header("填写面试信息")

    job = st.text_input(
        "岗位名称",
        placeholder="例如：软件测试实习生 / Python后端开发 / AI应用开发实习生"
    )

    direction = st.selectbox(
        "岗位方向",
        ["软件测试", "测试开发", "Python后端", "AI应用开发", "前端开发", "其他"]
    )

    company = st.text_input(
        "公司类型",
        placeholder="例如：软件公司 / AI公司 / 智能制造 / 互联网公司"
    )

    level = st.text_area(
        "我的基础",
        placeholder="例如：会一点 Python 基础，了解测试用例，项目经验较少",
        height=150
    )

    difficulty = st.selectbox(
        "面试难度",
        ["基础", "中等", "偏难"]
    )

    output_type = st.multiselect(
        "你想生成哪些内容？",
        ["高频面试题", "参考答案", "自我介绍", "项目经历包装建议", "面试前复习清单"],
        default=["高频面试题", "参考答案", "自我介绍", "面试前复习清单"]
    )


# =========================
# 6. 点击按钮后生成内容
# =========================
if st.button("开始生成面试准备内容", type="primary"):
    if not job or not company or not level or not output_type:
        st.warning("请把岗位名称、公司类型、你的基础和生成内容都填写完整。")
    else:
        prompt = build_prompt(
            job=job,
            direction=direction,
            company=company,
            level=level,
            difficulty=difficulty,
            output_type=output_type
        )

        with st.spinner("AI 正在生成中，请稍等..."):
            try:
                result = call_deepseek(client, prompt)
                saved_path = save_history(result)

                st.success(f"生成完成！已自动保存到：{saved_path}")
                st.subheader("生成结果")
                st.markdown(result)

                file_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"interview_prepare_{file_time}.txt"

                st.download_button(
                    label="下载面试准备内容",
                    data=result,
                    file_name=file_name,
                    mime="text/plain"
                )

            except Exception as e:
                st.error("生成失败，请检查 API Key、网络连接或账户余额。")
                st.code(str(e))