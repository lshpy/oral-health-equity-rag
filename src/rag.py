"""
구강보건 RAG — 임베딩 검색 + 근거기반 답변 + 안전 가드레일.
- 답변은 KB(근거 문서)에서만. 출처 인용. 진단·처방 금지. 응급은 대면진료 안내.
- ANTHROPIC_API_KEY 있으면 Claude가 '검색된 근거만으로' 쉬운 말 요약(새 정보 금지). 없으면 추출식.
"""
import json, os
from pathlib import Path
import numpy as np

_KB = None
_EMB = None
_MODEL = None

KB_PATH = Path(__file__).resolve().parent.parent / "data" / "kb.jsonl"

DISCLAIMER = ("ℹ️ 이 답변은 교육용 정보이며 진단·처방이 아닙니다. "
             "증상이 있으면 치과의사의 대면 진료를 받으시길 권합니다.")
EMERGENCY_KWS = ["얼굴이 붓", "얼굴 붓", "붓고 열", "발열", "숨쉬기", "삼키기 어렵", "출혈이 멈추지", "심하게 부", "고열"]
URGENT_MSG = ("⚠️ 얼굴 부기·심한 통증·발열·호흡/삼킴 곤란 등은 응급 신호일 수 있습니다. "
              "지체 없이 치과 또는 응급실 진료를 받으세요.")


def _load():
    global _KB, _EMB, _MODEL
    if _KB is not None:
        return
    from sentence_transformers import SentenceTransformer
    _KB = [json.loads(l) for l in open(KB_PATH, encoding="utf-8") if l.strip()]
    # 한국어 의미검색: 다국어/한국어 임베딩 모델 (영어 all-MiniLM 대비 크게 향상)
    _MODEL = SentenceTransformer(os.environ.get("EMB_MODEL", "jhgan/ko-sroberta-multitask"))
    texts = [f"{d['topic']}. {d['text']}" for d in _KB]
    _EMB = _MODEL.encode(texts, normalize_embeddings=True)


def retrieve(query, k=3):
    _load()
    q = _MODEL.encode([query], normalize_embeddings=True)[0]
    sims = _EMB @ q
    idx = np.argsort(-sims)[:k]
    return [(_KB[i], float(sims[i])) for i in idx]


def _extractive_answer(query, hits):
    parts = []
    for d, s in hits:
        parts.append(f"• [{d['topic']}] {d['text']}\n  (출처: {d['source']})")
    return "다음 근거 자료를 참고하세요:\n\n" + "\n\n".join(parts)


def _claude_answer(query, hits):
    import anthropic
    ctx = "\n\n".join(f"[{d['topic']}] {d['text']} (출처: {d['source']})" for d, _ in hits)
    client = anthropic.Anthropic()
    model = os.environ.get("ANSWER_MODEL", "claude-haiku-4-5-20251001")
    sys = ("너는 구강보건 교육 도우미다. 아래 <근거>에 있는 내용만으로 쉬운 말로 답하라. "
           "근거에 없는 내용·진단·처방은 하지 마라. 답 끝에 참고한 항목명을 괄호로 표시하라. "
           "증상·응급이면 치과 대면진료를 권하라.")
    msg = client.messages.create(model=model, max_tokens=400, system=sys,
        messages=[{"role": "user", "content": f"<근거>\n{ctx}\n</근거>\n\n질문: {query}"}])
    return msg.content[0].text


def answer(query, k=3):
    hits = retrieve(query, k)
    urgent = any(kw in query for kw in EMERGENCY_KWS)
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            body = _claude_answer(query, hits)
        except Exception:
            body = _extractive_answer(query, hits)
    else:
        body = _extractive_answer(query, hits)
    out = ""
    if urgent:
        out += URGENT_MSG + "\n\n"
    out += body + "\n\n" + DISCLAIMER
    sources = [{"topic": d["topic"], "source": d["source"], "score": round(s, 3)} for d, s in hits]
    return out, sources


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "충치를 어떻게 예방하나요?"
    a, s = answer(q)
    print(a)
    print("\n---sources---")
    for x in s:
        print(x)
