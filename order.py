
import discord
from discord.ext import commands
from discord import app_commands

class OrderBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="order", description="Place a design order")
    @app_commands.describe(
        design_type="Select the type of design you want",
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
    async def order(
        self,
        interaction: discord.Interaction,
        design_type: app_commands.Choice[str],
        design_details: str,
        payment_method: app_commands.Choice[str],
        payment_proof: discord.Attachment
    ):
        user = interaction.user
        report_channel = self.bot.get_channel(1372552386240839752)

        try:
            await user.send(
                "**Your Order Has Been Placed!**\n"
                "Thank you for ordering with us! Your design request has been sent to our team.\n"
                "**Stay awesome and creative!**"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Couldn't DM you! Please check your privacy settings.",
                ephemeral=True
            )
            return

        embed = discord.Embed(title="New Design Order", color=discord.Color.green())
        embed.add_field(name="Customer", value=f"{user} ({user.id})", inline=False)
        embed.add_field(name="Design Type", value=design_type.value, inline=False)
        embed.add_field(name="Design Details", value=design_details, inline=False)
        embed.add_field(name="Payment Method", value=payment_method.value, inline=False)

        await report_channel.send(embed=embed)
        await report_channel.send("Payment Proof:", file=await payment_proof.to_file())

        await interaction.response.send_message(
            "**Thank you!** Your order has been placed and sent to our team.",
            ephemeral=True
        )

    @app_commands.command(name="status", description="Live service availability of our designers")
    async def status(self, interaction: discord.Interaction):
        service_available = True

        if service_available:
            msg = "**Design Service Status: ONLINE** \n"
            emoji = "🟢"
        else:
            msg = "**Design Service Status: OFFLINE** \n"
            emoji = "🔴"

        await interaction.response.send_message(f"{emoji} {msg}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(OrderBot(bot))
