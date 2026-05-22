#!/usr/bin/env python3
"""Generate FTB Quests SNBT files from quests_inventory.json.

Output:
  src/minecraft/config/ftbquests/quests/data.snbt
  src/minecraft/config/ftbquests/quests/chapter_groups.snbt
  src/minecraft/config/ftbquests/quests/chapters/<chapter>.snbt
  src/minecraft/kubejs/assets/ftbquests/lang/en_us.json
  src/minecraft/kubejs/assets/ftbquests/lang/ru_ru.json

Conventions:
  - Quest id = first 16 hex chars of md5("<age>:<index>:<title>")
  - Translation keys:
      ftbquests.chapter.<chapter_id>.title
      ftbquests.quest.<quest_id>.title
      ftbquests.quest.<quest_id>.desc
  - Position (x, y) in FTB Quests grid units: section x_offset + intra-section dx, y = quest_index * 1.5
  - First quest of a section has no dependency (FTB Quests will auto-start it once chapter is unlocked).
  - Subsequent quests in the same section depend on the prior quest (linear chain).
"""
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PLANNING = REPO / ".planning" / "codebase"
OUT_QUESTS = REPO / "src" / "minecraft" / "config" / "ftbquests" / "quests"
OUT_CHAPTERS = OUT_QUESTS / "chapters"
OUT_LANG = REPO / "src" / "minecraft" / "kubejs" / "assets" / "ftbquests" / "lang"


def slugify(s: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in s).strip("_")


REGISTRY_PATH = PLANNING / "quest_id_registry.json"


def _load_registry() -> dict:
    """Frozen mapping (age, index) -> 16-char hex quest id.

    Once a quest is generated its id never changes — even if its title is edited.
    This keeps dependency chains intact across content rewrites.
    """
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {}


def _save_registry(registry: dict) -> None:
    REGISTRY_PATH.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


_REGISTRY = _load_registry()


def quest_id(age: str, idx, title: str) -> str:
    key = f"{age}::{idx}"
    if key not in _REGISTRY:
        # First time we see this (age, idx) — derive deterministically from age+idx+title and freeze.
        raw = f"{age}:{idx}:{title}".encode("utf-8")
        _REGISTRY[key] = hashlib.md5(raw).hexdigest()[:16].upper()
    return _REGISTRY[key]


def chapter_id_for_chapter(slug: str) -> str:
    """Deterministic chapter id from slug."""
    return hashlib.md5(f"chapter:{slug}".encode("utf-8")).hexdigest()[:16].upper()


def chapter_group_id() -> str:
    return "0000000000000001"


def snbt_string(s: str) -> str:
    """Quote a string in SNBT (FTB Quests dialect — same as JSON for the string layer)."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_chapter(chapter_def, quests_in_chapter):
    """Render one chapter SNBT file."""
    cid = chapter_id_for_chapter(chapter_def["id"])
    title_key = f"ftbquests.chapter.{chapter_def['id']}.title"

    lines = []
    lines.append("{")
    lines.append(f"\tid: \"{cid}\"")
    lines.append(f"\tfilename: \"{chapter_def['id']}\"")
    lines.append(f"\ttitle: \"{{{title_key}}}\"")
    lines.append(f"\ticon: \"{chapter_def['icon']}\"")
    lines.append(f"\torder_index: {chapter_def['order'] - 1}")
    lines.append("\tdefault_quest_shape: \"\"")
    lines.append("\tdefault_hide_dependency_lines: false")
    lines.append("\tgroup: \"\"")
    lines.append("\tquests: [")

    # Group quests by section so we can chain dependencies properly
    by_section = {}
    for q in quests_in_chapter:
        by_section.setdefault(q["_section"], []).append(q)

    for section_id, section_quests in by_section.items():
        section_quests.sort(key=lambda q: q["index_in_age"])
        prev_id = None
        for i, q in enumerate(section_quests):
            qid = quest_id(q["age"], q["index_in_age"], q["title"])
            x = q["_x_offset"] + 0.0
            y = q["_y_base"] + i * 1.5
            t_key = f"ftbquests.quest.{qid.lower()}.title"
            d_key = f"ftbquests.quest.{qid.lower()}.desc"

            lines.append("\t\t{")
            lines.append(f"\t\t\tx: {x}d")
            lines.append(f"\t\t\ty: {y}d")
            lines.append(f"\t\t\ttitle: \"{{{t_key}}}\"")
            lines.append(f"\t\t\ticon: \"{q['_icon']}\"")
            lines.append(f"\t\t\tid: \"{qid}\"")
            lines.append("\t\t\ttasks: [{")
            task_id = quest_id(q["age"] + "::task", q["index_in_age"], q["title"])
            lines.append(f"\t\t\t\tid: \"{task_id}\"")
            lines.append("\t\t\t\ttype: \"checkmark\"")
            lines.append(f"\t\t\t\ttitle: \"{{{t_key}}}\"")
            lines.append("\t\t\t}]")
            lines.append("\t\t\tdescription: [")
            lines.append(f"\t\t\t\t\"{{{d_key}}}\"")
            lines.append("\t\t\t]")
            if prev_id:
                lines.append(f"\t\t\tdependencies: [\"{prev_id}\"]")
            lines.append("\t\t}")
            prev_id = qid

    lines.append("\t]")
    lines.append("\tquest_links: [ ]")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main():
    inventory = json.loads((PLANNING / "quests_inventory.json").read_text(encoding="utf-8"))
    chapters_def = json.loads((PLANNING / "chapters.json").read_text(encoding="utf-8"))
    age_map = json.loads((PLANNING / "age_to_chapter.json").read_text(encoding="utf-8"))
    icons_by_section = chapters_def["quest_icons_by_section"]
    chapters = chapters_def["chapters"]
    chapter_by_id = {c["id"]: c for c in chapters}

    # Decorate every quest with its chapter / section / position / icon
    decorated_by_chapter = {c["id"]: [] for c in chapters}
    for q in inventory["quests"]:
        m = age_map.get(q["age"])
        if not m:
            print(f"WARN: no chapter mapping for age {q['age']!r}", file=sys.stderr)
            continue
        q2 = dict(q)
        q2["_chapter"] = m["chapter"]
        q2["_section"] = m["section"]
        q2["_x_offset"] = m["x_offset"]
        q2["_y_base"] = m["y_base"]
        q2["_icon"] = icons_by_section.get(m["section"], "minecraft:paper")
        decorated_by_chapter[m["chapter"]].append(q2)

    # Ensure dirs
    OUT_CHAPTERS.mkdir(parents=True, exist_ok=True)
    OUT_LANG.mkdir(parents=True, exist_ok=True)

    # data.snbt — root config: team-mode single, no item consumption.
    data_snbt = """{
\tdefault_reward_team: false
\tdefault_team_consume_items: false
\tdefault_quest_disable_jei: false
\tdefault_quest_shape: ""
\tdefault_quest_size: 1.0d
\tdefault_repeatable_quest: false
\tdrop_loot_crates: false
\temergency_items: [ ]
\temergency_items_cooldown: 300
\tloot_crate_no_drop: { passive: 400, monster: 600, boss: 0 }
\tloot_crates: { }
\tlock_message: ""
\tdetection_delay: 20
\tdisable_gui: false
\tgrid_scale: 0.5d
\tpause_game: false
\tlock_team: false
\tdrop_loot_crates_on_monsters: false
\tdrop_loot_crates_on_bosses: true
}
"""
    (OUT_QUESTS / "data.snbt").write_text(data_snbt, encoding="utf-8")

    # chapter_groups.snbt — single flat list
    (OUT_QUESTS / "chapter_groups.snbt").write_text("{ chapter_groups: [ ] }\n", encoding="utf-8")

    # Render each chapter
    for chapter_def in chapters:
        quests = decorated_by_chapter[chapter_def["id"]]
        if not quests and chapter_def["id"] != "faq":
            # still write a placeholder chapter so the sidebar shows it
            placeholder_lines = [
                "{",
                f"\tid: \"{chapter_id_for_chapter(chapter_def['id'])}\"",
                f"\tfilename: \"{chapter_def['id']}\"",
                f"\ttitle: \"{{ftbquests.chapter.{chapter_def['id']}.title}}\"",
                f"\ticon: \"{chapter_def['icon']}\"",
                f"\torder_index: {chapter_def['order'] - 1}",
                "\tquests: [ ]",
                "}",
            ]
            (OUT_CHAPTERS / f"{chapter_def['id']}.snbt").write_text("\n".join(placeholder_lines) + "\n", encoding="utf-8")
        else:
            (OUT_CHAPTERS / f"{chapter_def['id']}.snbt").write_text(render_chapter(chapter_def, quests), encoding="utf-8")

    # FAQ chapter — synthetic content
    faq_lines = [
        "{",
        f"\tid: \"{chapter_id_for_chapter('faq')}\"",
        "\tfilename: \"faq\"",
        "\ttitle: \"{ftbquests.chapter.faq.title}\"",
        "\ticon: \"minecraft:writable_book\"",
        "\torder_index: 10",
        "\tquests: [",
    ]
    faq_entries = [
        ("how_to_use", "How to use this book", "minecraft:writable_book", 0.0, 0.0),
        ("mob_spawning", "Mob spawning rules", "minecraft:zombie_head", 0.0, 1.5),
        ("gateways_intro", "What are Gateways?", "gateways:gate_pearl", 0.0, 3.0),
        ("colors", "Discovering colors", "minecraft:white_concrete_powder", 0.0, 4.5),
        ("checklist_parallel", "Why is there still a Checklist book?", "minecraft:lectern", 0.0, 6.0),
    ]
    # Add the chapter-level fields for visual consistency with other chapters
    faq_lines.insert(6, "\tdefault_quest_shape: \"\"")
    faq_lines.insert(7, "\tdefault_hide_dependency_lines: false")
    faq_lines.insert(8, "\tgroup: \"\"")
    for idx, (slug, _title, icon, x, y) in enumerate(faq_entries, start=1):
        # Deterministic id derived from the slug + a stable counter — no Python hash() randomness
        qid = quest_id("FAQ", f"{idx:02d}-{slug}", slug)
        faq_lines.append("\t\t{")
        faq_lines.append(f"\t\t\tx: {x}d")
        faq_lines.append(f"\t\t\ty: {y}d")
        faq_lines.append(f"\t\t\ttitle: \"{{ftbquests.quest.{qid.lower()}.title}}\"")
        faq_lines.append(f"\t\t\ticon: \"{icon}\"")
        faq_lines.append(f"\t\t\tid: \"{qid}\"")
        faq_lines.append("\t\t\ttasks: [{")
        task_id = quest_id("FAQ::task", f"{idx:02d}-{slug}", slug)
        faq_lines.append(f"\t\t\t\tid: \"{task_id}\"")
        faq_lines.append("\t\t\t\ttype: \"checkmark\"")
        faq_lines.append("\t\t\t}]")
        faq_lines.append("\t\t\tdescription: [")
        faq_lines.append(f"\t\t\t\t\"{{ftbquests.quest.{qid.lower()}.desc}}\"")
        faq_lines.append("\t\t\t]")
        faq_lines.append("\t\t}")
    faq_lines.extend(["\t]", "}"])
    (OUT_CHAPTERS / "faq.snbt").write_text("\n".join(faq_lines) + "\n", encoding="utf-8")

    # Build i18n: load existing lang files (so hand-written wiki descriptions survive a re-run)
    # and only fill in keys that are missing.
    def _load_existing(path: Path) -> dict:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    en = _load_existing(OUT_LANG / "en_us.json")
    ru = _load_existing(OUT_LANG / "ru_ru.json")

    def en_set(key: str, value: str) -> None:
        """Only set if the key is missing — never overwrite human-curated translations."""
        en.setdefault(key, value)

    def ru_set(key: str, value: str) -> None:
        ru.setdefault(key, value)

    for chapter_def in chapters:
        en_set(f"ftbquests.chapter.{chapter_def['id']}.title", chapter_def["title"])
        ru_set(f"ftbquests.chapter.{chapter_def['id']}.title", {
            "getting_started": "Начало пути",
            "tech_basics":     "Основы техники",
            "resources":       "Ресурсы",
            "storage":         "Хранилище",
            "power":           "Энергия",
            "advanced_tech":   "Сложная техника",
            "magic":           "Магия",
            "exploration":     "Исследование",
            "miscellaneous":   "Разное",
            "endgame":         "Финал",
            "faq":             "Справка",
        }[chapter_def["id"]])

    # Quest titles & placeholder descs for all 178 quests — only set missing keys
    for q in inventory["quests"]:
        qid = quest_id(q["age"], q["index_in_age"], q["title"]).lower()
        en_set(f"ftbquests.quest.{qid}.title", q["title"])
        en_set(f"ftbquests.quest.{qid}.desc", q["title"] + ".")
        ru_set(f"ftbquests.quest.{qid}.title", q["title"])  # placeholder, full RU in wiki phase
        ru_set(f"ftbquests.quest.{qid}.desc", q["title"] + ".")

    # FAQ keys
    faq_titles_en = {
        "how_to_use":         ("How to Use This Book", "Navigate with the sidebar. Each chapter represents an age of progression. Quests link top-to-bottom; complete the prerequisite to unlock its child. The Checklist book is still installed if you prefer the classic checkbox UI."),
        "mob_spawning":       ("Mob Spawning Rules", "Mobs do not spawn naturally on the island. Place a mob Trophy (drop from a Gateway) on a block to allow that mob to spawn nearby. Passives need light level 8–15, hostiles 0–7, and any mob must be > 24 blocks from you. Press §3F7§r to see light levels."),
        "gateways_intro":     ("What Are Gateways?", "Gateways are wave-based fights you trigger with a Gateway Pearl. Beating them rewards a mob Trophy (so you can spawn that mob) and loot. Three flavours: §aNormal§r (intro), §6Titan§r (waves 50/100/150), §cChallenge§r (one-of-a-kind themed fights)."),
        "colors":             ("Discovering Colors", "You start the pack colorblind. Each of the 16 Minecraft colors must be §ediscovered§r via a specific crafting recipe or world event (throwing dye in water, dyeing a sapling, smelting, etc.). Discovering a color recolors the world for you and unlocks recipes that use that color."),
        "checklist_parallel": ("Why Two Quest Systems?", "The original §aChecklist§r book is kept for a fast \"todo list\" experience. §6FTB Quests§r is the main progression UI with dependency graphs, icons, and per-quest guides. Use whichever you prefer — neither is required to play, and completing one does NOT auto-tick the other."),
    }
    faq_titles_ru = {
        "how_to_use":         ("Как пользоваться книгой", "Навигация — через сайдбар. Каждая глава = одна эпоха прогрессии. Квесты связаны сверху вниз; выполнение родителя открывает дочерний квест. Если предпочитаешь классический чеклист — установлен мод Checklist."),
        "mob_spawning":       ("Правила спавна мобов", "На острове мобы не появляются естественным образом. Чтобы разрешить спавн, поставь Трофей моба (выпадает из Gateway). Пассивам нужен свет 8–15, враждебным 0–7, и любой моб должен быть > 24 блоков от тебя. Уровень света — клавиша §3F7§r."),
        "gateways_intro":     ("Что такое Gateways?", "Gateway — это волновая арена, которая активируется Gateway Pearl. За победу даётся Трофей моба (открывает спавн) и лут. Три вида: §aОбычные§r (старт), §6Титан§r (волны 50/100/150), §cChallenge§r (уникальные тематические боссы)."),
        "colors":             ("Открытие цветов", "Игра начинается в чёрно-белом мире. Каждый из 16 цветов нужно §eоткрыть§r через определённый рецепт или действие (бросить краситель в воду, покрасить саженец, обжечь и т. д.). Открытие цвета возвращает миру цвет и открывает рецепты с этим цветом."),
        "checklist_parallel": ("Зачем две системы квестов?", "Книга §aChecklist§r оставлена для быстрого \"todo-листа\". §6FTB Quests§r — основная система прогрессии с деревом, иконками и пошаговыми гайдами. Используй любую — обе необязательны, и выполнение в одной не отмечает квест в другой."),
    }
    # Resolve slug -> idx so lang-file keys line up with chapter SNBT IDs
    faq_slug_to_idx = {slug: idx for idx, (slug, _title, _icon, _x, _y) in enumerate(faq_entries, start=1)}
    # FAQ entries: these ARE hand-authored seed text, but only set if missing so a future
    # edit to en_us.json wins over the inlined seed.
    for slug, (t, d) in faq_titles_en.items():
        idx = faq_slug_to_idx[slug]
        qid = quest_id("FAQ", f"{idx:02d}-{slug}", slug).lower()
        en_set(f"ftbquests.quest.{qid}.title", t)
        en_set(f"ftbquests.quest.{qid}.desc", d)
    for slug, (t, d) in faq_titles_ru.items():
        idx = faq_slug_to_idx[slug]
        qid = quest_id("FAQ", f"{idx:02d}-{slug}", slug).lower()
        ru_set(f"ftbquests.quest.{qid}.title", t)
        ru_set(f"ftbquests.quest.{qid}.desc", d)

    (OUT_LANG / "en_us.json").write_text(json.dumps(en, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    (OUT_LANG / "ru_ru.json").write_text(json.dumps(ru, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    # Persist the (now possibly-expanded) registry so future runs are reproducible.
    _save_registry(_REGISTRY)

    # Summary
    print(f"Generated {len(chapters)} chapters, {sum(len(v) for v in decorated_by_chapter.values())} quests + {len(faq_entries)} FAQ entries")
    print(f"  data.snbt: {OUT_QUESTS / 'data.snbt'}")
    print(f"  chapters: {OUT_CHAPTERS}")
    print(f"  en_us.json keys: {len(en)}")
    print(f"  ru_ru.json keys: {len(ru)}")


if __name__ == "__main__":
    main()
