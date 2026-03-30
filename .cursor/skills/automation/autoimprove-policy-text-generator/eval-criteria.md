# Eval Criteria: policy-text-generator

## Binary Evals

EVAL 1: Policy Compliance
Question: 생성된 문구가 정책 조항의 핵심 내용을 정확히 반영하는가?
Pass condition: 근거 정책 조항이 명시되어 있고, 문구 내용이 해당 조항과 일치
Fail condition: 정책 조항 미명시, 또는 정책과 모순되는 내용 포함

EVAL 2: Tone Consistency
Question: 생성된 문구가 문구 유형별 톤 가이드를 따르는가?
Pass condition: 유형(에러/안내/응대 등)에 맞는 톤과 길이 기준 준수
Fail condition: 에러 메시지에 과도한 친근함, 약관에 비격식 표현 등 톤 불일치

EVAL 3: Multiple Candidates
Question: 최소 2개 이상의 문구 후보를 제시하는가?
Pass condition: 2개 이상 후보 + 각각의 근거 정책 명시
Fail condition: 단일 후보만 제시, 또는 근거 없는 후보

EVAL 4: Terminology Check
Question: 금지 표현을 사용하지 않고 필수 용어를 포함하는가?
Pass condition: 정책 유형별 필수 용어 포함, 금지 표현 미사용
Fail condition: 금지 표현 사용 또는 필수 법적/브랜드 용어 누락

EVAL 5: Actionable Output
Question: 출력이 바로 사용 가능한 형식인가?
Pass condition: 마크다운 출력 템플릿 형식 준수, 글자수 표시
Fail condition: 비정형 텍스트, 또는 미완성 placeholder 포함

## Test Scenarios

1. "과금 정책 기반 결제 실패 에러 메시지 3개 만들어줘"
2. "무료 플랜 API 제한 도달 안내 문구를 친근한 톤으로"
3. "개인정보 수집 동의 팝업 문구를 법적으로 정확하게"
4. "서비스 점검 안내 공지 문구 (SLA 정책 기반)"
5. "회원 탈퇴 시 데이터 삭제 안내 문구"
