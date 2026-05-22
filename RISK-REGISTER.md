# Risk Register — Nested Semantic Graph

**Last Updated:** 2026-05-22

| Risk ID | Description | Probability | Impact | Status | Mitigation | Last Reviewed |
|:--------|:------------|:-----------|:-------|:-------|:-----------|:--------------|
| R1 | Gap between ultrametric physics formalism and linguistics application | Low | Medium | **Mitigated** — Due diligence found complete 2026-05 publication corpus bridging both domains (Few Become One, Language-Info-Architecture, Tree Cophenetic, etc.) | N/A — risk retired | 2026-05-22 |
| R2 | No external linguistics/AI literature imported — search request manifest needed | Low | Medium | **Mitigated** — Language-Info-Architecture, Few Become One, Q-PNA, and Verb Lexicon all published with DOIs providing linguistic grounding | N/A — risk retired | 2026-05-22 |
| R3 | PILE OF BABEL connection must be explicit to avoid appearing derivative | Low | Medium | **Mitigated** — ADR-0003 adopted, explicit connection made in 0.1.md §9.1, 0.4.md, and README.md | N/A — risk retired | 2026-05-22 |
| R4 | Project must correctly position as computational sequel, not novel conceptual work | Low | High | **Active** — Positioned in README, 0.1.md §12 (Gap Analysis), ADR-0004. Ongoing: the search architecture spec (0.3.md) must clearly articulate its contribution relative to Few Become One §V | Review each deliverable against ADR-0004 | 2026-05-22 |
| R5 | Scope creep — original sprint tasks have been reordered and deliverables have exceeded initial estimates | Medium | Low | **Monitoring** — S2 (lit grounding) was absorbed by 0.1.md; S4 (sub-graph) became 0.3.md; S3 (linguistic) became 0.4.md. The reordering is natural given the discovered prior work. S5 (prototype) and S6 (pathway) are the remaining major tasks. | Triage remaining scope; consider separate sprint for reader testing | 2026-05-22 |
| R6 | Python prototype may require dependencies beyond standard library | Medium | Medium | **Active** — Subgraph isomorphism and tree edit distance algorithms may need numpy/scipy for efficiency. The ultrametric-ai-poc uses streamlit. | Use standard library for prototype; document external dependencies if needed | 2026-05-22 |
| R7 | Single-author limitation — blind reader testing requires external perspective | Medium | Medium | **Active** — S7 (Reader Testing) uses REVIEWER subagent for blind validation. The REVIEWER cannot verify factual accuracy against source files. | Mitigated by §11.5 protocol: 2-round minimum, severity classification. REVIEWER provides structural/readability feedback; parent verifies facts. | 2026-05-22 |

---
*Generated from RISK-REGISTER-TEMPLATE.md v1.0. Last updated: 2026-05-22.*
