import math
import copy

spells = {
    "Magic Missile": {"cost": 53, "damage": 4, "heal": 0, "effect": None},
    "Drain": {"cost": 73, "damage": 2, "heal": 2, "effect": None},
    "Shield": {"cost": 113, "damage": 0, "heal": 0, "effect": {"armor": 7, "turns": 6}},
    "Poison": {"cost": 173, "damage": 0, "heal": 0, "effect": {"damage": 3, "turns": 6}},
    "Recharge": {"cost": 229, "damage": 0, "heal": 0, "effect": {"mana": 101, "turns": 5}},
}

def simulate(player, boss, effects, spent_mana, min_mana):
    if spent_mana >= min_mana:
        return math.inf

    player["armor"] = 0
    new_effects = {}
    for effect, timer in effects.items():
        if timer > 0:
            if "armor" in spells[effect]["effect"]:
                player["armor"] = spells[effect]["effect"]["armor"]
            if "damage" in spells[effect]["effect"]:
                boss["hp"] -= spells[effect]["effect"]["damage"]
            if "mana" in spells[effect]["effect"]:
                player["mana"] += spells[effect]["effect"]["mana"]
            if timer > 1:
                new_effects[effect] = timer - 1

    effects = new_effects

    if boss["hp"] <= 0:
        return spent_mana

    for spell, properties in spells.items():
        if properties["cost"] > player["mana"]:
            continue
        if spell in effects:
            continue

        new_player = copy.deepcopy(player)
        new_boss = copy.deepcopy(boss)
        new_effects = copy.deepcopy(effects)

        new_player["mana"] -= properties["cost"]
        new_spent_mana = spent_mana + properties["cost"]

        new_boss["hp"] -= properties["damage"]
        new_player["hp"] += properties["heal"]

        if properties["effect"]:
            new_effects[spell] = properties["effect"]["turns"]

        if new_boss["hp"] <= 0:
            min_mana = min(min_mana, new_spent_mana)
            continue

        new_player["armor"] = 0
        ongoing_effects = {}
        for effect, timer in new_effects.items():
            if timer > 0:
                if "armor" in spells[effect]["effect"]:
                    new_player["armor"] = spells[effect]["effect"]["armor"]
                if "damage" in spells[effect]["effect"]:
                    new_boss["hp"] -= spells[effect]["effect"]["damage"]
                if "mana" in spells[effect]["effect"]:
                    new_player["mana"] += spells[effect]["effect"]["mana"]
                if timer > 1:
                    ongoing_effects[effect] = timer - 1

        new_effects = ongoing_effects

        if new_boss["hp"] <= 0:
            min_mana = min(min_mana, new_spent_mana)
            continue

        damage = max(1, new_boss["damage"] - new_player["armor"])
        new_player["hp"] -= damage

        if new_player["hp"] <= 0:
            continue

        min_mana = min(min_mana, simulate(new_player, new_boss, new_effects, new_spent_mana, min_mana))

    return min_mana

player = {"hp": 50, "mana": 500, "armor": 0}
boss = {"hp": 55, "damage": 8}

min_mana = simulate(player, boss, {}, 0, math.inf)
print(f"Least mana spent to win: {min_mana}")
