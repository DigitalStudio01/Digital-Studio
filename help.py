
import discord
from discord.ext import commands
from discord import app_commands

class HelpReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Report an issue or request assistance")
    @app_commands.describe(
        description="Describe your issue or question",
        proof="Attach an image as proof if needed"
    )
    async def help_command(self, interaction: discord.Interaction, description: str, proof: discord.Attachment = None):
        user = interaction.user
        report_channel = self.bot.get_channel(1372473589718188086)

        if not report_channel:
            await interaction.response.send_message("Couldn't find the report channel.", ephemeral=True)
            return

        embed = discord.Embed(
            title="New Help Request",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_author(name=f"{user}", icon_url=user.avatar.url if user.avatar else None)
        embed.set_footer(text=f"User ID: {user.id}")

        await report_channel.send(embed=embed)

        if proof:
            await report_channel.send("Attached proof:", file=await proof.to_file())

        await interaction.response.send_message("Your help request has been submitted.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpReport(bot))
