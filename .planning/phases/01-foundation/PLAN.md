# Phase 01-05 (combined v1 plan) — FTB Quests migration + CI/CD

This is the executor plan for the v1 scope of PR #1 on ZerLes/SkyFactory-5.

## Goal

Ship a draft-PR-ready commit set that:
1. Adds FTB Quests + deps to the mod manifest
2. Creates the FTB Quests config + 11 chapter files with 178 stubbed quests
3. Ships full mini-wiki descriptions for the 26 Getting-Started quests (Discovery + Stone + Chromatic), EN + RU
4. Adds CI/CD GitHub Actions workflows (build, validate, release)
5. Updates README and adds CLAUDE.md

## Requirements covered

R-001 .. R-051 (all v1). See `.planning/REQUIREMENTS.md`.

## Files to create / modify

### Mod manifest
- `.planning/codebase/added_mods.md` (informational, lists FTB Quests + FTB Library + FTB Teams CurseForge project IDs and recommended file versions for 1.20.1-Forge)
- `src/minecraft/config/ftbquests/quests/data.snbt` (root quest file, team-mode single)
- `src/minecraft/config/ftbquests/ftbquests-client.snbt` (client config — book UI prefs)
- `src/minecraft/config/ftbquests/quests/chapter_groups.snbt` (no groups — flat list)
- `src/minecraft/config/ftbquests/quests/chapters/{getting_started,tech_basics,resources,storage,power,advanced_tech,magic,exploration,miscellaneous,endgame,faq}.snbt` (11 files)

### Quests (one folder per chapter, each quest is one .snbt file)
- Read `.planning/codebase/quests_inventory.json`
- For each quest, generate a unique 16-char hex id (deterministic — `hashlib.md5(f"{age}:{index}:{title}").hexdigest()[:16]`)
- Within a chapter, the i-th quest depends on the (i-1)-th quest unless it's the first of a sub-category
- The first quest of each chapter (except Getting Started) depends on the last quest of the previous chapter's "gate quest" — pick one logical gate per chapter
- Position quests in a downward-flowing grid: `x = chapter_index * 0`, `y = quest_index * 1.5`, sub-categories shifted on x

### i18n
- `src/minecraft/kubejs/assets/ftbquests/lang/en_us.json`
- `src/minecraft/kubejs/assets/ftbquests/lang/ru_ru.json`
- Translation keys: `ftbquests.chapter.{slug}`, `ftbquests.quest.{slug}.title`, `ftbquests.quest.{slug}.desc`
- All 178 quests get an EN title; first 26 (Getting Started) get full EN desc + RU title + RU desc; rest get a short placeholder desc in both langs.

### Wiki content (Getting Started — 26 quests)
For each of Discovery (16), Stone Age (4), Chromatic Age (6), write a 4-8 line markdown-style description containing:
- **What to do** — concrete action, item names with `<item>` tags where supported by FTB Quests
- **How** — recipe hint or world-interaction sequence
- **Why** — what this unlocks (referencing the next quest's title)
- **Tips** — pitfalls or shortcuts

Source material:
- `tasks.txt` line for each quest
- Mod documentation links allowed in descriptions: Ex Nihilo Sequentia, Silent Gear, Crafting Stick, Eccentric Tome
- For colors specifically: each "Discover <Color>" links to a specific recipe/event in SF5 — the user is colorblind in-game until they discover that color

### CI/CD

`.github/workflows/build.yml`
- Triggers: `push: [develop, feat/**]`, `pull_request: [develop]`
- Job 1 `lint`: Node 20.5.1, `npm ci`, `npm run lint:direct`
- Job 2 `build` (needs lint): runs `cross-env NODE_ENV=production ts-node ./scripts/release/index.ts` minus the forge-download step (Minecraft can't auth in CI). Outputs `.releases/SkyFactory 5 v{version}.zip` etc. Uploads both as workflow artifacts named `SkyFactory-5-client-v{version}-{short-sha}.zip` and `SkyFactory-5-Server-v{version}-{short-sha}.zip`.

`.github/workflows/validate.yml`
- Trigger: `pull_request`
- Runs `npm run lint` and fails the PR check on any error.

`.github/workflows/release.yml`
- Triggers: `push: tags: ['v*']`, `workflow_dispatch`
- Builds prod zips, creates GitHub Release with both attached
- Release notes auto-generated from git log since previous tag
- Tag must be `v{semver}` and must match `mc-package.json` version (validation step)

**Important** — `scripts/release/index.ts` currently calls `ForgeManager.ensureDownloaded()` which tries to fetch the Forge installer and requires Minecraft account auth via msmc. CI cannot interact. Add a guard: if `process.env.CI === 'true'`, the release script must skip the Forge installer download for the **client** zip (the client doesn't need it bundled — the launcher fetches it) and for the **server** zip, embed only the Forge installer URL into a `SERVER_README.txt` so admins fetch it themselves. Implement this as a minimal patch to `scripts/release/index.ts`.

### Docs
- `README.md`: add a "## Quest Book (FTB Quests)" section between "## Development" and "## Release" with:
  - Where quests live (`src/minecraft/config/ftbquests/quests/chapters/`)
  - i18n keys & how to add a new language
  - How to test locally (`npm run start`, open the book in-game)
- `CLAUDE.md` at repo root, documenting:
  - The FTB Quests file layout
  - The naming convention for quest IDs and translation keys
  - The CI/CD pipeline overview
  - The Checklist mod parallel relationship

## Verification

After implementation, run inside the repo root:

```bash
# 1. Lint must pass
npm install
npm run lint:direct
# Expected: exits 0

# 2. JSON files must be valid
python3 -c "import json; [json.load(open(p)) for p in ['src/minecraft/kubejs/assets/ftbquests/lang/en_us.json','src/minecraft/kubejs/assets/ftbquests/lang/ru_ru.json']]"
# Expected: exits 0

# 3. All 178 quests present
python3 - <<'PY'
import os, glob
files = glob.glob("src/minecraft/config/ftbquests/quests/chapters/*/*.snbt")
print(f"quest files: {len(files)}")
assert len(files) == 178, f"expected 178, got {len(files)}"
PY

# 4. GitHub Actions YAML syntactically valid
python3 -c "import yaml; [yaml.safe_load(open(p)) for p in ['.github/workflows/build.yml','.github/workflows/validate.yml','.github/workflows/release.yml']]"
```

## Commit strategy

Make 5 atomic commits on `feat/ftb-quests-migration` (already exists):

1. `feat(quests): add FTB Quests config skeleton + mod manifest`
2. `feat(quests): generate 178 quest stubs across 11 chapters with dependencies`
3. `feat(quests): write step-by-step wiki for Getting Started (26 quests, EN + RU)`
4. `ci: add build/validate/release GitHub Actions workflows`
5. `docs: README + CLAUDE.md for FTB Quests layout and CI pipeline`

After all 5 commits, push to `origin/feat/ftb-quests-migration`.

## Rollback

If any verification step fails: do not push. Reset hard to the last good commit (`b192ee98` — bootstrap). Write the failure into `.planning/phases/01-foundation/FAILURE.md`.
