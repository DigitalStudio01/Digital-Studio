import discord
from discord.ext import commands
from discord import app_commands
import os

from commands.moderation import Moderation
from commands.utility import Utility
from commands.order import Order
from commands.help import Help

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.add_cog(Moderation(bot))
bot.add_cog(Utility(bot))
bot.add_cog(Order(bot))
bot.add_cog(Help(bot))

bot.run("YOUR_BOT_TOKEN")
