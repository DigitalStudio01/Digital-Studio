import discord
from discord.ext import commands
from discord import app_commands

class OrderBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="order", description="Place a design order")
    @app_commands.describe(
        design_type="Type of design you want",
        design_details="Describe your design idea",
        payment_method="Choose your payment method",
        payment_proof="Upload proof of payment"
    )
    @app_commands.choices(
        design_type=[
            app_commands.Choice(name="Logo", value="Logo"),
            app_commands.Choice(name="Banner", value="Banner"),
            app_commands.Choice(name="Thumbnail", value="Thumbnail"),
            app_commands.Choice(name="Edit", value="Edit"),
            app_commands.Choice(name="Other", value="Other")
        ],
        payment_method=[
            app_commands.Choice(name="G-Pay", value="G-Pay"),
            app_commands.Choice(name="PhonePay", value="PhonePay"),
            app_commands.Choice(name="Paytm", value="Paytm"),
            app_commands.Choice(name="FamPay", value="FamPay"),
            app_commands.Choice(name="Other", value="Other"),
        ]
    )
    async def order(self, interaction: discord.Interaction, design_type: app_commands.Choice[str], design_details: str, payment_method: app_commands.Choice[str], payment_proof: discord.Attachment):
        user = interaction.user
        log_channel = self.bot.get_channel(1372552386240839752)

        embed = discord.Embed(title="New Design Order", color=discord.Color.green())
        embed.add_field(name="Customer", value=f"{user} ({user.id})", inline=False)
        embed.add_field(name="Design Type", value=design_type.value, inline=False)
        embed.add_field(name="Design Details", value=design_details, inline=False)
        embed.add_field(name="Payment Method", value=payment_method.value, inline=False)
        embed.set_footer(text="Design Order Notification")
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)

        file = await payment_proof.to_file()

        if log_channel:
            await log_channel.send(embed=embed)
            await log_channel.send(file=file)

        await user.send("**Thank you! Your order has been placed. We'll contact you soon.**")

        await interaction.response.send_message("**Thanks for your order! Check your DMs for details.**", ephemeral=True)

    @app_commands.command(name="status", description="See if design service is available")
    async def status(self, interaction: discord.Interaction):
        service_available = True
        if service_available:
            await interaction.response.send_message(
                "**Design Service Status: ONLINE**
Green Circle: We're accepting orders!",
                ephemeral=False
            )
        else:
            await interaction.response.send_message(
                "**Design Service Status: OFFLINE**
Red Circle: We are currently unavailable.",
                ephemeral=False
            )

async def setup(bot):
    await bot.add_cog(OrderBot(bot))