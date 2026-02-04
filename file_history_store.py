import json, os
from typing import Sequence

from langchain_core.messages import messages_to_dict, messages_from_dict, BaseMessage

from langchain_core.chat_history import BaseChatMessageHistory


def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_message(self, message):
        """添加消息到历史记录中"""
        all_messages = list(self.messages)

        # 处理不同类型的消息输入
        if hasattr(message, '__iter__') and not isinstance(message, str):
            # 如果是可迭代对象（但不是字符串）
            all_messages.extend(message)
        else:
            # 单个消息对象
            all_messages.append(message)

        # 转换为字典格式保存
        new_messages = []
        for msg in all_messages:
            if hasattr(msg, 'type'):  # 确保是 BaseMessage 对象
                d = messages_to_dict([msg])[0]  # messages_to_dict 期望列表
                new_messages.append(d)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
