# code-explorer Eval Criteria

## Binary Evals (Yes/No)

### EVAL 1: 기획 용어 변환
Question: 답변에서 기술 용어가 기획 용어로 변환되어 제공되는가?
Pass condition: useState→"화면 상태 관리", useQuery→"서버 데이터 조회" 등 변환 테이블의 용어가 적용됨
Fail condition: onClick, useState, useEffect 등 기술 용어가 변환 없이 사용됨

### EVAL 2: 답변 구조 완전성
Question: 답변에 "동작 설명", "코드 위치", "연관 기능" 3개 섹션이 모두 포함되어 있는가?
Pass condition: 3개 섹션이 모두 존재하며 각각 1줄 이상의 내용 포함
Fail condition: 3개 섹션 중 하나라도 누락

### EVAL 3: 한국어 답변
Question: 답변이 한국어로 작성되었는가?
Pass condition: 섹션 제목과 설명이 한국어
Fail condition: 영어로 된 설명이 주를 이룸

### EVAL 4: 코드 위치 정확성
Question: "코드 위치" 섹션에 실제 파일 경로가 명시되어 있는가?
Pass condition: 최소 1개의 파일 경로가 `src/...` 형태로 포함
Fail condition: 파일 경로 없음 또는 "어딘가에 있을 것" 같은 모호한 표현

## Test Inputs

### Input 1: 동작 질문
"로그인 버튼 누르면 무슨 일이 일어나?"

### Input 2: 상태 질문
"데이터가 없을 때 화면에 뭐가 보여?"

### Input 3: 히스토리 질문
"검색 기능 언제 추가됐어?"

## Baseline Configuration
- Runs per experiment: 5
- Max score: 20 (4 evals × 5 runs)
- Budget cap: 8 experiments
