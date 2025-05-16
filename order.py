import discord
from discord import app_commands
from discord.ext import commands

class Order(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="order")
    async def order(self, interaction: discord.Interaction, design_type: str, description: str, payment_method: str, proof: discord.Attachment):
        embed = discord.Embed(title="New Design Order", color=discord.Color.blue())
        embed.add_field(name="Type", value=design_type, inline=False)
        embed.add_field(name="Description", value=description, inline=False)
        embed.add_field(name="Payment Method", value=payment_method, inline=False)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        if proof:
            embed.set_image(url=proof.url)

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Thank you! Your order has been submitted.", ephemeral=True)
