# Changelog — Nested Semantic Graph

All notable changes documented here. Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Sprint 6 — 2026-05-22] Final Completion

### Added
- `demo.py`: Quick-start script — one command demonstrates the entire project
- `.gitignore`: Python cache and OS artifact exclusions

### Changed
- `0.8.py`, `0.9.py`, `0.10.py`, `0.11.py`: All refactored to import from `nst_core.py`
- `SPRINT.md`, `BACKLOG.md`, `CHANGELOG.md`, `PROJECT STATE.md`: Final documentation refresh

## [Sprint 5 — 2026-05-22] Production Readiness

### Added
- `nst_core.py`: Canonical shared library — NestedSemanticTree, subtree matching, tree edit distance, match pipeline, builders
- `0.13.py`: Large-graph matcher benchmark (sub-ms up to 200 nodes)
- `0.14.json`: Parallel corpus seed (5 propositions, English + Turkish)

### Changed
- `0.5.py`: Refactored from 560 to 150 lines using `nst_core` imports

## [Sprint 4 — 2026-05-22] Evidence to Impact

### Added
- `0.12.html`: Interactive NST visualization tool (11 trees, 5 languages)
- `0.12.md`: Cross-linguistic corpus specification

### Changed
- `0.7.md`: Updated to v1.0 final. Added evaluation results, corpus stats. Language Gate: PASSED.

## [Sprint 3 — 2026-05-22] Evidence

### Added
- `0.10.py`: Turkish morphological pipeline (Zemberek simulation → NST → search)
- `0.10.md`: Evaluation framework specification (precision@k, recall@k, MRR)
- `0.11.py`: Expanded 25-document corpus across 5 languages with scalability benchmarks

## [Sprint 2 — 2026-05-22] From Prototype to Production

### Added
- `0.8.py`: Type III tree edit distance matching (Zhang-Shasha algorithm)
- `0.8.md`: Morphological analyzer survey (English through Mohawk)
- `0.9.py`: Enhanced 12-document corpus across 5 languages

### Changed
- `0.2.py`: Added Turkish tree to formal verification suite
- `0.7.md`: Major revision — added YAML frontmatter, author block, abstract, reader testing appendix

## [Sprint 1 — 2026-05-22] Formalization

### Added
- `0.1.md`: Internal Literature Review (35+ projects, 12 papers, 6 repos)
- `0.2.md` + `0.2.py`: Formal Definitions + Python Verification Suite
- `0.3.md`: Sub-Graph Matching Search Specification
- `0.4.md`: Cross-Linguistic Examples (English, Turkish, Mohawk)
- `0.5.py`: Full Pipeline Prototype
- `0.6.md`: Computational Pathway Architecture
- `0.7.md`: Initial Synthesis Draft

## [2026-05-22] — Project Initialization

### Added
- Project directory and git repository (`feature/initial-setup`)
- All 7 mandatory documentation files
- Four-round due diligence across releases, archive, notes, and GitHub

---
*Last updated: 2026-05-22 (Project complete)*
