"""Offline demo only: deterministic lexical retrieval, NOT Vertex AI Vector Search."""
from pathlib import Path

def search_policy(query: str):
    docs = list((Path(__file__).parents[3] / "data" / "policies").glob("*.txt"))
    tokens = set(query.lower().split())
    scored = []
    for path in docs:
        text = path.read_text(encoding="utf-8")
        score = len(tokens & set(text.lower().split()))
        if score: scored.append((score, path.name, text))
    return [{"source": name, "text": text} for _, name, text in sorted(scored, reverse=True)[:3]]
