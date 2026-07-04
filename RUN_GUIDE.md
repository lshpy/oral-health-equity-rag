# 실행 → 공개 → 증빙 (프로젝트3: 구강보건 RAG)

## 실행
```bash
cd 09_oral_health_rag
pip install -r requirements.txt
python -m src.eval           # 검색 정확도(precision@1, recall@3) 실측 -> results/eval.json
python -m src.rag "충치 예방법?"   # 단일 질의 테스트
python app.py                # Gradio 데모 -> HF Space 배포
```
- 기본은 추출식(안전). `ANTHROPIC_API_KEY` 설정 시 근거만으로 LLM 요약.
- 한국어 임베딩(ko-sroberta) 기본. `EMB_MODEL` 로 교체 가능.

## 공개 = 증빙
1. GitHub 별도 레포 push (예: `oral-health-equity-rag`)
2. `technical_note.md` 실수치 반영(이미 반영됨) → **Zenodo DOI** (ZENODO_SETUP 절차, ORCID 연결)
3. HF Space 배포(데모 URL), (선택) Papers with Code

## 증빙·자소서 반영
- 실적표 새 행: "구강보건 정보격차 완화 RAG 도우미 — 출처 우선·안전 가드레일, 한국어 검색 precision@1 0.93 (GitHub·HF·Zenodo DOI, 단독)".
- 자소서 봉사·사회적책임/특장점: "치과 접근이 어려운 이들에게 근거 있는 구강보건 정보를 전하는 도구를 직접 만들었다"(교육 도구, 진단 아님 명시).

## 정직성·안전
- 진단·처방 금지, 출처 인용, 응급 대면진료 안내. KB 출처는 권위 자료로 검증·교체.
- 결과 조작 0(본인 실행값). 실사용은 임상·법적 검토 후.
