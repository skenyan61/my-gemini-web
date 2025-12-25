import os
import sys
import io



import streamlit as st
from google import genai

# --- 2. 强制网络代理 (请确保 7890 是你代理软件的端口) ---
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

import streamlit as st

if "MY_KEY" in st.secrets:
    MY_KEY = st.secrets["MY_KEY"]
else:
    # 这样你在本地没配置 secrets 时，也可以手动填入做测试
    MY_KEY = "你的本地测试KEY"

# --- 4. 初始化 AI 客户端 ---
try:
    client = genai.Client(api_key=MY_KEY)
except Exception as e:
    st.error(f"初始化失败: {e}")

st.set_page_config(page_title="Gemini AI 助手", layout="centered")
st.title("🤖 我的私人 AI 助手")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示对话历史
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 用户输入框
if prompt := st.chat_input("想问点什么？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner('正在连接 Google 节点...'):
                # 尝试生成内容
                response = client.models.generate_content(
                    model="gemini-3-flash-preview", 
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # --- 5. 报错诊断区 ---
            st.error(f"❌ 运行出错了: {e}")
            
            st.write("---")
            st.warning("正在为您诊断... 请查看下方您的 API Key 权限支持的模型列表：")
            try:
                # 如果 404，这行代码会列出你所有能用的模型
                for model_info in client.models.list():
                    st.code(model_info.name)
                st.info("提示：请对比上面的列表。如果列表中没有 'models/gemini-1.5-flash'，请在代码里更换模型名称。")
            except:
                st.error("无法获取模型列表，这通常意味着您的 API Key 彻底失效或网络完全不通。")
