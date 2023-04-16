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


@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')

# Add a new command to interact with the looting system:
@bot.command(name='loot')
async def get_looted_items(ctx):
    message = await ctx.send('How many items were found?')

    try:
        # Wait for user's response.
        msg = await bot.wait_for(
            'message',
            check=lambda message: message.author == ctx.author,
            timeout=30  # Timeout after 30 seconds if no reply is received.
        )

        # Parse and validate user input as an integer.
        num_players = int(msg.content)

        if num_players < 1:
            raise ValueError("Invalid number of items")

        items_list = []

        for _ in range(num_players):
            item = generate_loot()
            items_list.append(item)

        looted_items_str = ', '.join(items_list)

        await ctx.send(f'Your party found: {looted_items_str}')

    except ValueError as e:
        await ctx.send(str(e))
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)
