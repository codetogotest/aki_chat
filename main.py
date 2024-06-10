import streamlit as st
from langchain.memory import ConversationBufferMemory

from utils import get_chat_response

st.set_page_config(
    page_title="Aki 簡易版聊天機器人",
    page_icon=":sparkles:",
    layout="centered",
)

st.title("💬 Aki 簡易版聊天機器人")

with st.sidebar:
    openai_api_key = st.text_input("請輸入OpenAI API Key：", type="password")
    st.markdown(
        "[如何取得OpenAI API key](https://platform.openai.com/account/api-keys)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "您好，我是你的AI聊天小幫手，有什麼可以幫助您呢？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    if not openai_api_key:
        st.info("請輸入你的OpenAI API Key")
        st.stop()
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，請稍後..."):
        response = get_chat_response(prompt, st.session_state["memory"],
                                     openai_api_key)
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)
