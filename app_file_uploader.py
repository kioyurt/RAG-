import streamlit as st
from knowledge_base import KnowledgeBaseService
st.title("知识库更新服务")


uploader_file=st.file_uploader(
    "上传文件",
    type=["txt"],
    accept_multiple_files=False,

)

service=KnowledgeBaseService()

if "service" not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()
if uploader_file:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size/1024

    st.subheader(f"文件信息,文件名：{file_name}")
    st.write(f"格式:{file_type}  |  大小：{file_size} KB")

    text = uploader_file.getvalue().decode("utf-8")
    # st.write(text)
    with st.spinner("上传中..."):
        st.session_state["service"].upload_by_str(text,file_name)
































