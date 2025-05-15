import discord
from discord.ext import commands
from discord import app_commands

class HelpReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Get help or report a problem")
    @app_commands.describe(description="Describe the issue", proof="Upload proof if available")
    async def help_command(self, interaction: discord.Interaction, description: str, proof: discord.Attachment = None):
        user = interaction.user
        report_channel = self.bot.get_channel(1372473589718188086)

        embed = discord.Embed(title="Help Request", description=description, color=discord.Color.blue())
        embed.set_author(name=f"{user}", icon_url=user.avatar.url if user.avatar else None)
        embed.set_footer(text=f"User ID: {user.id}")

        if report_channel:
            await report_channel.send(embed=embed)
            if proof:
                await report_channel.send(file=await proof.to_file())

        await interaction.response.send_message("Your help request has been submitted!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpReport(bot))