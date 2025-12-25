import os
import sys
import io



import streamlit as st
from google import genai



import streamlit as st
from google import genai
import os

# --- 删掉了所有的 os.environ["HTTP_PROXY"] 设置 ---

# 1. 从 Secrets 读取 Key (确保你在 Streamlit 后台填了它)
if "MY_KEY" in st.secrets:
    MY_KEY = st.secrets["MY_KEY"]
else:
    st.error("请在 Streamlit Secrets 中配置 MY_KEY")
    st.stop()

# 2. 初始化客户端
client = genai.Client(api_key=MY_KEY)

st.title("我的云端 AI 助手")

# ... 后面的聊天界面代码保持不变 ...
# 记得模型名字依然用之前成功的 "gemini-2.0-flash"

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


