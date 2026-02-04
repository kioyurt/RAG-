from langchain_chroma import Chroma
import config_date as config




class VectorStoreService(object):
    def __init__(self,embedding):
        self.embedding= embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            persist_directory=config.persist_directory,
            embedding_function=self.embedding,
        )


    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": 2})



















