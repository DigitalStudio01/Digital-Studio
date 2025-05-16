import discord
from discord import app_commands
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear")
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Deleted {amount} messages.", ephemeral=False)

    @app_commands.command(name="nuke")
    async def nuke(self, interaction: discord.Interaction):
        old_channel = interaction.channel
        new_channel = await old_channel.clone()
        await old_channel.delete()
        await new_channel.send("This channel has been nuked!")
