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
print(f"Fix 1 applied to {LAVA_KEY}")
print(f"  EN § count: {en[LAVA_KEY].count('§')}, RU § count: {ru[LAVA_KEY].count('§')}")

# =========================================================================
# FIX 2 — Replace "Gear Crafting Table" → "Gear Smithing Table" + fix center slot
# Quest: Stone Age idx=4 → qid=096d3b92e663cb71
# =========================================================================
SILENT_KEY = 'ftbquests.quest.096d3b92e663cb71.desc'

# EN: replace "Gear Crafting Table" and fix the center-slot description
en[SILENT_KEY] = (
    "Open the §eSilent's Gear§r tool workbench (§6Gear Smithing Table§r). "
    "Open the §eGear Smithing Table§r and slot your existing tool plus the new material to swap it in. "
    "Replace the §6head material§r with §eCobblestone§r, §eAndesite§r, §eDiorite§r, or §eGranite§r.\n\n"
    "Stone-tier materials significantly improve §6mining speed§r and §6durability§r over Colorless/Wood tier.\n\n"
    "§aTip:§r Each stone type has slightly different stats — experiment! §eAndesite§r and §eGranite§r often have better durability bonuses.\n\n"
    "§aResult:§r Upgraded tools let you mine faster, progress through the Stone Age, and prepare for §6Metal Age§r materials ahead."
)

# RU: same replacements
ru[SILENT_KEY] = (
    "Открой §eверстак Silent's Gear§r (§6Gear Smithing Table§r). "
    "Открой §eGear Smithing Table§r и вставь свой инструмент вместе с новым материалом, чтобы заменить его. "
    "Замени §6материал головки§r на §eБулыжник§r, §eАндезит§r, §eДиорит§r или §eГранит§r.\n\n"
    "Каменный материал значительно улучшает §6скорость добычи§r и §6прочность§r по сравнению с бесцветным/деревянным уровнем.\n\n"
    "§aСовет:§r Каждый тип камня даёт немного разные характеристики — экспериментируй! §eАндезит§r и §eГранит§r часто дают лучший бонус к прочности.\n\n"
    "§aРезультат:§r Прокачанные инструменты ускоряют добычу и готовят тебя к материалам §6Металлического Века§r."
)

edited_keys.add(SILENT_KEY)
print(f"Fix 2 applied to {SILENT_KEY}")
print(f"  EN § count: {en[SILENT_KEY].count('§')}, RU § count: {ru[SILENT_KEY].count('§')}")

# =========================================================================
# FIX 3 — "Sappling" → "Sapling" (barrel dirt quest)
# =========================================================================
BARREL_KEY = 'ftbquests.quest.bce0485ccf92da1a.desc'
old_en_barrel = en[BARREL_KEY]
en[BARREL_KEY] = en[BARREL_KEY].replace('Sappling', 'Sapling')
if en[BARREL_KEY] != old_en_barrel:
    edited_keys.add(BARREL_KEY)
    print(f"Fix 3 applied (EN): fixed Sappling→Sapling in {BARREL_KEY}")

# RU doesn't have 'Sappling' (it uses Cyrillic), but scan all values to be safe
for k in list(en.keys()):
    old = en[k]
    en[k] = en[k].replace('Sappling', 'Sapling')
    if en[k] != old:
        edited_keys.add(k)
        print(f"Fix 3 extra EN: {k}")

for k in list(ru.keys()):
    old = ru[k]
    ru[k] = ru[k].replace('Sappling', 'Sapling')
    if ru[k] != old:
        edited_keys.add(k)
        print(f"Fix 3 extra RU: {k}")

# =========================================================================
# FIX 4 — Balance § color codes between EN and RU for the 4 specific keys
# =========================================================================

# Key 1: ftbquests.quest.3f5aa9a592917d94.desc (Automate Cobblestone)
# EN=16, RU=12 → RU needs 4 more § codes
# EN has: §e§r §6§r §6§r §e§r §e§r §e§r §a§r §e§r §e§r §e§r §a§r §e§r (lots of emphasis)
# RU current: missing §e§r on "Block Placer" and "Block Breaker" (they share one pair) and missing "§e§r" on "Drills"
# Let's look at specific differences:
# EN: "§eBlock Placer§r + §eBlock Breaker§r" - 4 § codes in this phrase
# RU: "§eBlock Placer + Block Breaker§r" - 2 § codes (missing pair around Block Breaker)
# EN: "§eDrills§r" - 2 § codes; RU: "Бурилки" with no emphasis - 2 missing

CОБBLESTONE_KEY = 'ftbquests.quest.3f5aa9a592917d94.desc'
# EN=16, RU=12, need to add 4 §-codes to RU
# Current RU:
# "§eГенератор Булыжника§r" (2) "§6Block Breaker§r" (2) "§6Mechanical Drill§r" (2) = 6
# "§eBlock Placer + Block Breaker§r" (2 - missing the inner split) "из Industrial Foregoing"
# "§aСовет:§r" (2) "§aРезультат:§r" (2) = 4
# Total RU = 12
# EN has additionally: §e§r around "Block Placer" + §e§r around "Block Breaker" in tip (2+2=4 extra)
# Wait let me recount EN carefully:
# EN: §e(1)Cobblestone Generator§r(2) §6(3)Block Breaker§r(4) §6(5)Mechanical Drill§r(6)
#     §a(7)Tip:§r(8) §e(9)Block Placer§r(10) §e(11)Block Breaker§r(12) §e(13)Drills§r(14)
#     §a(15)Result:§r(16)
# RU: §e(1)Генератор Булыжника§r(2) §6(3)Block Breaker§r(4) §6(5)Mechanical Drill§r(6)
#     §a(7)Совет:§r(8) §e(9)Block Placer + Block Breaker§r(10) [missing §e Drills split]
#     §a(11)Результат:§r(12)
# So RU is missing:
# - split §e§r around "Block Breaker" in the tip (add §e...§r): §eBlock Placer§r + §eBlock Breaker§r
# - §e§r around "Бурилки" (Drills)
# That's 4 more § codes

ru[CОБBLESTONE_KEY] = (
    "Ручное производство Булыжника из Пепла — слишком медленно. Время автоматизировать!\n\n"
    "Классический метод: построй §eГенератор Булыжника§r — расположи источники Лавы и Воды по разные стороны от ямки. "
    "В ямке формируется Булыжник; ломай его §6Block Breaker§r или §6Mechanical Drill§r (мод Create).\n\n"
    "§aСовет:§r Связка §eBlock Placer§r + §eBlock Breaker§r из Industrial Foregoing отлично работает. "
    "§eБурилки§r мода Create дают более высокую производительность.\n\n"
    "§aРезультат:§r Бесконечный Булыжник → Камень, Гравий, Песок, Лава. Основа всей будущей переработки ресурсов!"
)
edited_keys.add(CОБBLESTONE_KEY)
print(f"Fix 4 applied to {CОБBLESTONE_KEY}")
print(f"  EN § count: {en[CОБBLESTONE_KEY].count('§')}, RU § count: {ru[CОБBLESTONE_KEY].count('§')}")

# Key 2: ftbquests.quest.4e4cf2d27ba2d029.desc (Obtain Obsidian)
# EN=16, RU=14 → RU needs 2 more
# EN: §6(1)Water source block§r(2) §6(3)Lava source block§r(4) §e(5)Obsidian§r(6) §6(7)Diamond Pickaxe§r(8)
#     §a(9)Tip:§r(10) §e(11)Silent's Gear Diamond Pickaxe§r(12) §6(13)Enchanted Golden Apple§r(14) §6(15)...§r(16)? 
# wait let me recount EN:
# §6Water source block§r §6Lava source block§r §eObsidian§r = 6
# §6Diamond Pickaxe§r = 2 → total 8
# §aTip:§r = 2 → total 10
# §eSilent's Gear Diamond Pickaxe§r = 2 → total 12
# §6Enchanted Golden Apple§r = 2 → total 14 -- wait that's 14 not 16
# Let me look more carefully at EN text again:
# "§aResult:§r Obsidian is needed..." = 2 more → total 16
# 
# RU: §6источник Воды§r §6источника Лавы§r §eОбсидиан§r = 6
#     §6Алмазной Киркой§r = 2 → 8
#     §aСовет:§r = 2 → 10
#     §eАлмазную Кирку Silent's Gear§r = 2 → 12
#     §aРезультат:§r = 2 → 14
# Missing: §6Enchanted Golden Apple§r equivalent in RU (EN has "§6Enchanted Golden Apple§r method")
# EN tip: "§eSilent's Gear Diamond Pickaxe§r to mine Obsidian — or use the §6Enchanted Golden Apple§r method"
# RU tip: "§eАлмазную Кирку Silent's Gear§r или ускорить добычу алмазов через просеивание."
# RU is missing the §6Enchanted Golden Apple§r reference → add it

OBSIDIAN_KEY = 'ftbquests.quest.4e4cf2d27ba2d029.desc'
ru[OBSIDIAN_KEY] = (
    "Классическая ванильная механика: §6источник Воды§r поверх §6источника Лавы§r создаёт §eОбсидиан§r.\n\n"
    "Положи источник Лавы в ямку, затем вылей или поставь Воду сверху. Лава превратится в Обсидиан — добывай его §6Алмазной Киркой§r (или лучше).\n\n"
    "§aСовет:§r Можно скрафтить §eАлмазную Кирку Silent's Gear§r или ускорить добычу алмазов через просеивание с §6Зачарованным Золотым Яблоком§r.\n\n"
    "§aРезультат:§r Обсидиан нужен для Портала в Незер, Стола Зачарования, Эндер-сундука и многих важных mid-game рецептов."
)
edited_keys.add(OBSIDIAN_KEY)
print(f"Fix 4 applied to {OBSIDIAN_KEY}")
print(f"  EN § count: {en[OBSIDIAN_KEY].count('§')}, RU § count: {ru[OBSIDIAN_KEY].count('§')}")

# Key 3: ftbquests.quest.a692fda4a82cbcb1.desc (Silkworm String)
# EN=14, RU=12 → RU needs 2 more
# EN: §e(1)Silkworms§r(2) §6(3)Leaf block§r(4) §e(5)infest§r(6) §6(7)String§r(8)
#     §a(9)Tip:§r(10) §e(11)Sickle§r(12) §a(13)Result:§r(14)
# RU: §e(1)Шелкопряда§r(2) §6(3)Листовому блоку§r(4) §6(5)Нить§r(6)
#     §a(7)Совет:§r(8) §e(9)Серп§r(10) §a(11)Результат:§r(12)
# Missing: §e§r around "infest" verb (EN has "§einfest§r it") → add §eзаразятся§r? 
# But Russian sentence structure differs. Need to add 2 § codes.
# Best approach: add §e§r emphasis on the "infest" action in Russian

SILKWORM_KEY = 'ftbquests.quest.a692fda4a82cbcb1.desc'
ru[SILKWORM_KEY] = (
    "Найди §eШелкопряда§r (Silkworm) — он выпадает из листьев при ломке. "
    "Кликни ПКМ по §6Листовому блоку§r с Шелкопрядом в руке — листья §eзаразятся§r!\n\n"
    "Заражение постепенно распространяется на соседние листья. Когда лист полностью заражён (белая паутина), ломка даёт §6Нить§r (String).\n\n"
    "§aСовет:§r Дай заражению распространиться на соседние листья перед сбором. Используй §eСерп§r для быстрой массовой уборки!\n\n"
    "§aРезультат:§r Нить → Шерсть → куча рецептов: кровати, ковры, зачарование и многое другое."
)
edited_keys.add(SILKWORM_KEY)
print(f"Fix 4 applied to {SILKWORM_KEY}")
print(f"  EN § count: {en[SILKWORM_KEY].count('§')}, RU § count: {ru[SILKWORM_KEY].count('§')}")

# Key 4: ftbquests.quest.bb96e110dd945484.desc (Colored Crafting Tables)
# EN=16, RU=14 → RU needs 2 more
# EN: §e(1)16 colors§r(2) §6(3)Color Crafting Table§r(4) §6(5)4 Colored Planks§r(6)
#     §e(7)Colored Planks§r(8) §6(9)Dye§r(10) §6(11)Colorless Planks§r(12)
#     §a(13)Tip:§r(14) §6(15)Chromatic Age§r(16)
# RU: §e(1)16 цветов§r(2) §6(3)Цветной Верстак§r(4) §6(5)4 Цветных Доски§r(6)
#     §e(7)Цветные Доски§r(8) §6(9)Бесцветных Досок§r(10)
#     §a(11)Совет:§r(12) §6(13)Chromatic Age§r(14)
# Missing: §6Dye§r equivalent in RU (EN "using §6Dye§r on §6Colorless Planks§r")
# RU says "покраской §6Бесцветных Досок§r краской" — "краской" has no emphasis

COLORED_KEY = 'ftbquests.quest.bb96e110dd945484.desc'
ru[COLORED_KEY] = (
    "Для каждого из §e16 цветов§r существует свой §6Цветной Верстак§r. Для крафта нужны §64 Цветных Доски§r одного цвета в сетке 2×2.\n\n"
    "§eЦветные Доски§r получаются покраской §6Бесцветных Досок§r краской §6Краситель§r, или из цветных деревьев. Каждый верстак открывает рецепты своего цвета.\n\n"
    "§aСовет:§r Собери несколько разных цветных верстаков — это откроет больше рецептов в начале игры.\n\n"
    "Больше цветов = больше возможностей! Загляни в главу §6Chromatic Age§r за советами по получению краски."
)
edited_keys.add(COLORED_KEY)
print(f"Fix 4 applied to {COLORED_KEY}")
print(f"  EN § count: {en[COLORED_KEY].count('§')}, RU § count: {ru[COLORED_KEY].count('§')}")

# =========================================================================
# FIX 5 — Add §aNext:§r lines to 5 quests
# =========================================================================

def has_next_line(text):
    return '§aNext:§r' in text or '§aResult:§r' in text

# Quest next titles
next_quests = {
    # Age of Discovery idx=1 → next is idx=2: "Use a Barrel to create Dirt"
    '7c8df3e097e319fc': 'Use a Barrel to create Dirt',
    # Stone Age idx=1 → next is idx=2: "Obtain Obsidian"
    'b81aea269d8e19e4': None,  # Already has §aResult:§r mentioning Obsidian — check below
    # Chromatic Age idx=2 → next is idx=3: "Click on a Color Leaves block with Dye to create Flowers"
    '7646a7b0d274cd26': None,  # Already has §aResult:§r — check below
    # Age of Discovery idx=2 → next is idx=3: "Eat Dirt!"
    'bce0485ccf92da1a': 'Eat Dirt!',
    # Stone Age idx=4 → next age: Chromatic Age idx=1
    '096d3b92e663cb71': '(Chromatic Age — Throw Dye into Water to change its color)',
}

# For Stone Age idx=1 (Make Lava) - we just rewrote it and it has §aResult:§r mentioning Obsidian ✓
# For Chromatic Age idx=2 (Dye Block) - has §aResult:§r ✓
# Age of Discovery idx=1 - check if §aResult:§r exists
AOD1_KEY = 'ftbquests.quest.7c8df3e097e319fc.desc'
print(f"\nAOD1 has next/result: {has_next_line(en[AOD1_KEY])}")
print(f"AOD1 last lines: {en[AOD1_KEY][-200:]}")

# Stone Age idx=1 - we rewrote it with §aResult:§r  
LAVA_KEY2 = 'ftbquests.quest.b81aea269d8e19e4.desc'
print(f"Lava has next/result: {has_next_line(en[LAVA_KEY2])}")

# Chromatic idx=2
CHROMA2_KEY = 'ftbquests.quest.7646a7b0d274cd26.desc'
print(f"Chroma2 has next/result: {has_next_line(en[CHROMA2_KEY])}")

# AOD idx=2 (Barrel)
BARREL_KEY2 = 'ftbquests.quest.bce0485ccf92da1a.desc'
print(f"Barrel has next/result: {has_next_line(en[BARREL_KEY2])}")

# Stone Age idx=4 (Silent's Gear)
SILENT_KEY2 = '096d3b92e663cb71'
print(f"Silent has next/result: {has_next_line(en[f'ftbquests.quest.{SILENT_KEY2}.desc'])}")

EOF
