# Definition of Done — Nested Semantic Graph

**Project:** Nested Semantic Graph
**Phase:** P2 Execution
**Last Updated:** 2026-05-22

## What "Done" Means for This Project

A task is **done** only when ALL applicable criteria below are satisfied. Tasks marked complete without satisfying DoD criteria are `[~]` in-progress, not `[x]` complete.

## DoD Criteria by Deliverable Type

### A. Document Deliverables (e.g., 0.1.md, 0.2.md, 0.3.md, 0.4.md)

- [ ] File exists on disk (Test-Path confirmed)
- [ ] File has non-zero size (Get-Item .Length > 0)
- [ ] All claims traceable to source: `[CODE-EXECUTED]`, `[EXTERNAL-SOURCE: path]`, or `[LLM-INFERRED]`
- [ ] All mathematical content in $...$ or $$...$$ (no bare Unicode math)
- [ ] No placeholder DOIs (`########`, `XXXX`)
- [ ] Date fields verified against `datetime.date.today()`
- [ ] No generation artifacts (bracket-delimited markers)
- [ ] References section is complete and accurate
- [ ] Git-committed with descriptive message

### B. Python Code Deliverables (e.g., 0.2.py)

- [ ] File exists on disk
- [ ] Executes without errors (Python exit code 0)
- [ ] All verification checks pass (explicit PASS/FAIL output)
- [ ] No Unicode outside cp1252 in critical output
- [ ] Self-contained: only standard library imports unless documented
- [ ] Docstrings explain purpose of each function/class
- [ ] Git-committed with descriptive message

### C. Project Management Updates

- [ ] SPRINT.md updated with task status change
- [ ] CHANGELOG.md updated with deliverable entry
- [ ] PROJECT STATE.md updated with current status
- [ ] All changes committed to feature branch

### D. Cross-Linguistic / Linguistics Deliverables

- [ ] Language examples labeled `[LLM-INFERRED]` unless verified against native speaker or reference grammar
- [ ] Mohawk/Iroquoian examples follow standard Iroquoianist transcription conventions
- [ ] Entropy/statistical values from Language-Info-Architecture cited with "synthetic data" caveat

### E. Publication-Quality Standards

- [ ] Reader testing conducted (REVIEWER subagent, §11.5 protocol)
- [ ] All `[BLOCKING]` and `[MAJOR]` issues resolved
- [ ] Publication Language Gate scan passed (§11.7)
- [ ] YAML frontmatter complete (if publication document)
- [ ] Curly/smart quotes in body text (Python scan verified)
- [ ] Publication-ready filename (descriptive, not versioned)

---

## Current Sprint Tasks and Their DoD

| Task ID | DoD Criteria Applicable | Status |
|:--------|:------------------------|:-------|
| S0 — Internal Literature Review | All A criteria | [x] |
| S1 — Formal Definitions | A (document) + B (code) + C (project mgmt) | [x] |
| S2 — Search Spec | A (document) + C (project mgmt) | [x] |
| S3 — Cross-Linguistic Examples | A + D + C | [x] |
| S4 — Python Prototype | B + C | [ ] |
| S5 — Computational Pathway | A + C | [ ] |
| S6 — Reader Testing | A + E + C | [ ] |

---
*Generated from DEFINITION-OF-DONE-TEMPLATE.md v1.0.*
