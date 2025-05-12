import discord
from discord.ext import commands
from discord import app_commands

class HelpReport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Report an issue or ask for help")
    @app_commands.describe(
        description="Tell us about your problem or how we can help",
        proof="Upload a screenshot or image if you have one"
    )
    async def help_command(self, interaction: discord.Interaction, description: str, proof: discord.Attachment = None):
        user = interaction.user
        channel_id = 1371367408308064448  # Help report channel ID
        channel = self.bot.get_channel(channel_id)

        if not channel:
            await interaction.response.send_message("Couldn't find the report channel.", ephemeral=True)
            return

        embed = discord.Embed(
            title="New Help Request",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_author(name=f"{user}", icon_url=user.avatar.url if user.avatar else None)
        embed.set_footer(text=f"User ID: {user.id}")

        await channel.send(embed=embed)

        if proof:
            file = await proof.to_file()
            await channel.send("Attached proof:", file=file)

        await interaction.response.send_message("Your help request has been submitted.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpReport(bot))
