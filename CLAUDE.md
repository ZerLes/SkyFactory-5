# Repo conventions for AI agents

> Working notes for Claude / Computer / Codex agents. Humans should read `README.md` first.

## Repository layout

```
src/minecraft/                # Files that ship inside the modpack zip (resourcepacks, configs, scripts, datapacks)
  config/                     # mod configs, one folder/file per mod
    checklist/                # Legacy book-style task list (Checklist mod). Kept in parallel with FTB Quests.
    ftbquests/                # Primary quest book — tree UI with chapters, mini-wiki descriptions
      quests/
        data.snbt             # Root quest-book config (team-mode single, no item consumption)
        chapter_groups.snbt   # Flat — no chapter groups
        chapters/             # One .snbt file per chapter (Getting Started, Tech Basics, ..., FAQ)
  kubejs/assets/ftbquests/lang/
    en_us.json                # English (primary)
    ru_ru.json                # Russian
  global_packs/               # Built-in data + resource packs
  thingpacks/                 # ThingPacks (data-driven content)
  packmenu/                   # PackMenu customization

scripts/
  release/                    # Build pipeline (called by `npm run release`)
    index.ts                  # Patched to honour SF5_CI_SKIP_FORGE_DOWNLOAD for CI

.github/workflows/
  validate.yml                # PR gate: lint + i18n keyset parity check
  build.yml                   # Every push: produces client + server zips as artifacts
  release.yml                 # On `v*.*.*` tag: GitHub Release with both zips attached

.planning/                    # GSD-flow planning artifacts. Treat as read/write for new agent sessions.
  PROJECT.md
  REQUIREMENTS.md             # R-IDs you should cite in commit messages / PR descriptions
  ROADMAP.md
  STATE.md                    # Append after every phase boundary
  codebase/
    quests_inventory.json     # 178 quests parsed from checklist/tasks.txt — source of truth
    age_to_chapter.json       # Mapping: each Age (from tasks.txt) → FTB Quests chapter + section + grid offset
    chapters.json             # Chapter metadata (id, title, icon, sidebar order)
    generate_ftbquests.py     # Regenerates all chapter SNBTs from the JSONs above
    parse_tasks.py            # Re-parses checklist/tasks.txt into quests_inventory.json
  phases/<NN-slug>/PLAN.md    # Per-phase atomic plans (see .planning/phases/01-foundation/PLAN.md)
```

## Quest editing workflow

To add a quest or fix one:

1. Edit `.planning/codebase/quests_inventory.json` (source of truth) and/or `.planning/codebase/age_to_chapter.json`.
2. Re-run `python3 .planning/codebase/generate_ftbquests.py`.
3. Add/update the corresponding entry in `en_us.json` and `ru_ru.json`. **Both languages must have the same keyset** — the validate workflow enforces this.
4. Quest IDs are deterministic: `md5(f"{age}:{index_in_age}:{title}").hexdigest()[:16].upper()`. Translation keys use the lowercase form. Don't invent IDs by hand.

To add a new chapter:

1. Add an entry to `.planning/codebase/chapters.json`.
2. Update `.planning/codebase/age_to_chapter.json` to route at least one age to it (or add a synthetic placeholder age).
3. Re-run the generator.
4. Add `ftbquests.chapter.<id>.title` keys to both lang files.

## Conventions

- **Branch naming**: `feat/<topic>`, `fix/<topic>`, `chore/<topic>`. PRs default to **draft**.
- **Commit prefix**: use Conventional Commits — `feat(quests):`, `ci:`, `docs:`, `chore(planning):`, `fix(release):`.
- **PR descriptions**: cite the R-IDs from `.planning/REQUIREMENTS.md` that the PR satisfies.
- **No manual zip uploads**: ship via GitHub Releases (tag `v{semver}` matching `mc-package.json` version → `release.yml` does the rest).
- **No jars in git**: mods live on CurseForge. The `.modlist.json` tracks which mods + recommended versions ship with the pack.
- **The Checklist mod stays**: it's the lightweight fallback quest UI. Don't remove it — that's a deliberate parallel-system decision.

## CI environment variables

- `SF5_CI_SKIP_FORGE_DOWNLOAD=true` — set in `build.yml` and `release.yml`. Makes `scripts/release/index.ts` skip the Mojang-authenticated Forge installer download (which can't run in CI) and embed a `SERVER_README.txt` with the Maven URL instead.
- `CI=true` — implicit on GitHub Actions, can be tested in scripts.

## Local dev quick-reference

```bash
nvm use                            # picks up Node from .nvmrc
npm install
npm run lint:direct                # same lint that CI runs
npm run release:dev                # builds zips with a date+random suffix into .releases/
npm run release                    # prod-named zips
NODE_ENV=production SF5_CI_SKIP_FORGE_DOWNLOAD=true npm run release   # simulate what CI does
```

## When you're stuck

1. Read `.planning/PROJECT.md` for the high-level pitch.
2. Read the latest entry in `.planning/STATE.md` to see where the last session left off.
3. Find the phase you're working on in `.planning/phases/` — its `PLAN.md` describes the contract.
4. If you're a fresh subagent, the orchestrator should have already pointed you at a specific PLAN.md. Stick to its `<files>` list.
