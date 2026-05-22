# SkyFactory 5 [![Curseforge][curseimg]][curselink]

[![Twitch Status](https://img.shields.io/twitch/status/darkosto?color=411145&label=Darkosto&logo=twitch)](https://twitch.tv/darkosto) [![Discord][discordimg]][discordlink]

[discordimg]: https://img.shields.io/discord/329440410839678986.svg?logo=discord&logoWidth=18&colorB=7289DA
[discordlink]: https://discord.gg/darkosto
[curseimg]: http://cf.way2muchnoise.eu/392141.svg
[curselink]: https://www.curseforge.com/minecraft/modpacks/skyfactory-5

## Development

The repo utilizes Node.js (and npm) to manage build tools, and other useful dependencies. In addition, the repo includes pre-configured settings and recommended extensions to improve the developer experience, so VSCode is recommended.

1. [Getting Started](#getting-started)
2. [Development Loop](#development-loop)
3. [Additional Scripts](#additional-scripts)

### Getting Started

When first starting development, make sure you go through these steps to get your development environment set up.

1. [Installing / Setting Up Node](#nodejs--npm)

#### Node.js / NPM

To get started, make sure you have Node.js installed. For easier management of your Node.js version, we recommend installing NVM (Node Version Manager) instead. For Windows you can install from the latest release [here](https://github.com/coreybutler/nvm-windows/releases) and for OSX/Linux follow the steps [here](https://github.com/nvm-sh/nvm#installing-and-updating).

Once installed, run `nvm install 20.5.1` then `nvm use 20.5.1` once the installation completes.

### Development Loop

1. Install any recommended project extensions.
2. Ensure you are using the correct Node.js version by running `npm run setup:node`.
3. If you've pulled in changes, make sure you've updated your dependencies by running `npm install`.
4. Run `npm run start` to start Minecraft.
5. Work on the project.

### Updating Minecraft or Forge version

The versions used are tracked in the [mc-package.json](./mc-package.json) file. To update:

1. Change the versions in the [mc-package.json](./mc-package.json) file.
2. Update the [settings.bat](./src/server/settings.bat) file.
3. Update the [settings.sh](./src/server/settings.sh) file.

### Additional Scripts

These are additional scripts that are provided for easing development processes.

- `npm run generate` starts a prompt to generate certain project files.
- `npm run symlink` generates symlinks between the repo and a minecraft instance.

## Quest Book (FTB Quests)

The primary in-game progression UI is **FTB Quests**, organised into 11 chapters that map 1:1 to the ages from the original `Checklist` book:

| Chapter | Source ages from `tasks.txt` |
|---|---|
| Getting Started | Age of Discovery, Stone Age, Chromatic Age |
| Tech Basics | Age of Automation |
| Resources | Age of Farming |
| Storage | Age of Hoarding |
| Power | Age of Power |
| Advanced Tech | Age of Life, Age of Simulation |
| Magic | Age of Magic (Ars Nouveau / Occultism / Botanist / Mastery) |
| Exploration | Normal / Titan / Challenge Gateways, Age of Travel, Age of Worlds |
| Miscellaneous | Age of Miscellaneous, Age of Craziness |
| Endgame | Age of Legends, Age of Dragons, Crazy/Nobody-Would-Actually-Do-This |
| FAQ | Synthetic — book usage, mob spawning rules, gateway intro, color discovery |

The **`Checklist`** mod and its `config/checklist/` book are kept installed in parallel — if you prefer the lightweight chec​kbox UI, you can use both. Neither is required to play, and completion of a quest in one does NOT auto-tick the other.

### File layout

- `src/minecraft/config/ftbquests/quests/data.snbt` — root quest-book config (team-mode `single`, item consumption disabled)
- `src/minecraft/config/ftbquests/quests/chapters/<chapter>.snbt` — one file per chapter
- `src/minecraft/kubejs/assets/ftbquests/lang/en_us.json` — English titles + descriptions
- `src/minecraft/kubejs/assets/ftbquests/lang/ru_ru.json` — Russian translations

### Adding or editing a quest

1. Edit `.planning/codebase/quests_inventory.json` (the source of truth, parsed from `tasks.txt`).
2. Run `python3 .planning/codebase/generate_ftbquests.py` to regenerate the SNBT files.
3. Update both `en_us.json` and `ru_ru.json` for the affected translation keys. The validate workflow fails the PR if the two languages don't have the same keyset.
4. Open a draft PR; see [`CLAUDE.md`](./CLAUDE.md) for conventions.

### Adding a new language

Drop a new `<lang>.json` next to `en_us.json` with the same keys. FTB Quests will auto-discover it. Run the parity check locally:

```bash
python3 -c "import json; en=set(json.load(open('src/minecraft/kubejs/assets/ftbquests/lang/en_us.json'))); new=set(json.load(open('src/minecraft/kubejs/assets/ftbquests/lang/<lang>.json'))); print('missing:', en - new)"
```

## Release

### Creating A Release

Releases are now built by [`.github/workflows/release.yml`](./.github/workflows/release.yml) on every `v*.*.*` git tag, with both client and server zips attached to the GitHub Release. To cut one:

1. Bump `version` in [mc-package.json](./mc-package.json).
2. Open a PR, get it merged.
3. Tag the merge commit: `git tag v5.0.9 && git push origin v5.0.9`. The release workflow asserts that the tag matches `mc-package.json` and fails fast if not.
4. The zips appear on the Releases page; download and upload to CurseForge.

For a quick local build (no Mojang auth needed): `SF5_CI_SKIP_FORGE_DOWNLOAD=true npm run release`. The server zip will embed a `SERVER_README.txt` with the Forge installer Maven URL instead of bundling the installer.

The legacy manual flow still works:

1. Increment the version in [mc-package.json](./mc-package.json).
2. Run `npm run release` to generate a client and server zip file in the [.releases directory](./.releases/).

### Continuous integration

- [`validate.yml`](./.github/workflows/validate.yml) — runs on every PR. Runs `npm run lint:direct` and verifies the FTB Quests SNBT layout + EN/RU key parity.
- [`build.yml`](./.github/workflows/build.yml) — runs on every push and PR. Produces `SkyFactory-5-{client|server}-v{version}-{short-sha}.zip` as 14-day workflow artifacts so you can grab a build from any branch.

### Ignoring Files

Files in the repo can be ignored from releases by adding to the respective releaseignore file:

- For client-only ignore entries: [.releaseignore-client](./releaseignore-client)
- For server-only ignore entries: [.releaseignore-server](./releaseignore-server)
  - A common use case for this is to ignore client-only mods.
- For ignore entries that apply to both client and server releases: [.releaseignore-shared](./releaseignore-shared)
