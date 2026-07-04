# Equitable Oral-Health Assistant — Citation-First Retrieval (RAG)

닿기 어려운 사람에게 **믿을 수 있는 구강보건 정보**를 쉬운 말로, **항상 출처와 함께** 전달하는
검색기반(RAG) 질의응답 도구. 정보 접근의 평등(equity)을 목표로 한다.

> ⚠️ **교육용 정보이며 진단·처방이 아님.** 모든 답변은 근거 문서에서만 나오고 출처를 인용하며,
> 증상·응급 상황에는 반드시 **치과의사 대면 진료를 권한다.** (안전 가드레일 내장)
> 이 원칙은 "왜 그 판단인지 근거를 보인다"는 설명가능성(XAI) 철학과 같은 선상.

## 왜 이 프로젝트인가
- **평등·접근성**: 치과 접근이 어려운 취약계층에게 신뢰할 정보를 낮은 문턱으로.
- **출처 우선(안전)**: 환각을 막기 위해 **근거 문서에서만** 답하고 출처를 표시 → 의료 정보의 신뢰성.
- 서울대 봉사비전(소외계층 구강보건·재능 나눔)·의료정보/NLP 연구와 정렬.

## 동작
1. 공개 구강보건 지식베이스(KB)를 문장 임베딩(all-MiniLM)으로 색인.
2. 질문 임베딩 → 코사인 top-k 근거 문서 검색.
3. **근거 문서에서만** 답 구성(+출처 인용 + 안전 고지). (선택) ANTHROPIC_API_KEY 있으면 Claude가 그 근거만으로 쉬운 말 요약 — 새 정보 추가·진단 금지.
4. 응급·진단성 질문은 전문 진료 안내로 라우팅.

## 구조
```
09_oral_health_rag/
├── README.md · requirements.txt · RUN_GUIDE.md
├── data/kb.jsonl            # 공개 구강보건 KB(출처 필드 포함, 검증·교체 대상)
├── src/rag.py               # 임베딩·검색·근거기반 답변·안전 가드레일
├── src/eval.py              # 검색 정확도(precision@k) 소규모 평가
├── app.py                   # Gradio 데모(HF Space 배포용)
└── technical_note/technical_note.md
```

## 빠른 시작
```bash
pip install -r requirements.txt
python -m src.eval          # 검색 정확도(precision@k) 실측
python app.py               # 로컬 데모 → HF Space에 그대로 배포
```

## 정직성·안전
- 진단·처방 금지, 출처 인용 필수, 응급은 대면진료 안내.
- KB의 `source`는 **권위 있는 공개 자료로 검증·교체**(WHO Oral Health, 질병관리청 구강보건, 대한치과의사협회 등).
- 결과·성능은 본인 실행값(조작 0).
