# CONTRIBUTING — Nested Semantic Graph

**Project:** Nested Semantic Graph
**Last Updated:** 2026-05-22

## How to Contribute

This project follows the **Projects Agent** workflow (§0.9 of the system prompt). The agent is the primary executor. Human contributions come through:

1. **Project direction** — Setting sprint goals, prioritizing backlog items, providing domain expertise
2. **Code review** — Reviewing Python prototypes before they become published
3. **Publication decisions** — Approving moves to `Obsidian\releases\`
4. **External resources** — Supplying DOIs, GitHub repos, archived project references

## Agent Workflow

All agent work follows the Phase 0-5 pipeline (§5 of the system prompt):

1. **Phase 0:** Git pre-flight (branch check, worktree cleanliness)
2. **Phase 1:** Task framing (goal, output form, constraints)
3. **Phase 2:** Approach selection (brainstorming, research, writing, analysis, engineering)
4. **Phase 3:** Iterative execution (produce → check → refine)
5. **Phase 4:** Synthesis & delivery
6. **Phase 5:** Execution audit & close-out

## File Naming

- **Content files:** `MAJOR.MINOR[.PATCH].ext` (§10)
- **Project management files:** Fixed descriptive names (§0.7, Rule 0)
- **Publication files:** Descriptive filenames (§11.1)

## Git Discipline

- **NEVER** commit to `main` — all work on `feature/<name>` branches
- **ALWAYS** use `-C` flag: `git -C "G:\My Drive\projects\nested-semantic-graph\" <command>`
- **Post-work checklist** (§9.3): stage → verify staging → commit → verify commit → verify branch
- **Commit message format:** `ACTION:[CREATE|EDIT|DELETE] FILE: <path> RATIONALE:<reason>`

## Code Standards

- Python standard library only (unless documented)
- Self-contained scripts, re-executable
- All quantitative output from code execution, never LLM inference
- Unicode safety scan before execution (§0.5, Rule 4)

## Publication Standards

- All publication documents must pass the Publication Language Gate (§11.7)
- Reader testing required before declaring "publication-ready" (§11.5)
- User approval required before any move to `Obsidian\releases\`

## Cross-Project Learning

- Read `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md` at session start
- Add project-specific lessons to `LEARNINGS.md`
- Lessons marked "Cross-Project: YES" are candidates for CPL promotion

---
*Generated from CONTRIBUTING-TEMPLATE.md v1.0.*
