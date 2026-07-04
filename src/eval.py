"""
검색 정확도 소규모 평가: 질문 -> 기대 KB 항목(topic id)이 top-k 안에 드는가 (precision@k, recall@k).
결과: results/eval.json
"""
import json
from pathlib import Path
from .rag import retrieve

# (질문, 기대 KB id) — 소규모 자체 테스트셋
TESTS = [
    ("충치를 어떻게 예방하나요?", "caries_prevention"),
    ("불소치약이 도움이 되나요?", "caries_prevention"),
    ("칫솔질은 어떻게 해야 하나요?", "brushing_flossing"),
    ("치실 꼭 써야 하나요?", "brushing_flossing"),
    ("잇몸에서 피가 나요", "gum_disease"),
    ("잇몸이 붓고 입냄새가 나요", "gum_disease"),
    ("치과 얼마나 자주 가야 하나요?", "checkup_interval"),
    ("아이 충치 예방 실런트", "children_oral"),
    ("단 간식 자주 먹으면 안 좋나요?", "diet_caries"),
    ("입이 자주 말라요", "dry_mouth"),
    ("틀니 관리 어떻게 하나요?", "denture_care"),
    ("당뇨랑 잇몸병 관련 있나요?", "oral_systemic"),
    ("언제 치과에 꼭 가야 하나요?", "when_to_see"),
    ("돈이 없어 치과 못 가는데 방법 있나요?", "access_equity"),
]


def run(k=3):
    hit1 = hit3 = 0
    rows = []
    for q, gold in TESTS:
        got = [d["id"] for d, _ in retrieve(q, k)]
        top1 = got[0] == gold
        ink = gold in got
        hit1 += top1; hit3 += ink
        rows.append({"q": q, "gold": gold, "top": got, "top1": top1, "in_topk": ink})
    n = len(TESTS)
    res = {"n": n, "k": k, "precision@1": hit1 / n, "recall@k": hit3 / n, "rows": rows}
    out = Path("results"); out.mkdir(exist_ok=True)
    json.dump(res, open(out / "eval.json", "w"), ensure_ascii=False, indent=2)
    print(f"precision@1 = {hit1}/{n} = {hit1/n:.2f}")
    print(f"recall@{k}  = {hit3}/{n} = {hit3/n:.2f}")
    for r in rows:
        if not r["in_topk"]:
            print("  MISS:", r["q"], "-> got", r["top"], "expected", r["gold"])
    return res


if __name__ == "__main__":
    run()
