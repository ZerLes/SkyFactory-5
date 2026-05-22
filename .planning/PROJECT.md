# SF5 Quest Book → FTB Quests Migration

## Pitch

Replace the legacy `Checklist`-mod book-style quest list (`config/checklist/tasks.txt`) with a tree-based FTB Quests UI matching the modern modpack standard (categories on the left, dependency graph on the right, per-quest icons and detailed wiki-style descriptions with step-by-step guides). `Checklist` stays installed in parallel as a lightweight progress checkbox; FTB Quests is the primary progression UI.

Adds:
- FTB Quests + dependency mods to the pack
- ~178 quests split across 11 categories (Getting Started → Endgame + FAQ), preserving the ages from `tasks.txt`
- EN + RU localization (`en_us.json` + `ru_ru.json`)
- Per-quest "mini-wiki" — quest descriptions that double as a step-by-step guide referencing the previous quest's progress
- GitHub Actions CI/CD that builds CurseForge-compatible client + server zip artifacts on every push and produces a versioned release on tag

## Hard constraints

- Minecraft 1.20.1, Forge 47.4.0, FTB Quests Forge 1.20.1-2007.x
- Default branch: `develop`; PRs must be **draft** (user's `#prnew` default)
- Keep `Checklist` mod and its `config/checklist/` files intact
- All new file paths under `src/minecraft/...` (this is what the DarkPacks release pipeline zips)
- CI runs `npm run release` in production mode; release zips must be named exactly as `scripts/release/index.ts` names them (`SkyFactory 5 v{version}.zip`, `SkyFactory 5 Server v{version}.zip`)
- Versioning comes from `mc-package.json`'s `version` field — never hand-edit in CI
- DO NOT commit jar mods to git; FTB Quests + deps are listed in a manifest file for documentation, actual jars must come from CurseForge (consistent with current repo policy)

## Out of scope (v2)

- Auto-publishing to CurseForge via their API (only the artifact build; manual upload from GitHub releases page)
- Migrating Checklist progress to FTB Quests progress
- Quest icons beyond what's already available in `sf5_icons` or mod-provided items
- Voice-over / sound effects per quest
