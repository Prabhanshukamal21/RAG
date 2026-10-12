import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self,path="data/chroma_db",collection_name="rag_documents"):
        self.client=chromadb.PersistentClient(path=path)
        self.name=collection_name
        self.collection=self.client.get_or_create_collection(name=self.name,metadata={"hnsw:space":"cosine"})
        self.embedder=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    def add_chunks(self,chunks,source,base_metadata=None):
        base_metadata=base_metadata or {}
        offset=self.collection.count()
        vectors=self.embedder.encode(chunks,normalize_embeddings=True).tolist()
        ids=[f"{source}::{offset+i}" for i in range(len(chunks))]
        metas=[{"source":source,"chunk_id":offset+i,**{k:str(v) for k,v in base_metadata.items()}} for i in range(len(chunks))]
        self.collection.upsert(ids=ids,documents=chunks,embeddings=vectors,metadatas=metas)
    def search(self,query,top_k=4):
        count=self.collection.count()
        if not count: return []
        vector=self.embedder.encode([query],normalize_embeddings=True).tolist()
        res=self.collection.query(query_embeddings=vector,n_results=min(top_k,count),include=["documents","metadatas","distances"])
        return [{"text":t,"source":m.get("source","unknown"),"chunk_id":m.get("chunk_id","?"),"distance":float(d)} for t,m,d in zip(res["documents"][0],res["metadatas"][0],res["distances"][0])]
    def clear(self):
        self.client.delete_collection(self.name)
        self.collection=self.client.get_or_create_collection(name=self.name,metadata={"hnsw:space":"cosine"})
