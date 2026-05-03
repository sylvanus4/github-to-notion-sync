---
name: release-commander
description: Full release lifecycle orchestrator chaining 10 skills — code review, security, tests, performance, i18n, dependencies, changelog, commits, PR summary, and PR creation.
disable-model-invocation: true
---

Orchestrate the complete pre-release validation pipeline.

## Pipeline (Sequential)

1. **Code Review** (4 parallel domain agents): frontend, backend/DB, security, test coverage
2. **Security Scan**: OWASP Top 10, secret detection, dependency CVEs
3. **Test Validation**: Run test suites, check coverage thresholds
4. **Performance Check**: Verify no regressions against SLO targets
5. **i18n Sync**: Check translation key consistency across locales
6. **Dependency Audit**: Scan for known CVEs in dependencies
7. **Changelog Generation**: Create structured changelog from commits
8. **Domain-Split Commits**: Organize changes into clean bisectable commits
9. **PR Summary**: Generate comprehensive PR description
10. **PR Creation**: Open the pull request with all metadata

## Quality Gate

- All 10 stages must PASS
- Any FAIL blocks the release with specific remediation steps

## Output

- Structured pass/fail report per stage
- PR URL on success
- Remediation list on failure
