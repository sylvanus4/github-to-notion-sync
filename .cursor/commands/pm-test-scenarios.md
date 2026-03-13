---
description: Generate comprehensive test scenarios from user stories — happy path, edge cases, error handling
argument-hint: "<user stories or feature description>"
---

# PM Test Scenarios

Generate comprehensive test scenarios from user stories or features. Cover happy path, edge cases, and error handling. Include a coverage matrix and test data requirements. Uses pm-execution skill, test-scenarios sub-skill.

## Usage
```
/pm-test-scenarios Generate scenarios from these user stories
/pm-test-scenarios 이 사용자 스토리에서 테스트 시나리오 만들어줘
/pm-test-scenarios Test cases for the checkout flow
/pm-test-scenarios 체크아웃 플로우 테스트 케이스
```

## Workflow

### Step 1: Ingest User Stories
- Accept user stories, job stories, or feature specs
- Extract: actors, flows, inputs, expected outcomes, constraints

### Step 2: Happy Path Scenarios
- For each story: nominal flow, ideal inputs, expected result
- Format: Given [precondition], When [action], Then [expected outcome]
- One scenario per distinct flow path

### Step 3: Edge Cases
- Boundary values: min/max, empty, null, duplicates
- Unusual but valid inputs: special chars, long strings, timezones
- Concurrency: simultaneous actions, race conditions (if applicable)

### Step 4: Error Handling
- Invalid inputs: wrong format, missing required fields
- Permission failures: unauthorized access, expired sessions
- System failures: timeout, network error, dependency down
- Clear expected behavior: error message, recovery path

### Step 5: Coverage Matrix and Test Data
- Matrix: Story × Scenario Type × Priority
- Test data requirements: sample users, datasets, environment config
- Flag scenarios needing specific fixtures (e.g., paid user, expired subscription)

## Notes
- Prioritize: P0 happy path, P1 edge cases, P2 error handling
- Link each scenario to originating story for traceability
- Test data: prefer realistic, anonymized data over obviously fake values
