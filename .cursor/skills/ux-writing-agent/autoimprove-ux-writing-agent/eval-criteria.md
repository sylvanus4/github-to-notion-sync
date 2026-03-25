# Eval Criteria: ux-writing-agent

## Binary Evals

EVAL 1: Five-Dimension Rubric Present
Question: Does the output include scores on all 5 quality dimensions (Clarity, Consistency, Actionability, Tone, Naturalness)?
Pass condition: All 5 dimensions scored with numeric values and a weighted total
Fail condition: Any dimension missing, or no numeric scoring at all

EVAL 2: Cloud Service Tone
Question: Does the generated copy use professional cloud-service appropriate language (no casual slang, no overly formal legalese)?
Pass condition: Copy reads naturally as enterprise SaaS UI text that a cloud user would expect
Fail condition: Contains casual expressions, emoji, slang, or stiff legalese unsuitable for cloud UI

EVAL 3: English Naturalness
Question: Is the English copy free of awkward phrasing, unnatural word order, or L2 artifacts?
Pass condition: A native English speaker would find nothing unnatural in the copy
Fail condition: Contains clearly unnatural phrasing, word-for-word translation patterns, or grammatical errors

EVAL 4: Boundary Respect
Question: Does the output stay within the requested sub-skill mode (generate/review/audit/quality-check) without drifting into another mode?
Pass condition: Output matches the requested mode's deliverable format
Fail condition: Generate mode produces an audit report, or review mode generates new copy instead of reviewing

EVAL 5: Actionable Output Format
Question: Is the output in a structured markdown format that can be directly used (not freeform prose)?
Pass condition: Output follows the skill's specified template with labeled sections
Fail condition: Unstructured freeform text without section headers or labels

## Test Scenarios

1. "Create error messages for API rate limit exceeded in a cloud dashboard"
2. "Review these 5 button labels for consistency and tone"
3. "Audit the UI strings in this component for policy compliance"
4. "Quality-check this set of tooltip texts for clarity and actionability"
5. "Generate empty state messages for a cloud storage management page"
