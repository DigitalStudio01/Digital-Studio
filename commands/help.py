import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction, description: str, screenshot: discord.Attachment = None):
        embed = discord.Embed(title="Help Request", description=description, color=discord.Color.orange())
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        if screenshot:
            embed.set_image(url=screenshot.url)

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Thanks! Your help request was sent.", ephemeral=True)
