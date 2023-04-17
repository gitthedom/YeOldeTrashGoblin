import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Import your loot module and its functions here:
from modules.loot import generate_loot

load_dotenv()

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')


@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')


# Add a new command to interact with the looting system:
@bot.command(name='loot')
async def get_looted_items(ctx: commands.Context):
    await ctx.send('How many items were found?')

    try:
        # Wait for user's response.
        msg_items = await bot.wait_for(
            'message',
            check=lambda message: message.author == ctx.author,
            timeout=30  # Timeout after 30 seconds if no reply is received.
        )

        await ctx.send('What was the rank of the encounter?')

        msg_rank = await bot.wait_for(
            'message',
            check=lambda message: message.author == ctx.author,
            timeout=30  # Timeout after 30 seconds if no reply is received.
        )

        # Parse and validate user input as an integer.
        num_items = int(msg_items.content)
        num_rank = int(msg_rank.content)

        if num_items < 1:
            raise ValueError("Invalid number of items")

        if num_rank < 1:
            raise ValueError("Invalid number of items")

        items_list = []

        items = generate_loot(num_items, num_rank)

        await ctx.send(embed=items)

    except ValueError as e:
        await ctx.send(str(e))
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")


bot.run(TOKEN)
