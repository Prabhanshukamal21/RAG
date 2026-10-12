import streamlit as st
from rag.document_loader import load_uploaded_file
from rag.chunker import split_text
from rag.vector_store import VectorStore
from rag.generator import generate_answer

st.set_page_config(page_title="Local RAG Chatbot", page_icon="📚")
st.title("Local RAG Chatbot")
st.caption("Upload documents, then ask questions grounded in their contents.")

@st.cache_resource
def get_store():
    return VectorStore()
store=get_store()

with st.sidebar:
    st.header("Index documents")
    uploads=st.file_uploader("PDF, TXT, DOCX",type=["pdf","txt","docx"],accept_multiple_files=True)
    size=st.slider("Chunk size (characters)",300,1800,900,100)
    overlap=st.slider("Chunk overlap (characters)",0,300,150,25)
    if st.button("Index uploaded documents",type="primary",disabled=not uploads or overlap>=size):
        total=0
        for f in uploads:
            text,meta=load_uploaded_file(f)
            chunks=split_text(text,size,overlap)
            store.add_chunks(chunks,f.name,meta)
            total+=len(chunks)
        st.success(f"Indexed {total} chunks.")
    top_k=st.slider("Retrieved chunks (Top-K)",1,10,4)
    if st.button("Clear knowledge base"):
        store.clear()
        st.success("Knowledge base cleared.")
        st.rerun()

if "messages" not in st.session_state: st.session_state.messages=[]
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            with st.expander("Retrieved sources"):
                for s in m["sources"]: st.markdown(f"**{s['source']}**, chunk {s['chunk_id']}\n\n> {s['text']}")

q=st.chat_input("Ask a question about your documents...")
if q:
    st.session_state.messages.append({"role":"user","content":q})
    with st.chat_message("user"): st.markdown(q)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Retrieving evidence and generating answer..."):
                results=store.search(q,top_k)
                answer=generate_answer(q,results) if results else "The knowledge base is empty. Upload and index documents first."
            st.markdown(answer)
            sources=[{"source":r["source"],"chunk_id":r["chunk_id"],"text":r["text"]} for r in results]
            if sources:
                with st.expander("Retrieved sources"):
                    for s in sources: st.markdown(f"**{s['source']}**, chunk {s['chunk_id']}\n\n> {s['text']}")
            st.session_state.messages.append({"role":"assistant","content":answer,"sources":sources})
        except Exception as e:
            st.error(str(e))
