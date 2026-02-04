import os
import config_date as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

os.environ["DASHSCOPE_API_KEY"] = "yourkey"
os.environ["DASHSCOPE_API_MODEL"] = "qwen-max"
os.environ["DASHSCOPE_API_MODEL"] = "qwen-embed-v1.0"


def check_md5(md5_str: str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False


def save_md5(md5_str: str):
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str, encoding="utf-8"):
    b = input_str.encode(encoding)

    mobj = hashlib.md5()
    mobj.update(b)
    hex = mobj.hexdigest()
    return hex


class KnowledgeBaseService(object):
    def __init__(self):

        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(),
            persist_directory=config.persist_directory
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,

        )

    def upload_by_str(self, data, filename):
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return True
        if len(data) > config.max_split_chat:
            k_chunks: list[str] = self.spliter.split_text(data)

        else:
            k_chunks = [data]

        metdata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "admin",
        }

        self.chroma.add_texts(k_chunks, metdata=[metdata for _ in k_chunks])


        save_md5(md5_hex)
        return True
