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

## 2026-05-23 01:35 — Double code review + fixes applied

- CI lint failed on prettier (jsonc key ordering) — fixed in commit `09a56116` by sort_keys=True in lang files.
- Two independent code reviews ran (`.planning/reviews/review-1-structure-correctness.md`, `review-2-content-ux.md`) — both REQUEST_CHANGES with surgical findings.
- All P0 / P1 fixes applied in commit on top:
  - Generator now uses a frozen `.planning/codebase/quest_id_registry.json` so quest IDs stay stable across content edits (P0 + P1 from review #1).
  - FAQ ID generation switched from non-deterministic `abs(hash())` to md5-derived + registry-pinned.
  - Icons: `modular_golems:golem_core` → `modulargolems:metal_golem_body`, both `gateways:titan_pearl`/`challenge_pearl` → `gateways:gate_pearl` (P1 from review #2).
  - Wiki: Make Lava heat source rewritten to ForceCraft (P1 review #2), "Gear Smithing Table" naming fix, "Sappling"→"Sapling", 25 × `Sovет:`→`Совет:`, `Bulыжник`→`Булыжник`, §-balance fixed on 4 RU descs, `§aNext:` lines added to sample quests.
  - CI: `if-no-files-found: warn`→`error`, dev fallback removed in build.yml, `release.yml` dynamic prerelease for `-rc`/`-beta` tags, validate.yml `push:` trigger pruned to develop only, `softprops/action-gh-release` SHA-pinned to v2.0.6.
  - scripts/release/index.ts: case-insensitive `SF5_CI_SKIP_FORGE_DOWNLOAD`, dropped redundant `readMinecraftPackage()`.
  - REQUIREMENTS.md: R-012 corrected to reflect actual behaviour, R-021/R-022/R-023 added as v2 work.
  - Generator now preserves existing lang values via `dict.setdefault()` — re-runs no longer clobber hand-curated wiki.
- Local lint passes (exit 0) — all 5 commits are now lint-clean.
- Next: push fixes, wait for CI to go green, mark ready-for-review, merge.
