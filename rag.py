from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda

from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from file_history_store import get_history

os.environ["DASHSCOPE_API_KEY"] = "yourkey"
os.environ["DASHSCOPE_API_MODEL"] = "qwen3-max"
os.environ["DASHSCOPE_API_MODEL"] = "qwen-embed-v1.0"


class RagService(object):

    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings()
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "你是一个智能助手,以参考资料为主：{content},回答问题。并且我提供用户的对话历史记录，如下："),
                MessagesPlaceholder("history"),
                ("human", "回答提问：{input}")
            ]
        )
        self.chat_model = ChatTongyi()
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        def format_doc(input: list[Document]):
            if not input:
                return "no files"
            formatted_str = ""
            for doc in input:
                formatted_str += f"{doc.page_content},{doc.metadata}"
            return formatted_str

        def temp1(value) -> str:
            return value["input"]

        def temp2(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["content"] = value["content"]
            # 从 RunnableWithMessageHistory 获取历史记录
            new_value["history"] = value.get("history", [])
            return new_value

        chain = (
                {
                    "input": RunnablePassthrough(),
                    "content": RunnableLambda(temp1) | retriever | format_doc
                } | RunnableLambda(temp2) | self.prompt_template | self.chat_model | StrOutputParser()
        )

        conversion_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",

        )

        return conversion_chain
