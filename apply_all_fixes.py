#!/usr/bin/env python3
"""Apply all content fixes to en_us.json and ru_ru.json."""

import json

EN_PATH = '/home/user/workspace/sf5/src/minecraft/kubejs/assets/ftbquests/lang/en_us.json'
RU_PATH = '/home/user/workspace/sf5/src/minecraft/kubejs/assets/ftbquests/lang/ru_ru.json'

en = json.load(open(EN_PATH))
ru = json.load(open(RU_PATH))

assert len(en) == 377, f"Expected 377 EN keys, got {len(en)}"
assert len(ru) == 377, f"Expected 377 RU keys, got {len(ru)}"

edited_keys = set()

# =========================================================================
# FIX 1 — Rewrite Make Lava in a Fired Crucible (ForceCraft Heat block)
# Quest: Stone Age idx=1 → qid=b81aea269d8e19e4
# =========================================================================
LAVA_KEY = 'ftbquests.quest.b81aea269d8e19e4.desc'

en[LAVA_KEY] = (
    "Place a §eFired Crucible§r (smelt a basic Crucible in a furnace first) on top of a §6ForceCraft Heat block§r "
    "(§eForceCraft§r Tier 1 item — craft and place it directly below the crucible).\n\n"
    "Fill the Fired Crucible with §6Cobblestone§r. The Heat block melts it into §eLava§r! Collect with an empty bucket.\n\n"
    "§aTip:§r All standard Ex Nihilo heat sources (Campfire, Torch, Lava, Blaze Burner) are §cdisabled§r in SF5. "
    "The §eForceCraft Heat block§r is the only valid heat source for Fired Crucibles.\n\n"
    "§aResult:§r Lava + Water = Obsidian (next quest!)."
)

ru[LAVA_KEY] = (
    "Поставь §eОбожжённый Тигель§r (Fired Crucible — сначала переплавь обычный тигель в печи) на §6блок Жара ForceCraft§r "
    "(§eForceCraft§r предмет 1-го уровня — скрафти и поставь его прямо под тиглем).\n\n"
    "Загрузи §6Булыжник§r в тигель. Блок Жара расплавит его в §eЛаву§r! Собери пустым ведром.\n\n"
    "§cВнимание:§r Все стандартные источники тепла Ex Nihilo (Костёр, Факел, Лава, Blaze Burner) §cотключены§r в SF5. "
    "§eБлок Жара ForceCraft§r — единственный подходящий источник тепла для Обожжённых Тиглей.\n\n"
    "§aРезультат:§r Лава + Вода = Обсидиан (следующий квест!)."
)

edited_keys.add(LAVA_KEY)
print(f"Fix 1: {LAVA_KEY}  EN§={en[LAVA_KEY].count('§')} RU§={ru[LAVA_KEY].count('§')}")

# =========================================================================
# FIX 2 — Replace "Gear Crafting Table" → "Gear Smithing Table" + fix center slot
# Quest: Stone Age idx=4 → qid=096d3b92e663cb71
# =========================================================================
SILENT_KEY = 'ftbquests.quest.096d3b92e663cb71.desc'

en[SILENT_KEY] = (
    "Open the §eSilent's Gear§r tool workbench (§6Gear Smithing Table§r). "
    "Open the §eGear Smithing Table§r and slot your existing tool plus the new material to swap it in. "
    "Replace the §6head material§r with §eCobblestone§r, §eAndesite§r, §eDiorite§r, or §eGranite§r.\n\n"
    "Stone-tier materials significantly improve §6mining speed§r and §6durability§r over Colorless/Wood tier.\n\n"
    "§aTip:§r Each stone type has slightly different stats — experiment! §eAndesite§r and §eGranite§r often have better durability bonuses.\n\n"
    "§aResult:§r Upgraded tools let you mine faster, progress through the Stone Age, and prepare for §6Metal Age§r materials ahead."
)

ru[SILENT_KEY] = (
    "Открой §eверстак Silent's Gear§r (§6Gear Smithing Table§r). "
    "Открой §eGear Smithing Table§r и вставь свой инструмент вместе с новым материалом, чтобы заменить его. "
    "Замени §6материал головки§r на §eБулыжник§r, §eАндезит§r, §eДиорит§r или §eГранит§r.\n\n"
    "Каменный материал значительно улучшает §6скорость добычи§r и §6прочность§r по сравнению с бесцветным/деревянным уровнем.\n\n"
    "§aСовет:§r Каждый тип камня даёт немного разные характеристики — экспериментируй! §eАндезит§r и §eГранит§r часто дают лучший бонус к прочности.\n\n"
    "§aРезультат:§r Прокачанные инструменты ускоряют добычу и готовят тебя к материалам §6Металлического Века§r."
)

edited_keys.add(SILENT_KEY)
print(f"Fix 2: {SILENT_KEY}  EN§={en[SILENT_KEY].count('§')} RU§={ru[SILENT_KEY].count('§')}")

# =========================================================================
# FIX 3 — "Sappling" → "Sapling" (scan all keys)
# =========================================================================
for k in list(en.keys()):
    old = en[k]
    en[k] = en[k].replace('Sappling', 'Sapling')
    if en[k] != old:
        edited_keys.add(k)
        print(f"Fix 3 EN: fixed Sappling→Sapling in {k}")

for k in list(ru.keys()):
    old = ru[k]
    ru[k] = ru[k].replace('Sappling', 'Sapling')
    if ru[k] != old:
        edited_keys.add(k)
        print(f"Fix 3 RU: fixed Sappling→Sapling in {k}")

# =========================================================================
# FIX 4 — Balance § color codes between EN and RU for 4 specific keys
# =========================================================================

# Key 1: Automate Cobblestone — EN=16, RU=12 (need 4 more § in RU)
# Fix: add §e§r split on "Block Placer"/"Block Breaker" and add §eБурилки§r
COBBLE_KEY = 'ftbquests.quest.3f5aa9a592917d94.desc'
ru[COBBLE_KEY] = (
    "Ручное производство Булыжника из Пепла — слишком медленно. Время автоматизировать!\n\n"
    "Классический метод: построй §eГенератор Булыжника§r — расположи источники Лавы и Воды по разные стороны от ямки. "
    "В ямке формируется Булыжник; ломай его §6Block Breaker§r или §6Mechanical Drill§r (мод Create).\n\n"
    "§aСовет:§r Связка §eBlock Placer§r + §eBlock Breaker§r из Industrial Foregoing отлично работает. "
    "§eБурилки§r мода Create дают более высокую производительность.\n\n"
    "§aРезультат:§r Бесконечный Булыжник → Камень, Гравий, Песок, Лава. Основа всей будущей переработки ресурсов!"
)
edited_keys.add(COBBLE_KEY)
print(f"Fix 4: {COBBLE_KEY}  EN§={en[COBBLE_KEY].count('§')} RU§={ru[COBBLE_KEY].count('§')}")

# Key 2: Obtain Obsidian — EN=16, RU=14 (need 2 more § in RU)
# Fix: add §6Зачарованным Золотым Яблоком§r to match EN's §6Enchanted Golden Apple§r
OBSIDIAN_KEY = 'ftbquests.quest.4e4cf2d27ba2d029.desc'
ru[OBSIDIAN_KEY] = (
    "Классическая ванильная механика: §6источник Воды§r поверх §6источника Лавы§r создаёт §eОбсидиан§r.\n\n"
    "Положи источник Лавы в ямку, затем вылей или поставь Воду сверху. Лава превратится в Обсидиан — добывай его §6Алмазной Киркой§r (или лучше).\n\n"
    "§aСовет:§r Можно скрафтить §eАлмазную Кирку Silent's Gear§r или ускорить добычу алмазов через просеивание с §6Зачарованным Золотым Яблоком§r.\n\n"
    "§aРезультат:§r Обсидиан нужен для Портала в Незер, Стола Зачарования, Эндер-сундука и многих важных mid-game рецептов."
)
edited_keys.add(OBSIDIAN_KEY)
print(f"Fix 4: {OBSIDIAN_KEY}  EN§={en[OBSIDIAN_KEY].count('§')} RU§={ru[OBSIDIAN_KEY].count('§')}")

# Key 3: Silkworm String — EN=14, RU=12 (need 2 more § in RU)
# Fix: add §e§r around "заразятся" to match EN's §einfest§r
SILKWORM_KEY = 'ftbquests.quest.a692fda4a82cbcb1.desc'
ru[SILKWORM_KEY] = (
    "Найди §eШелкопряда§r (Silkworm) — он выпадает из листьев при ломке. "
    "Кликни ПКМ по §6Листовому блоку§r с Шелкопрядом в руке — листья §eзаразятся§r!\n\n"
    "Заражение постепенно распространяется на соседние листья. Когда лист полностью заражён (белая паутина), ломка даёт §6Нить§r (String).\n\n"
    "§aСовет:§r Дай заражению распространиться на соседние листья перед сбором. Используй §eСерп§r для быстрой массовой уборки!\n\n"
    "§aРезультат:§r Нить → Шерсть → куча рецептов: кровати, ковры, зачарование и многое другое."
)
edited_keys.add(SILKWORM_KEY)
print(f"Fix 4: {SILKWORM_KEY}  EN§={en[SILKWORM_KEY].count('§')} RU§={ru[SILKWORM_KEY].count('§')}")

# Key 4: Colored Crafting Tables — EN=16, RU=14 (need 2 more § in RU)
# Fix: add §6Краситель§r to match EN's §6Dye§r reference
COLORED_KEY = 'ftbquests.quest.bb96e110dd945484.desc'
ru[COLORED_KEY] = (
    "Для каждого из §e16 цветов§r существует свой §6Цветной Верстак§r. Для крафта нужны §64 Цветных Доски§r одного цвета в сетке 2×2.\n\n"
    "§eЦветные Доски§r получаются покраской §6Бесцветных Досок§r краской §6Краситель§r, или из цветных деревьев. Каждый верстак открывает рецепты своего цвета.\n\n"
    "§aСовет:§r Собери несколько разных цветных верстаков — это откроет больше рецептов в начале игры.\n\n"
    "Больше цветов = больше возможностей! Загляни в главу §6Chromatic Age§r за советами по получению краски."
)
edited_keys.add(COLORED_KEY)
print(f"Fix 4: {COLORED_KEY}  EN§={en[COLORED_KEY].count('§')} RU§={ru[COLORED_KEY].count('§')}")

# =========================================================================
# FIX 5 — Add §aNext:§r lines to 5 quests
# =========================================================================

def has_next_or_result(text):
    return '§aNext:§r' in text or '§aResult:§r' in text or '§aРезультат:§r' in text

# Age of Discovery idx=1 → next is idx=2: "Use a Barrel to create Dirt"
AOD1_KEY = 'ftbquests.quest.7c8df3e097e319fc.desc'
if not has_next_or_result(en[AOD1_KEY]):
    en[AOD1_KEY] += '\n\n§aNext:§r Use a Barrel to create Dirt.'
    edited_keys.add(AOD1_KEY)
    print(f"Fix 5: added Next to EN {AOD1_KEY}")
if not has_next_or_result(ru[AOD1_KEY]):
    ru[AOD1_KEY] += '\n\n§aДалее:§r Use a Barrel to create Dirt.'
    edited_keys.add(AOD1_KEY)
    print(f"Fix 5: added Next to RU {AOD1_KEY}")

# Stone Age idx=1 (Make Lava) — we already rewrote it with §aResult:§r mentioning Obsidian ✓
print(f"Fix 5: Make Lava already has Result (EN has_result={has_next_or_result(en[LAVA_KEY])})")

# Chromatic Age idx=2 (Dye Block) — already has §aResult:§r ✓
CHROMA2_KEY = 'ftbquests.quest.7646a7b0d274cd26.desc'
print(f"Fix 5: Chromatic Age idx=2 already has Result (EN has_result={has_next_or_result(en[CHROMA2_KEY])})")

# Age of Discovery idx=2 (Barrel) — check
BARREL_KEY = 'ftbquests.quest.bce0485ccf92da1a.desc'
if not has_next_or_result(en[BARREL_KEY]):
    en[BARREL_KEY] += '\n\n§aNext:§r Eat Dirt!'
    edited_keys.add(BARREL_KEY)
    print(f"Fix 5: added Next to EN {BARREL_KEY}")
if not has_next_or_result(ru[BARREL_KEY]):
    ru[BARREL_KEY] += '\n\n§aДалее:§r Eat Dirt!'
    edited_keys.add(BARREL_KEY)
    print(f"Fix 5: added Next to RU {BARREL_KEY}")

# Stone Age idx=4 (Silent's Gear) — we just rewrote it, check
# We wrote §aResult:§r in both EN and RU ✓ but need to update it with the cross-age reference
# The rewrite has: "§aResult:§r Upgraded tools..." — need to also mention next age
# Per instructions: Stone Age idx=4 (last in age), set Next to "(Chromatic Age — Throw Dye into Water to change its color)"
# The existing §aResult:§r line doesn't name the next age, so we need to add a §aNext:§r line
if '§aNext:§r' not in en[SILENT_KEY]:
    en[SILENT_KEY] += '\n\n§aNext:§r (Chromatic Age — Throw Dye into Water to change its color).'
    edited_keys.add(SILENT_KEY)
    print(f"Fix 5: added Next to EN {SILENT_KEY}")
if '§aДалее:§r' not in ru[SILENT_KEY] and '§aNext:§r' not in ru[SILENT_KEY]:
    ru[SILENT_KEY] += '\n\n§aДалее:§r (Chromatic Age — Throw Dye into Water to change its color).'
    edited_keys.add(SILENT_KEY)
    print(f"Fix 5: added Next to RU {SILENT_KEY}")

# =========================================================================
# Final § balance check for Fix 5 additions
# =========================================================================
print("\n=== Post-Fix 5 § balance check ===")
for k in [AOD1_KEY, LAVA_KEY, CHROMA2_KEY, BARREL_KEY, SILENT_KEY]:
    ec = en[k].count('§')
    rc = ru[k].count('§')
    status = "OK" if ec == rc else "MISMATCH"
    print(f"  {k}: EN§={ec} RU§={rc} [{status}]")

# AOD1 and Barrel: we added §aNext:§r to EN (2 §) and §aДалее:§r to RU (2 §) — balanced
# Silent: we added §aNext:§r to EN (2 §) and §aДалее:§r to RU (2 §) — balanced

# =========================================================================
# SAVE FILES
# =========================================================================
print(f"\nTotal edited keys: {len(edited_keys)}")
print(f"Edited: {sorted(edited_keys)}")

# Verify key counts unchanged
assert len(en) == 377, f"EN key count changed: {len(en)}"
assert len(ru) == 377, f"RU key count changed: {len(ru)}"

with open(EN_PATH, 'w', encoding='utf-8') as f:
    json.dump(en, f, indent=2, ensure_ascii=False, sort_keys=True)
    f.write('\n')

with open(RU_PATH, 'w', encoding='utf-8') as f:
    json.dump(ru, f, indent=2, ensure_ascii=False, sort_keys=True)
    f.write('\n')

print("Files saved successfully.")
