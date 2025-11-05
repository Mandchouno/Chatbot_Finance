import os, glob
from sentence_transformers import SentenceTransformer
import chromadb

_model = SentenceTransformer("all-MiniLM-L6-v2")  # rapide et léger
_client = chromadb.Client()
_col = _client.get_or_create_collection("kb_main")

def _bootstrap():
    if _col.count() > 0:
        return
    docs = []
    for p in glob.glob("data/knowledge/**/*", recursive=True):
        if os.path.isfile(p) and os.path.getsize(p) < 2_000_000 and p.split(".")[-1] in ["md","txt"]:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            docs.append((p, txt))
    if not docs:
        return
    ids = [f"doc-{i}" for i,_ in enumerate(docs)]
    texts = [d[1] for d in docs]
    metas = [{"path": d[0]} for d in docs]
    _col.add(ids=ids, documents=texts, metadatas=metas)

_bootstrap()

def answer_with_knowledge(question: str):
    if _col.count() == 0:
        return {"answer": "Ajoute des fichiers dans data/knowledge pour activer le RAG.", "sources": []}
    hits = _col.query(query_texts=[question], n_results=3)
    chunks = hits["documents"][0]
    paths  = [m["path"] for m in hits["metadatas"][0]]
    answer = "\n\n".join(chunks)[:1200]
    return {"answer": answer, "sources": paths}