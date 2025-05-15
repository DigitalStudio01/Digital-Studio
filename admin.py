
import discord
from discord.ext import commands
from discord import app_commands

warnings = {}

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @app_commands.command(name="ban", description="Ban a user from the server")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        await user.ban(reason=reason)
        await interaction.response.send_message(f"**{user}** has been banned. Reason: {reason}", ephemeral=True)

    @commands.has_permissions(administrator=True)
    @app_commands.command(name="unban", description="Unban a user by ID")
    async def unban(self, interaction: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"**{user}** has been unbanned.", ephemeral=True)

    @commands.has_permissions(administrator=True)
    @app_commands.command(name="kick", description="Kick a user from the server")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        await user.kick(reason=reason)
        await interaction.response.send_message(f"**{user}** has been kicked. Reason: {reason}", ephemeral=True)

    @commands.has_permissions(administrator=True)
    @app_commands.command(name="warn", description="Warn a user")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        user_warnings = warnings.get(user.id, 0) + 1
        warnings[user.id] = user_warnings
        await interaction.response.send_message(f"**{user}** has been warned. Reason: {reason}\nTotal warnings: {user_warnings}", ephemeral=True)

    @commands.has_permissions(administrator=True)
    @app_commands.command(name="unwarn", description="Remove a warning from a user")
    async def unwarn(self, interaction: discord.Interaction, user: discord.Member):
        user_warnings = max(warnings.get(user.id, 0) - 1, 0)
        warnings[user.id] = user_warnings
        await interaction.response.send_message(f"One warning removed from **{user}**. Total warnings now: {user_warnings}", ephemeral=True)

    @commands.has_permissions(administrator=True)
    @app_commands.command(name="announce", description="Send an announcement in a specific channel")
    async def announce(self, interaction: discord.Interaction, channel: discord.TextChannel, message: str):
        await channel.send(f"**Announcement:** {message}")
        await interaction.response.send_message("Announcement sent.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
