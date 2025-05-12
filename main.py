import discord
from discord.ext import commands
import asyncio
import os

from order import OrderBot        # Contains /order and /status
from help import HelpReport       # Contains /help
from keep_alive import keep_alive  # Added this line

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Globally synced {len(synced)} command(s)")

        guild = discord.Object(id=1371360669340930138)
        synced_guild = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced_guild)} command(s) to guild {guild.id}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def setup_bot():
    await bot.add_cog(OrderBot(bot))     # /order and /status are inside this cog
    await bot.add_cog(HelpReport(bot))   # /help command

async def main():
    keep_alive()  # Keeps the bot alive 24/7
    await setup_bot()
    await bot.start(os.environ["TOKEN"])

asyncio.run(main())
