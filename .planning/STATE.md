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
