# Changelog — Nested Semantic Graph

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- **0.12.md: Cross-Linguistic Corpus Specification** — Sprint 4.2 deliverable. Format template (§4), parallel text resource research (UD, Parallel Bible, WALS, ODIN, Tatoeba — §5), 3-phase expansion plan to 27 documents (§6), verification protocol (§7), UD-to-NST mapping strategy.
- **0.11.html: NST Visualization Tool** — Sprint 4.1 deliverable. Interactive HTML/JS viewer: expand/collapse subtrees, two-node LCA selection with highlighting, ultrametric distance display. Embedded 12-tree, 5-language corpus. SVG tree layout, node color coding by category, language badges.
- **0.11.md: Visualization Tool Docs** — Documentation for 0.11.html: features, architecture, verification.
- **0.10.py: Turkish Morphological Pipeline** — Sprint 3.1 deliverable. Zemberek simulator, NST builder from morphological parses, subtree search, precision/recall/MRR evaluation. 15-document Turkish corpus, 10 queries, 15/15 ultrametric verification passed.
- **0.10.md: Pipeline Results** — Full analysis: Mean P@5=0.180, R@5=0.375, F1@5=0.230, MRR=0.382. Honest finding: Type I matching too rigid for morphological variation — motivates Type II/III integration.
- **0.2.md: Formal Definitions** — 11 formal mathematical definitions, 2 theorems (Ultrametric Inequality, Language Neutrality), connections to Tree Cophenetic and Q-PNA §2-3.
- **0.2.py: Python Verification Suite** — NestedSemanticTree class, binary-lifting LCA (O(log n)), exhaustive ultrametric verification across 3 trees (22/22 passed).
- **0.3.md: Sub-Graph Matching Search Spec** — Formal specification: search problem definition, three-tier matching criteria (Type I exact subtree isomorphism, Type II partial match, Type III tree edit distance), RANK-AND-CLUSTER algorithm with ultrametric cluster detection, full pipeline connecting Q-PNA encoder to NSG matcher, complexity analysis, worked walkthrough, and 8 limitations.
- **0.4.md: Cross-Linguistic Examples** — Same proposition in English (isolating), Turkish (agglutinative), Mohawk (polysynthetic). All three produce isomorphic NSTs. Linearization algebra formalized (order, chunking, morpheme realization, function word insertion). Connected to Language-Info-Architecture entropy gradient and compression-tax trade-off.

## [2026-05-22] — Initialization & Due Diligence

### Added
- **0.1.md: Internal Literature Review** — Comprehensive four-pass due diligence report (53,983 bytes, 583 lines). Documents the complete ultrametric-language-AI research program: 35+ archived projects, 12 published papers (11 DOIs), 6 GitHub repositories, 3 archival 2025 projects.

---
*Last updated: 2026-05-22*
