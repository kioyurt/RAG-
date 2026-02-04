import streamlit as st
from rag import RagService
import config_date as config
st.title("个人知识库助手")
st.divider()

rag_service = RagService()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "欢迎来到知识库助手，你可以向我提问任何问题."}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    ai_list = []
    with st.spinner("wait a little"):

        def cap(gen,cache):
            for i in gen:
                cache.append(i)
                yield i


        res = st.session_state["rag"].chain.stream({"input": prompt},config.session_config)
        st.chat_message("assisant").write_stream(cap(res,ai_list))




        st.session_state["message"].append(
            {"role": "assistant", "content": "".join(ai_list)}
        )
