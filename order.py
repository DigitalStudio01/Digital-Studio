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
        owner = await self.bot.fetch_user(1371360049074798686)  # Your Discord user ID

        # DM to customer
        try:
            await user.send(
                "**Your Order Has Been Placed!**\n"
                "Thank you for ordering with us! Your design request has been sent to **@designerparth_**.\n"
                "We will share your delivery time soon.\n\n"
                "**Stay awesome and creative!**"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Couldn't DM you! Please check your privacy settings.",
                ephemeral=True
            )
            return

        # Embed to bot owner
        embed = discord.Embed(
            title="New Design Order",
            color=discord.Color.green()
        )
        embed.add_field(name="Customer", value=f"{user} ({user.id})", inline=False)
        embed.add_field(name="Design Type", value=design_type.value, inline=False)
        embed.add_field(name="Design Details", value=design_details, inline=False)
        embed.add_field(name="Payment Method", value=payment_method.value, inline=False)

        await owner.send(embed=embed)
        await owner.send("Payment Proof:", file=await payment_proof.to_file())

        # Confirm to user
        await interaction.response.send_message("Order received! Please check your DM.", ephemeral=True)

    @app_commands.command(name="status", description="Check if design service is currently available")
    async def status(self, interaction: discord.Interaction):
        service_available = True  # Change this to False when you're unavailable

        if service_available:
            await interaction.response.send_message(
                "**Our design service is currently AVAILABLE!**\n"
                "Feel free to place your order anytime!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "**Our design service is currently UNAVAILABLE.**\n"
                "Please check back later or contact @designerparth_.",
                ephemeral=True
            )

# Required for loading this cog
async def setup(bot):
    await bot.add_cog(OrderBot(bot))
