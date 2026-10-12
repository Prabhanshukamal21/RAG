import requests
URL="http://localhost:11434/api/chat"
MODEL="llama3.2"

def generate_answer(question,results):
    context="\n\n---\n\n".join(f"[Source: {r['source']}, chunk {r['chunk_id']}]\n{r['text']}" for r in results)
    system=("Answer only from the supplied context. If it does not contain enough evidence, say so. "
            "Do not invent facts; mention source filenames where useful.")
    try:
        response=requests.post(URL,json={"model":MODEL,"stream":False,"options":{"temperature":0.2},
          "messages":[{"role":"system","content":system},{"role":"user","content":f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"}]},timeout=180)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError("Cannot connect to Ollama. Start Ollama and run: ollama pull llama3.2") from e
    except requests.exceptions.Timeout as e:
        raise RuntimeError("Ollama timed out. Try a smaller local model.") from e
    return response.json().get("message",{}).get("content","No answer returned.")
