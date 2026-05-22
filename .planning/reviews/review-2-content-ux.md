# Code Review #2 — Game Content, UX, FTB Quests Semantics

**Reviewer:** Subagent #2  
**Branch:** `feat/ftb-quests-migration`  
**Date:** 2025

---

## Top-line Verdict

**REQUEST_CHANGES**

Two icon IDs reference non-existent items (`gateways:titan_pearl`, `gateways:challenge_pearl`), one icon uses a wrong namespace (`modular_golems:golem_core` vs the pack's actual `modulargolems` namespace), the mini-wiki "Make Lava" quest contains a factual error about the heat source, one quest calls the Silent's Gear workbench by the wrong name, and a systematic Cyrillic/Latin mixed-script bug renders all 25 `§aSovет:` tip labels garbled in-game. None of these are individually blocking, but taken together they push this to REQUEST_CHANGES. The cross-chapter dependency gap is a deliberate design choice and can stay for v1 with a documented rationale; flagged as P2 below.

---

## Issue Table

| # | Sev | Area | Issue | Suggested Fix |
|---|-----|------|-------|---------------|
| 1 | P1 | Icons | `gateways:titan_pearl` is not a registered item in the Gateways to Eternity 1.20.1 mod. All gateway pearls use `gateways:gate_pearl` with NBT to distinguish tier. This will show a broken/missing item icon in the sidebar. Evidence: every loot table and ZenScript recipe in the pack uses `<item:gateways:gate_pearl>.withTag({gateway:…})`. | Replace `icon: "gateways:titan_pearl"` with `icon: "gateways:gate_pearl"`. |
| 2 | P1 | Icons | `gateways:challenge_pearl` — same issue as above. | Replace with `icon: "gateways:gate_pearl"`. |
| 3 | P1 | Icons | `modular_golems:golem_core` uses wrong namespace. The pack uses `modulargolems` (no underscore) — confirmed by `src/minecraft/scripts/item_durability.zs` (`modulargolems:iron_golem_spear` etc.). There is no `modular_golems` namespace anywhere in the codebase. | Replace with `icon: "modulargolems:golem_core"` (or an appropriate `modulargolems:` item; verify in-game if `golem_core` is the correct item name). |
| 4 | P1 | Wiki / RU | Systematic Cyrillic/Latin mixed-script bug: all 25 occurrences of `§aSovет:§r` in `ru_ru.json` contain Latin characters (`S`, `o`, `v`) mixed with Cyrillic (`е`, `т`). In-game this renders as mojibake or wrong glyph in some font renderers, and is clearly a copy-paste error. | Global replace `§aSovет:§r` → `§aСовет:§r` in `ru_ru.json`. |
| 5 | P1 | Wiki / RU | `ru_ru.json` quest `096d3b92e663cb71` desc: `§eBulыжник§r` — Latin `B`, `u`, `l` mixed with Cyrillic `ы`. Should be `§eБулыжник§r`. | Fix in `ru_ru.json`. |
| 6 | P1 | Wiki / EN | Quest `b81aea269d8e19e4` ("Make Lava in a Fired Crucible") states heat source is "a Blaze Burner or a lava block below it". In SF5, **all** standard Ex Nihilo heat sources (lava, fire, campfire, torch, etc.) are explicitly disabled via `"conditions": [{"type": "forge:false"}]` in every `exnihilosequentia/recipes/heat/*.json` file. A Create mod Blaze Burner provides lit fire, but `ens_fire.json` is also disabled. The actual SF5 heat source for the Fired Crucible is the `forcecraft:heat` item from the ForceCraft mod. The description will mislead early-game players. | Replace "Blaze Burner (Blaze Rod + Furnace) or a lava block below it" with a reference to the ForceCraft heat item. Cross-check with the ForceCraft in-game guide (Tier 1 → Heat) before finalising wording. |
| 7 | P2 | Wiki / EN | Quest `096d3b92e663cb71` ("Upgrade your Silent's Gear tools") calls the workbench "Gear Crafting Table". The actual registered item is `silentgear:gear_smithing_table` ("Gear Smithing Table"). This is confirmed by `src/minecraft/scripts/tags/colors/gray.zs` and `config/jei/blacklist.cfg`. | Change "Gear Crafting Table" → "Gear Smithing Table" in both EN and RU descriptions. |
| 8 | P2 | Wiki / EN | Quest `bce0485ccf92da1a` ("Use a Barrel to create Dirt") contains a spelling error: "§eSappling§r" (double-p). | Fix to "§eSapling§r" in `en_us.json` (and propagate to `ru_ru.json` if the Russian still has the sapling term). |
| 9 | P2 | Wiki — next-quest refs | R-014 requires "a 'what unlocks next' closing line referencing the next quest's title". Only 3 of 26 Getting Started quests include such a forward reference ("Craft a Silent's Gear Axe", "Right Click with an Axe on a Log", "Make Lava in a Fired Crucible"). The other 23 end with `§aResult:§r` bullet points that explain the current quest's outcome but do not name the next quest. | Add a `§aNext:§r` closing sentence to each quest that has a named successor. At minimum cover the sample five: Crafting Stick → Barrel, Make Lava → Obtain Obsidian, Dye Block → Flowers, Stone Material → (chapter end or next Chromatic quest). |
| 10 | P2 | Chapter-order consistency | `chapters.json` uses a 1-based `order` field (1–11); the SNBTs use `order_index` 0-based (0–10). These are internally consistent and the resulting sidebar order matches the reference screenshot exactly (Getting Started → FAQ). No fix required — but the off-by-one between the two documents is confusing for future maintainers. | Add a comment in `chapters.json` noting that `order` is 1-based planning metadata and `order_index` in SNBT is 0-based FTB Quests native. |
| 11 | P2 | Age→Chapter mapping | "Age of Farming" → `resources` chapter. Mystical Agriculture is closer to Tech than to generic Resources. The review prompt correctly identifies this tension. However, the chapter description "Resources" is broad enough to accommodate MA seeds. Only mildly misleading; no functional regression. | Optional: move "Age of Farming" to `tech_basics`, which already contains "Age of Automation". If the chapter is kept in Resources, add a note in `age_to_chapter.json`. |
| 12 | P2 | Cross-chapter dependencies | No chapter has a cross-chapter dependency on another. All 11 chapters are fully independent trees — the player can open "Endgame" on day 1. R-012 says "inter-age via 'gate' quests" but this is not implemented. | This is a valid v1 choice ("parallel chapters") but must be explicitly decided. Recommend either: (a) add a code comment in `data.snbt` or a ROADMAP note documenting that cross-chapter gating is intentionally deferred to v2, or (b) implement at minimum Getting Started → Tech Basics → (branch) gating. Either way, update R-012 to reflect the actual behavior. |
| 13 | P2 | Missing quests | The 16 "Discover {Color}" quests from `tasks.txt` (lines 34–49) are not migrated to FTB Quests. They exist only in the Checklist book. R-012 counts "178 quests" which excludes them, so this is arguably intentional — but the FAQ's "Discovering Colors" entry describes the mechanic without directing players to the Checklist for those 16 checkboxes. | Add one sentence to the "Discovering Colors" FAQ entry: "The 16 individual color-discovery checkboxes live in the §aChecklist§r book (the classic tab in your inventory), not in this quest book." |
| 14 | P2 | FAQ accuracy | "How to Use This Book": "Each chapter represents an age of progression" is inaccurate — several chapters contain multiple ages (e.g., Getting Started = Discovery + Stone + Chromatic; Exploration = Normal GW + Titan GW + Challenge GW + Travel + Worlds). | Reword to "Each chapter groups one or more ages of progression." |
| 15 | P2 | FAQ gap | "Mob Spawning Rules" correctly covers light levels and distance but omits the Spawner mechanic: "Spawners found in the world can be picked up (no Silk Touch needed) and retuned with a Trophy." This is described in `tasks.txt` but absent from the FAQ. | Add a third paragraph covering the Spawner → Trophy upgrade path. |
| 16 | P2 | SNBT semantics — future work | All 183 quests use `type: "checkmark"` (no item/advancement requirements). This is reasonable for v1 but means the quest book cannot auto-complete from gameplay events. REQUIREMENTS.md has no v2 requirement for mixed item/advancement tasks. | Add an explicit v2 requirement (e.g., R-021): "Key progression quests (first reactor build, first AE2 network, gateway completions) use `type: 'item'` or `type: 'advancement'` tasks for auto-tracking." |
| 17 | P3 | Icons | `thermal:energy_cell` and `thermal:dynamo_stirling` — both confirmed present in the pack via ZenScript tags. ✅ No issue. | — |
| 18 | P3 | Icons | `biggerreactors:reactor_casing` — confirmed present in `data/biggerreactors/recipes/crafting/cyanite_reprocessor.json`. ✅ | — |
| 19 | P3 | Icons | `mysticalagriculture:inferium_seeds` — confirmed in `recipes/thermal_recipes/insolator/inferium_seeds.json`. ✅ | — |
| 20 | P3 | Icons | `industrialforegoing:mob_duplicator` — confirmed in `src/minecraft/scripts/unification.zs`. ✅ | — |
| 21 | P3 | Icons | `rftoolsdim:dimension_builder` — confirmed in obscure_tooltips JSON. ✅ | — |
| 22 | P3 | Icons | `sophisticatedstorage:chest` — confirmed in `scripts/tags.zs` and `recipes/dark_oak_chest.json`. ✅ | — |
| 23 | P3 | Icons | `ae2:controller` — confirmed in tooltips JSON. ✅ | — |
| 24 | P3 | Icons | `ars_nouveau:source_gem` — confirmed in `advancements/color_stages/magenta_stage.json`. ✅ | — |
| 25 | P3 | Icons | `gateways:gate_pearl` (used in FAQ entry and exploration chapter) — confirmed in `treasurebags/loot_tables/bags/white.json` and all ZenScript gateway scripts. ✅ | — |

---

## Icon Suspect List (Summary)

| Icon ID | Verdict | Confidence | Suggested Replacement |
|---------|---------|------------|-----------------------|
| `gateways:titan_pearl` | ❌ Does not exist | **HIGH** | `gateways:gate_pearl` |
| `gateways:challenge_pearl` | ❌ Does not exist | **HIGH** | `gateways:gate_pearl` |
| `modular_golems:golem_core` | ❌ Wrong namespace | **HIGH** | `modulargolems:golem_core` (verify item name) |
| `biggerreactors:reactor_casing` | ✅ Valid | — | — |
| `mysticalagriculture:inferium_seeds` | ✅ Valid | — | — |
| `industrialforegoing:mob_duplicator` | ✅ Valid | — | — |
| `rftoolsdim:dimension_builder` | ✅ Valid | — | — |
| `sophisticatedstorage:chest` | ✅ Valid | — | — |
| `ae2:controller` | ✅ Valid | — | — |
| `thermal:dynamo_stirling` | ✅ Valid | — | — |
| `thermal:energy_cell` | ✅ Valid | — | — |
| `ars_nouveau:source_gem` | ✅ Valid | — | — |
| `gateways:gate_pearl` | ✅ Valid | — | — |

---

## Q5 — Mini-Wiki Sample Scoring

> Note: "Discover Black" is not present in the FTB Quests SNBT files at all — the 16 "Discover {Color}" entries from `tasks.txt` were intentionally excluded from the 178-quest migration scope (they remain in the Checklist book). Scoring is therefore for the 4 quests that are present.

| Quest | Actionability (1–5) | Accuracy (1–5) | Tone (1–5) | Color-code usage (1–5) | Next-quest ref |
|-------|---------------------|----------------|-----------|------------------------|----------------|
| Use the Crafting Stick to make a Colorless Crafting Table | 5 | 5 | 5 | 4 | No |
| Make Lava in a Fired Crucible | 5 | **2** ⚠ | 5 | 4 | Yes ("next quest!") |
| Use Color Dyed Water to convert Sand into a Dye Block | 5 | 5 | 5 | 4 | No |
| Upgrade Silent's Gear tools with a Stone Material | 4 | **3** ⚠ | 5 | 3† | No |
| **Discover Black** | N/A | N/A | N/A | N/A | **ABSENT** |

† Color-code score penalised: `§eBulыжник§r` (P1 typo in RU) and "Gear Crafting Table" wrong name (P2 EN accuracy hit).

### Factual issues per quest

**"Make Lava in a Fired Crucible" (accuracy: 2/5)**  
- EN desc says heat source is "a Blaze Burner (Blaze Rod + Furnace) or a lava block below it."  
- All standard Ex Nihilo heat sources (`ens_lava.json`, `ens_fire.json`, `ens_campfire.json`, etc.) are **disabled** in SF5 via `"type":"forge:false"` conditions. Neither a Create Blaze Burner nor a lava block will work as written.  
- RU desc repeats the same error: "Blaze Burner или блок лавы снизу."  
- The correct heat source is `forcecraft:heat` (ForceCraft Tier 1 item placed below the crucible).

**"Upgrade Silent's Gear tools with a Stone Material" (accuracy: 3/5)**  
- EN desc calls the workbench "Gear Crafting Table". The registered item is `silentgear:gear_smithing_table` ("Gear Smithing Table").  
- RU desc calls it "верстак Silent's Gear (§6Gear Crafting Table§r)" — same misnomer.  
- EN desc also mentions "Place your existing tool in the center slot" which may not match the actual Gear Smithing Table UI layout in 1.20.1 (it's a dedicated smithing-style interface). Low confidence — verify in-game.

---

## Q1 — Sidebar Order

chapters.json `order` field (1-based): Getting Started=1, Tech Basics=2, Resources=3, Storage=4, Power=5, Advanced Tech=6, Magic=7, Exploration=8, Miscellaneous=9, Endgame=10, FAQ=11.

SNBT `order_index` (0-based): getting_started=0, tech_basics=1, resources=2, storage=3, power=4, advanced_tech=5, magic=6, exploration=7, miscellaneous=8, endgame=9, faq=10.

Reference screenshot sidebar: Getting Started, Tech Basics, Resources, Storage, Power, Advanced Tech, Magic, Exploration, Miscellaneous, Endgame, FAQ.

**Result: ✅ MATCH.** The two numbering schemes differ only in base (1 vs 0) but produce the same ordering, and it matches the reference exactly.

---

## Q2 — Age → Chapter Mapping

| Age | Mapped To | Assessment |
|-----|-----------|------------|
| Age of Discovery | Getting Started | ✅ Correct |
| Stone Age | Getting Started | ✅ Correct |
| Chromatic Age | Getting Started | ✅ Correct |
| Age of Automation | Tech Basics | ✅ Correct |
| **Age of Farming** | **Resources** | ⚠ Debatable — Mystical Agriculture is a tech mod. Consider Tech Basics. |
| Age of Hoarding | Storage | ✅ Correct |
| Age of Power | Power | ✅ Correct |
| Age of Life | Advanced Tech | ✅ Defensible (Modular Golems = tech-flavoured automation) |
| Age of Simulation | Advanced Tech | ✅ Correct (IF mob duplicator) |
| Age of Magic | Magic | ✅ Correct |
| Normal / Titan / Challenge Gateways | Exploration | ✅ Correct |
| Age of Travel | Exploration | ✅ Correct |
| Age of Worlds | Exploration | ✅ Correct (RFTools dimensions) |
| Age of Miscellaneous | Miscellaneous | ✅ Correct |
| Age of Craziness | Miscellaneous | ✅ Correct |
| Age of Legends | Endgame | ✅ Correct |
| Age of Dragons | Endgame | ✅ Correct |
| AKA Nobody Is Crazy Enough... | Endgame | ✅ Correct |

**Verdict:** The only genuinely questionable mapping is Age of Farming → Resources. Mystical Agriculture is predominantly a tech-progression mod; grouping it with generic resource production (Resources chapter) instead of machine-power progression (Tech Basics) is a UI clarity miss. All other mappings are defensible.

---

## Q3 — Cross-Chapter Dependencies

Verified: zero cross-chapter dependencies exist in any SNBT file. All 11 chapters are fully independent; a new player can open Endgame on Day 1.

**Analysis:**  
- R-012 states "inter-age via 'gate' quests" but this is not implemented.  
- Two valid design choices:  
  - **A (current):** Fully open — players choose their own path. Works for experienced players or cooperative groups. Matches the original Checklist spirit (no enforced ordering beyond within-chapter).  
  - **B (gated):** First quest of each chapter depends on the last quest of the prior. Enforces the original age progression story. Better for new players.  
- **Recommendation for v1:** Keep current open layout but (1) remove the "inter-age via 'gate' quests" language from R-012 to accurately describe what's shipped, and (2) add a ROADMAP item for optional v2 chapter-gating as a configurable mode.

---

## Q6 — FTB Quests SNBT Correctness

| Item | Status |
|------|--------|
| `default_team_consume_items: false` | ✅ Correct for checklist-style |
| `disable_gui: false` | ✅ Sensible |
| `pause_game: false` | ✅ Sensible |
| `lock_team: false` | ✅ Good for solo players |
| All quests `type: "checkmark"` | ✅ Correct for v1 skeleton |
| v2 item/advancement tasks mentioned in REQUIREMENTS.md | ❌ Missing — not called out as future work |

REQUIREMENTS.md has no requirement for mixing in item/advancement tasks. This should be added as an explicit v2 requirement (see Issue #16 above).

---

## Q7 — FAQ Chapter

| Entry | Answers player's question? | Consistent with actual SF5? | Missing info |
|-------|---------------------------|----------------------------|--------------|
| How to Use This Book | ✅ Yes (navigation + Checklist note) | ⚠ "Each chapter represents an age" is inaccurate (chapters group multiple ages) | — |
| Mob Spawning Rules | ✅ Yes | ✅ Light levels and distance match `tasks.txt` exactly | Spawner pick-up + Trophy retune mechanic (from tasks.txt) not mentioned |
| What Are Gateways? | ✅ Yes | ✅ Three tier descriptions are correct | Challenge Gateway flavour text ("one-of-a-kind") is accurate |
| Discovering Colors | ✅ Partially | ✅ Mechanic description is correct | Does not tell the player that the 16 individual color-discovery checkboxes are in the Checklist book, not FTB Quests |
| Why Two Quest Systems? | ✅ Yes | ✅ | Team/shared-progress behaviour not mentioned (relevant for multiplayer) |

**Missing from all FAQ entries:** team mode / progress sharing. In multiplayer, "completing one does NOT auto-tick the other" (mentioned for Checklist vs FTB) should be expanded to explain that FTB Quests progress is per-player by default (`lock_team: false`).

---

## Positive Notes

- The EN descriptions for all four present sample quests are **well-written**: step-by-step instructions, mod attribution, practical Tips and Results sections.
- Color-code `§e` / `§6` / `§a` / `§c` usage is consistent and readable.
- The `Discovering Colors` and `Why Two Quest Systems` FAQ entries are excellent: they proactively answer the two most common new-player confusions.
- All 377 EN and RU lang keys are present and matched — no missing translations.
- `biggerreactors:reactor_casing`, `ae2:controller`, `thermal:energy_cell`, `thermal:dynamo_stirling`, `mysticalagriculture:inferium_seeds`, `industrialforegoing:mob_duplicator`, `rftoolsdim:dimension_builder`, `sophisticatedstorage:chest` are all confirmed correct for this pack.
- 183/183 quests use `type: "checkmark"` — consistent with a v1 skeleton approach.
