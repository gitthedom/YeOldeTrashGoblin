import random
import discord
from Database.database_handler import DatabaseHandler


def generate_loot(number_of_items, encounter_rank):
    handler = DatabaseHandler()

    weighted_rank_table = {
        1: [("common", 0.6), ("uncommon", 0.4)],
        2: [("common", 0.5), ("uncommon", 0.45), ("rare", 0.05)],
        3: [("common", 0.4), ("uncommon", 0.5), ("rare", 0.1)],
        4: [("common", 0.25), ("uncommon", 0.55), ("rare", 0.15), ("very rare", 0.05)],
        5: [("uncommon", 0.7), ("rare", 0.20), ("very rare", 0.1)],
        6: [("uncommon", 0.5), ("rare", 0.3), ("very rare", 0.15), ("legendary", 0.05)]
    }

    chosen_rank_weight = weighted_rank_table.get(encounter_rank)

    rarities = [t for t, w in chosen_rank_weight]
    weights = [w for t, w in chosen_rank_weight]

    embed = discord.Embed(
        title="Collect your prize",
        description="Items looted from the slain bodies of your enemies!",
        color=discord.Color.dark_red())

    for _ in range(number_of_items):
        selected_rarity = random.choices(rarities, weights=weights, k=1)[0]
        loot_table = handler.fetch_data('game_items', ['name'], 'rarity=?', (selected_rarity,))

        selected_item_original_name = random.choice(loot_table)

        rarity_message = selected_rarity.capitalize()

        embed.add_field(name=f"{selected_item_original_name[0]}", value=f"{rarity_message}", inline=False)

    return embed
