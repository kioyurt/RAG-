md5_path="./md5.text"


collection_name="rag"


persist_directory="./chroma_db"

chunk_size=1000

chunk_overlap=100

separators=["\n\n", "\n", " ", "","!","?","。","，","；","：","、","（","）","【","】","《","》","."]


max_split_chat=100


similarity_threshold=2


session_config = {
    "configurable":{
        "session_id": "user_01",
    }
}


