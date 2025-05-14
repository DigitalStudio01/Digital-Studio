import os
import discord
from discord.ext import commands
import asyncio

from order import OrderBot       # /order and /status slash commands
from help import HelpReport      # /help slash command

# If you're using keep_alive (like with Replit or UptimeRobot)
try:
    from keep_alive import keep_alive
    use_keep_alive = True
except ImportError:
    use_keep_alive = False

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    try:
        # Global slash command sync
        synced = await bot.tree.sync()
        print(f"Globally synced {len(synced)} command(s)")

        # Optional: Guild-specific sync for faster command updates
        guild_id = os.getenv("GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            synced_guild = await bot.tree.sync(guild=guild)
            print(f"Synced {len(synced_guild)} command(s) to guild {guild.id}")
    except Exception as e:
        print(f"[!] Failed to sync commands: {e}")

async def setup_bot():
    await bot.add_cog(OrderBot(bot))
    await bot.add_cog(HelpReport(bot))

async def main():
    if use_keep_alive:
        keep_alive()

    await setup_bot()
    await bot.start(os.environ["TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())
