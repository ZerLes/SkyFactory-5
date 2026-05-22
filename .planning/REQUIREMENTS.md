# Requirements

Each ID is referenced from PLAN.md `<requirements>` blocks. `v1` = this PR/migration; `v2` = follow-up PRs (one per remaining age).

## FTB Quests integration

- **R-001** (v1): FTB Quests Forge mod listed as a runtime dependency in a tracked file (`.modlist.json` or equivalent) with version pinned to a 1.20.1 release.
- **R-002** (v1): FTB Library and FTB Teams (FTB Quests deps) similarly listed.
- **R-003** (v1): FTB Quests config files committed under `src/minecraft/config/ftbquests/` with team-mode "single" and consume-items disabled by default (book-friendly).
- **R-004** (v1): `Checklist` mod and `config/checklist/tasks.txt` left intact.

## Quest content (skeleton — v1)

- **R-010** (v1): 11 FTB Quests chapter files (one per category) committed: Getting Started, Tech Basics, Resources, Storage, Power, Advanced Tech, Magic, Exploration, Miscellaneous, Endgame, FAQ.
- **R-011** (v1): Chapter order on the sidebar matches the reference screenshot.
- **R-012** (v1): All 178 quests from `tasks.txt` materialised as SNBT quest entries with dependency links reflecting progression (intra-age serial, inter-age via "gate" quests).
- **R-013** (v1): Each quest has an icon (mod-provided item id) and at least a 1-sentence description.
- **R-014** (v1): First three ages (Discovery, Stone, Chromatic — 26 quests) ship with **full mini-wiki**: per-quest description containing step-by-step instructions, item references, and a "what unlocks next" closing line referencing the next quest's title.

## Quest content (full wiki — v2)

- **R-020** (v2): The remaining 17 ages get full mini-wikis, shipped one PR per logical group (Tech/Resources/Storage in one PR, Power+Advanced Tech in another, Magic in its own PR because it has 54 quests with 4 sub-trees, etc.).

## Localization

- **R-030** (v1): All quest titles, descriptions, and chapter names use translation keys (no hardcoded English in SNBT).
- **R-031** (v1): `en_us.json` and `ru_ru.json` lang files committed under `src/minecraft/kubejs/assets/ftbquests/lang/` (KubeJS asset pipeline) covering at minimum the v1 skeleton scope.
- **R-032** (v2): RU translations expanded as new ages ship.

## CI/CD

- **R-040** (v1): `.github/workflows/build.yml` runs on push to any branch and on PRs. It runs lint and produces both client and server release zips as workflow artifacts named `SkyFactory-5-client-v{version}-{short-sha}.zip` / `SkyFactory-5-Server-v{version}-{short-sha}.zip`.
- **R-041** (v1): `.github/workflows/release.yml` runs on tags `v*` and on manual dispatch. Creates a GitHub Release with both zips attached. Zip names match the `npm run release` (production) output exactly so they're drop-in usable for CurseForge upload.
- **R-042** (v1): `version` is read from `mc-package.json` — never hand-typed in the workflow.
- **R-043** (v1): Workflow uses Node 20.5.1 (matches `.nvmrc`).
- **R-044** (v1): A `validate.yml` check runs the existing lint pipeline (`npm run lint`) on every PR and gates merge.
- **R-045** (v1): Release workflow tag pattern enforces semver-ish `v{major}.{minor}.{patch}`. Auto-bumping not in scope; tagging is manual.

## Documentation

- **R-050** (v1): `README.md` updated with a section explaining the new quest book, where translations live, and how to run a local release build.
- **R-051** (v1): `CLAUDE.md` at repo root documenting the FTB Quests file layout for future AI agents.
