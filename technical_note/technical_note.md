# A Citation-First Oral-Health Assistant for Information-Access Equity: A Preliminary Retrieval Study

**Author:** Seunghyun Lee — ORCID [0009-0006-1926-653X](https://orcid.org/0009-0006-1926-653X)
**Date:** 2026-0X  **Type:** Preliminary technical report (not peer-reviewed)
> ⚠️ 교육용 정보 도구(진단·처방 아님). 블라인드 자소서 본문엔 실명·ORCID 미기재; 이 공개본에만.

## Abstract
치과 접근이 어려운 사람에게 신뢰할 구강보건 정보를 **출처와 함께** 전달하는 검색기반(RAG) 도우미를 만들고, 한국어 질의에서의 검색 정확도를 예비 평가했다. 11개 구강보건 항목 KB와 14개 질문으로, **영어 임베딩(all-MiniLM)** 은 precision@1 0.29에 그쳤으나 **한국어 임베딩(ko-sroberta)** 으로 교체하자 **precision@1 0.93, recall@3 1.00** 으로 크게 향상됐다. 모든 답변은 근거 문서에서만 생성되고 출처를 인용하며, 응급·진단성 질의는 대면 진료로 안내한다. 정보 접근의 평등을 목표로 한 안전 우선 설계다.

## 1. Introduction
- 동기: 형편·지역에 따른 치과 접근 격차 → 신뢰할 정보의 낮은 문턱 제공(equity).
- 원칙: 의료 정보의 신뢰성을 위해 **환각 방지(근거에서만 답)+출처 인용**. 이는 "판단 근거를 보인다"는 설명가능성 철학과 같은 선상.

## 2. Method
- KB: 11개 구강보건 항목(예방·칫솔질·치주·검진·아동·식이·구강건조·보철·구강-전신·응급·**취약계층 접근**), 각 항목에 출처 필드.
- 임베딩 검색: 문장 임베딩 코사인 top-k. 답변은 근거 문서에서만(추출식) 또는 (API 키 시) 근거만으로 LLM 요약. 진단 금지·출처 인용·응급 라우팅.

## 3. Preliminary Results (KB=11, 질문=14)
| 임베딩 | precision@1 | recall@3 |
|---|---|---|
| all-MiniLM (영어) | 0.29 | 0.50 |
| **ko-sroberta (한국어)** | **0.93** | **1.00** |
- 관찰: 한국어 의료 질의에서는 **언어 적합 임베딩이 결정적**. 접근성 질문("돈이 없어 치과 못 가는데")도 '취약계층 구강보건 접근'을 최상위로 검색.
- 안전: 응급 키워드 시 대면진료 경고 선행, 모든 답에 진단 아님 고지.

## 4. Limitations
소규모 KB·자체 테스트셋·예비. KB 출처는 권위 자료로 검증·교체 필요. 실사용 전 임상·법적 검토 필요(진단 도구 아님).

## 5. Conclusion
출처 우선·안전 우선의 구강보건 정보 도구가 접근 격차 완화에 기여할 수 있음을 예비적으로 보였다. 향후 권위 KB 확충·다국어·사용자 평가로 확장.

## Artifacts
Code: [GitHub URL] · DOI: [Zenodo DOI] · Author ORCID: 0009-0006-1926-653X

## References
[1] Reimers & Gurevych, Sentence-BERT. [2] ko-sroberta (jhgan). [3] 구강보건 공개 자료(검증·인용 예정).
