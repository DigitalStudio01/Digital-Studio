
import os
import discord
from discord.ext import commands
import asyncio

from order import OrderBot
from help import HelpReport
from admin import AdminCommands

try:
    from keep_alive import keep_alive
    use_keep_alive = True
except ImportError:
    use_keep_alive = False

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Globally synced {len(synced)} command(s)")
    except Exception as e:
        print(f"[!] Failed to sync commands: {e}")

async def setup_bot():
    await bot.add_cog(OrderBot(bot))
    await bot.add_cog(HelpReport(bot))
    await bot.add_cog(AdminCommands(bot))

async def main():
    if use_keep_alive:
        keep_alive()
    await setup_bot()
    await bot.start(os.environ["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())
