import random

def generate_loot():
    # Define possible loot items
    loot_table = [
        'Potion of Healing',
        'Scroll of Fireball',
        'Bag of Holding',
        'Cloak of Invisibility'
    ]

    # Randomly select an item from the loot table
    chosen_loot = random.choice(loot_table)

    return chosen_loot