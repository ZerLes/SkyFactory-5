# CI Lint Trace — `Lint + format check`

## Top-line diagnosis

**jest fails on `json-schema-validator/no-invalid` in `example_style.json`**: the file uses two properties (`frame` at root level, `tag` inside `filter`) that are not defined in `schemas/minecraft/obscure_tooltips/style.json`, which uses `additionalProperties: false`.

---

## Environment

| Item | Value |
|------|-------|
| Node | v20.20.1 (CI uses 20.5.1) |
| npm  | 10.8.2 |
| prettier | 3.0.2 (from node_modules) |
| Branch | `feat/ftb-quests-migration` @ `6fc6922d` |
| Repo | `/home/user/workspace/sf5` |

---

## Reproduction Steps

```bash
cd /home/user/workspace/sf5

# 1. Clean install
rm -rf node_modules
npm ci --no-audit --no-fund --prefer-offline
# → husky installs hooks, 933 packages installed in ~2 min

# 2. Verify binaries (both present and executable)
ls -la node_modules/.bin/prettier  # → symlink to ../prettier/bin/prettier.cjs
node_modules/.bin/prettier --version  # → 3.0.2

# 3. Run full lint check
npm run lint:direct 2>&1; echo "EXIT=$?"
```

---

## Full Output of `npm run lint:direct`

```
> skyfactory-5@5.0.0 lint:direct
> npm run format:validate:direct && jest --config jest-eslint.config.js

> skyfactory-5@5.0.0 format:validate:direct
> prettier --ignore-unknown --check --log-level=warn "**/*.@(cjs|js|json|json5|jsonc|jsx|mcmeta|mjs|properties|toml|ts|tsx)"

[prettier exits 0 — no output, all files pass]

/home/user/workspace/sf5/src/minecraft/global_packs/required_resources/sf5_resources/assets/obscure_tooltips/tooltips/styles/example_style.json
   4:3  error  Unexpected property "frame"       json-schema-validator/no-invalid
  11:5  error  Unexpected property "filter.tag"  json-schema-validator/no-invalid

✖ 2 problems (2 errors, 0 warnings)

EXIT=1
```

> **Note:** On the very first run after a fresh `npm ci`, AJV emits a one-time stderr warning:
> `exclusiveMinimum is not boolean` — this is a benign AJV draft-07 schema compatibility
> warning during initial schema compilation. It does **not** appear on subsequent runs and
> is not the cause of the failure.

---

## Step-by-step breakdown

### Step 1 — `npm run format:validate:direct` (PASSES)

Prettier 3.0.2 with plugins `prettier-plugin-properties` and `prettier-plugin-toml`
(from `.prettierrc.cjs`) checks all matching files. **Exit code 0. No files need reformatting.**

### Step 2 — `jest --config jest-eslint.config.js` (FAILS)

Uses `jest-runner-eslint` to run ESLint across all matched files in `src/`, `scripts/`,
`schemas/`, and root-level files.

**Failing file:**
```
src/minecraft/global_packs/required_resources/sf5_resources/assets/obscure_tooltips/tooltips/styles/example_style.json
```

**Errors (rule: `json-schema-validator/no-invalid`):**

| Line | Property | Reason |
|------|----------|--------|
| 4:3  | `frame`      | Not in `schemas/minecraft/obscure_tooltips/style.json` — schema has `additionalProperties: false` at root |
| 11:5 | `filter.tag` | Schema defines `filter.tags` (plural) with `additionalProperties: false`; file uses `filter.tag` (singular) |

---

## Root Cause Analysis

**Schema file:** `schemas/minecraft/obscure_tooltips/style.json`

The schema defines:
```json
{
  "additionalProperties": false,
  "properties": {
    "priority": ...,
    "panel": ...,
    "icon": ...,
    "effects": ...,
    "filter": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "items": ...,
        "enchantments": ...,
        "tags": { "type": "object" }   ← plural "tags"
      }
    }
  }
}
```

**Failing file:** `example_style.json` contains:
```json
{
  "priority": 1000,
  "panel": "obscure_tooltips:golden",
  "frame": "obscure_tooltips:bones",   ← NOT in schema (line 4)
  "icon": "obscure_tooltips:epic",
  "effects": [...],
  "filter": {
    "enchantments": { ... },
    "tag": { ... }                     ← should be "tags" plural (line 11)
  }
}
```

**Two issues in `example_style.json`:**
1. `frame` property at root — not listed in schema's `properties`, violates `additionalProperties: false`
2. `filter.tag` — schema defines `filter.tags` (plural); the file uses `tag` (singular), which violates `filter.additionalProperties: false`

---

## Fix Options

Either fix the source file OR update the schema:

**Option A — Fix `example_style.json`** (source file needs to match schema):
- Remove or rename `frame` → not in schema (need to add it to schema if it's a valid field)
- Rename `filter.tag` → `filter.tags`

**Option B — Fix `schemas/minecraft/obscure_tooltips/style.json`** (schema needs to match file):
- Add `"frame": { "type": "string" }` to schema `properties`
- Rename `"tags"` → `"tag"` in `filter.properties` (or add both)

Given that `example_style.json` is likely intentional sample content for a new feature
(on branch `feat/ftb-quests-migration`), **Option B is more likely correct**: the schema
needs to be updated to include the `frame` property and to use `tag` (singular) instead
of `tags` (or add both variants).

---

## What is NOT broken

- `node_modules/.bin/prettier` is present, symlinked, and executable after `npm ci`
- PATH propagation to `npm run` works correctly — this was **not** an issue in this environment
- Prettier passes on all files (format check exit 0)
- husky `prepare` hook completes successfully
- All other ESLint rules pass across the entire `src/`, `scripts/`, and `schemas/` trees
