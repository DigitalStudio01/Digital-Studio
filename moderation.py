import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.mention} has been banned. Reason: {reason}", ephemeral=False)

    @app_commands.command(name="unban")
    async def unban(self, interaction: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"{user} has been unbanned.", ephemeral=False)

    @app_commands.command(name="kick")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} has been kicked. Reason: {reason}", ephemeral=False)

    @app_commands.command(name="warn")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.response.send_message(f"{member.mention} has been warned. Reason: {reason}", ephemeral=False)

    @app_commands.command(name="unwarn")
    async def unwarn(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{member.mention}'s warning has been removed.", ephemeral=False)

    @app_commands.command(name="mute")
    async def mute(self, interaction: discord.Interaction, member: discord.Member):
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        for channel in interaction.guild.text_channels:
            await channel.set_permissions(member, overwrite=overwrite)
        await interaction.response.send_message(f"{member.mention} has been muted.", ephemeral=False)

    @app_commands.command(name="unmute")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        for channel in interaction.guild.text_channels:
            await channel.set_permissions(member, overwrite=None)
        await interaction.response.send_message(f"{member.mention} has been unmuted.", ephemeral=False)
