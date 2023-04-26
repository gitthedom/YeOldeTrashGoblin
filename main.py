import discord
import os # default module
from dotenv import load_dotenv
from discord.commands import Option

from modules.loot import generate_loot

load_dotenv() # load all the variables from the env file
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


@bot.slash_command(name="loot", description="Randomly dropped loot")
async def get_looted_items(ctx,
                           item_count: Option(int, "Number of items found", required=True),
                           rank_number: Option(int, "Rank Encounter Number (1-6)", required=True)):
    try:
        num_items = int(item_count) # int(msg_items.content)
        num_rank = int(rank_number) # int(msg_rank.content)

        if num_items < 1:
            raise ValueError("Invalid number of items")

        if num_rank < 1:
            raise ValueError("Invalid number of items")

        items_list = []

        items = generate_loot(num_items, num_rank)

        await ctx.respond(embed=items)

    except ValueError as e:
        await ctx.respond(str(e))
    except Exception as e:
        await ctx.respond(f"Error: {str(e)}")

bot.run(os.getenv('DISCORD_TOKEN')) # run the bot with the token
