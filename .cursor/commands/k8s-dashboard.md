---
description: "K8s GPU 대시보드 시작/재시작/중지/상태확인 (tools/gpu-dashboard)"
---

# /k8s-dashboard

K8s GPU 리소스 대시보드를 관리합니다. Node.js + Express 기반, http://localhost:3000 에서 실행됩니다.

## Usage

```
/k8s-dashboard              # 상태 확인 후 실행 (이미 실행 중이면 재시작)
/k8s-dashboard start        # 시작 (LIVE 모드, kubectl 필요)
/k8s-dashboard restart      # 재시작
/k8s-dashboard stop         # 중지
/k8s-dashboard status       # 상태 확인
/k8s-dashboard test         # TEST 모드로 시작 (mock 데이터, kubectl 불필요)
```

## Skill

Read and follow `.cursor/skills/infra/gpu-dashboard-ops/SKILL.md`.
