# State log

## 2026-05-22 22:40 — bootstrap

- Branch: `feat/ftb-quests-migration` cut from `develop` @ `aae4432`
- Parsed `src/minecraft/config/checklist/tasks.txt` → 178 quests across 20 ages
- Decisions:
  - Quest mod: **FTB Quests Forge 1.20.1** (closest match to reference screenshot, mature, SNBT format)
  - Keep `Checklist` mod parallel — coexists
  - Languages: EN (primary) + RU
  - Scope: full ~200 quests; v1 ships skeleton + Getting Started full wiki + CI/CD, v2 = per-age PRs
- Open questions: none
- Next: phase 01 — mod manifest + FTB Quests config skeleton + i18n scaffolding

## 2026-05-23 00:55 — v1 PR ready for review

- Branch `feat/ftb-quests-migration` pushed; **draft PR #1**.
- Commits:
  - `b192ee98` bootstrap planning directory
  - `8a6b084a` skeleton (11 chapters, 178 quest stubs, 377 i18n keys EN+RU)
  - `9029bbf2` CI/CD (validate.yml + build.yml + release.yml + scripts/release/index.ts CI patch)
  - `b3fc5134` Getting Started full wiki (26 quests) + README + CLAUDE.md
- R-001..R-014, R-030..R-031, R-040..R-045, R-050..R-051 covered. R-020 (full wiki for remaining 17 ages) deferred to follow-up PRs per ROADMAP.md.
- Open questions: none.
- Next: monitor CI runs on PR #1, address any lint failures, then mark ready-for-review.
