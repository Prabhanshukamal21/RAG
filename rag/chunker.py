def split_text(text,chunk_size=900,chunk_overlap=150):
    if chunk_size<=0 or chunk_overlap<0 or chunk_overlap>=chunk_size:
        raise ValueError("Require chunk_size > chunk_overlap >= 0")
    text="\n".join(line.strip() for line in text.splitlines() if line.strip())
    chunks=[]; start=0
    while start<len(text):
        end=min(start+chunk_size,len(text))
        if end<len(text):
            boundary=text.rfind(" ",start+int(chunk_size*.65),end)
            if boundary>start: end=boundary
        piece=text[start:end].strip()
        if piece: chunks.append(piece)
        if end>=len(text): break
        start=max(end-chunk_overlap,start+1)
    return chunks
