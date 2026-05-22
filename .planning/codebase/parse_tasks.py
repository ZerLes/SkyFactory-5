#!/usr/bin/env python3
"""Parse SkyFactory 5 checklist tasks.txt into structured JSON inventory.

Format rules observed in src/minecraft/config/checklist/tasks.txt:
  - "===" on its own line separates pages/sections.
  - Lines beginning with "#" are book commentary/headers (not tasks).
  - Lines matching r"^#\s*§1--==§(0|...)<Age Name>§1==--" mark an Age section.
  - Lines matching r"^#§1-=§0<SubCategory>§1=-" mark a sub-category within current age.
  - Any non-blank non-"#" non-"===" line is a checklist task.
  - "Discover §X==§0COLOR§X==" lines on the colors page are tasks too.
  - Minecraft formatting codes (§ + char) must be stripped for plain text titles.

Output: JSON list of {age, subcategory|null, index_in_age, title, raw}.
"""
import json
import re
import sys

MC_CODE = re.compile(r"§.")  # § + 1 char (color / formatting)
# §1 = blue, §0 = black etc. We allow any single formatting char before the title.
AGE_HEADER = re.compile(r"^#\s*§1--==§.([\w\s'\-]+?)§1==--\s*$")
SUB_HEADER = re.compile(r"^#§1-=§.([\w\s'\-]+?)§1=-\s*$")
COLOR_TASK = re.compile(r"^Discover\s+§.==§.([A-Za-z ]+)§.==")


def strip_codes(s: str) -> str:
    return MC_CODE.sub("", s).strip()


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    quests = []
    # The "Mob Spawning" page is a reference page in the book, not a real Age.
    # Reference pages explicitly excluded from quest extraction.
    REFERENCE_AGES = {"Mob Spawning"}
    current_age = "Colors"  # initial color-discovery page has no header
    current_sub = None
    index_in_age = 0

    for raw in lines:
        s = raw.rstrip()
        if not s or s == "===":
            continue

        # Detect Age header (with or without leading space after #)
        m_age = AGE_HEADER.match(s)
        if m_age:
            current_age = strip_codes(m_age.group(1))
            current_sub = None
            index_in_age = 0
            continue

        m_sub = SUB_HEADER.match(s)
        if m_sub:
            current_sub = strip_codes(m_sub.group(1))
            continue

        if current_age in REFERENCE_AGES:
            continue

        # Color discovery page
        m_color = COLOR_TASK.match(s)
        if m_color:
            color = m_color.group(1).strip()
            index_in_age += 1
            quests.append({
                "age": current_age,
                "subcategory": None,
                "index_in_age": index_in_age,
                "title": f"Discover {color}",
                "raw": s,
            })
            continue

        # Skip comment lines (book intros, thank-yous, etc.)
        if s.startswith("#"):
            continue

        # Real task line.
        index_in_age += 1
        quests.append({
            "age": current_age,
            "subcategory": current_sub,
            "index_in_age": index_in_age,
            "title": strip_codes(s),
            "raw": s,
        })

    # Stats
    by_age = {}
    for q in quests:
        by_age.setdefault(q["age"], 0)
        by_age[q["age"]] += 1

    out = {
        "total_quests": len(quests),
        "by_age": by_age,
        "quests": quests,
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main(sys.argv[1])
