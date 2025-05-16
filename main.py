import discord
from discord.ext import commands
import os
import asyncio
import threading
from aiohttp import web  # Web server for Render

# Import your cogs
from commands.moderation import Moderation
from commands.utility import Utility
from commands.order import Order
from commands.help import Help

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Register cogs
async def setup_bot():
    await bot.add_cog(Moderation(bot))
    await bot.add_cog(Utility(bot))
    await bot.add_cog(Order(bot))
    await bot.add_cog(Help(bot))

# Dummy web server to keep Render happy
async def handle(request):
    return web.Response(text="Bot is running!")

def start_web():
    app = web.Application()
    app.router.add_get("/", handle)
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port)

# Run web server in a separate thread
threading.Thread(target=start_web).start()

# Main async start
async def main():
    await setup_bot()
    await bot.start(os.environ["TOKEN"])

asyncio.run(main())
