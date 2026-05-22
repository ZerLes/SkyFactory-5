# Roadmap

| Phase | Title | Requirements covered | Depends on | PR |
|------:|-------|---------------------|-----------|----|
| 01 | Foundation: mod manifest, FTB Quests config skeleton, i18n scaffolding | R-001 .. R-004, R-031 | — | `feat/ftb-quests-migration` (this PR, draft) |
| 02 | Quest skeleton — 11 chapters, all 178 quests stubbed with dependencies + icons | R-010 .. R-013, R-030 | 01 | same PR |
| 03 | Full mini-wiki for Getting Started (Discovery + Stone + Chromatic = 26 quests), EN + RU | R-014 (first 3 ages), R-031 (subset) | 02 | same PR |
| 04 | CI/CD: build/validate/release GitHub Actions workflows | R-040 .. R-045 | — (parallel with 01-03) | same PR |
| 05 | Docs: README + CLAUDE.md updates | R-050, R-051 | 01-04 | same PR |
| --- | --- | --- | --- | --- |
| 10 | Full wiki: Tech Basics + Resources + Storage (~17 quests) | R-020 subset | this PR merged | follow-up PR |
| 11 | Full wiki: Power + Advanced Tech (~21 quests) | R-020 subset | 10 | follow-up PR |
| 12 | Full wiki: Magic (54 quests, 4 sub-trees) | R-020 subset | 10 | follow-up PR (largest) |
| 13 | Full wiki: Exploration (Gateways + Travel + Worlds, ~21 quests) | R-020 subset | 10 | follow-up PR |
| 14 | Full wiki: Misc + Endgame (Legends/Dragons/Simulation/Craziness, ~40 quests) | R-020 subset | 10-13 | follow-up PR |
| 15 | Full RU translations refresh covering 10-14 | R-032 | per-age PRs above | follow-up PR |

## Age → FTB Quests Category mapping

| Age (`tasks.txt`) | Category | Count |
|---|---|---:|
| Age of Discovery | Getting Started | 16 |
| Stone Age | Getting Started | 4 |
| Chromatic Age | Getting Started | 6 |
| Age of Automation | Tech Basics | 7 |
| Age of Farming | Resources | 5 |
| Age of Hoarding | Storage | 5 |
| Age of Power | Power | 11 |
| Age of Life | Advanced Tech | 10 |
| Age of Simulation | Advanced Tech | 5 |
| Age of Magic (4 sub) | Magic | 54 |
| Normal Gateways | Exploration | 5 |
| Titan Gateways | Exploration | 4 |
| Challenge Gateways | Exploration | 1 |
| Age of Travel | Exploration | 5 |
| Age of Worlds | Exploration | 6 |
| Age of Miscellaneous | Miscellaneous | 7 |
| Age of Craziness | Miscellaneous | 6 |
| Age of Legends | Endgame | 5 |
| Age of Dragons | Endgame | 12 |
| AKA Nobody Is Crazy Enough... | Endgame | 4 |
| (new — book usage / mob spawning reference) | FAQ | ~5 |
| **Total** | | **~183** |
