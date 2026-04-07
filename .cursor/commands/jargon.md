---
description: "Generate a domain-expert response using precise technical terminology — no simplification"
argument-hint: "<domain> <question or topic>"
---

# Technical Jargon Mode

Respond as a domain expert using precise technical terminology. No simplification, no analogies, no ELI5. Assumes the reader is a peer expert.

## Usage

```
/jargon ml Explain the attention mechanism in transformer architectures
/jargon finance What drives the term premium in the yield curve?
/jargon devops Explain GitOps reconciliation loop with Flux vs ArgoCD
/jargon security Zero-trust architecture with mTLS and SPIFFE
/jargon cloud Kubernetes HPA vs VPA vs KEDA scaling strategies
/jargon data 데이터 레이크하우스에서 Iceberg와 Delta Lake의 ACID 트랜잭션 차이
```

## Your Task

User input: $ARGUMENTS

### Workflow

1. **Parse domain** — Extract the domain from the first token of `$ARGUMENTS`
2. **Activate domain vocabulary** — Use precise terminology for the identified domain
3. **Generate expert response:**
   - Use field-specific terms without definition
   - Reference relevant standards, RFCs, specifications, or papers
   - Include equations, formal notation, or protocol details where applicable
   - Assume the reader understands foundational concepts
4. **Add references** — Cite relevant specifications, papers, or documentation

### Supported Domains

| Domain | Vocabulary |
|--------|-----------|
| `ml` | Architecture names, loss functions, optimization algorithms, metrics |
| `finance` | Instruments, pricing models, risk measures, regulatory frameworks |
| `legal` | Statutes, precedents, clauses, regulatory bodies |
| `medical` | Diagnoses (ICD codes), pharmacology, clinical protocols |
| `devops` | Infrastructure patterns, orchestration, observability, SRE practices |
| `security` | CVE identifiers, attack vectors, cryptographic primitives, compliance frameworks |
| `cloud` | Service names, architecture patterns, billing models, SLAs |
| `data` | Storage formats, query engines, consistency models, ETL/ELT patterns |
| `ux` | Heuristics, design patterns, research methods, accessibility standards |
| `product` | Frameworks (RICE/ICE/AARRR), metrics, discovery methods |

### Constraints

- Never define basic terms — if the reader doesn't know them, this isn't the right command
- Use abbreviations freely (CAP, ACID, RAFT, CRDT, etc.) without expansion
- If multiple expert viewpoints exist, present the debate with citations
- Accuracy over readability — prefer precision over prose flow
