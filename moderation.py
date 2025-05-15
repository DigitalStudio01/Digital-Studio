import discord
from discord.ext import commands

warnings = {}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"**{member} has been banned.** Reason: {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member_name):
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if member_name in str(user):
                await ctx.guild.unban(user)
                await ctx.send(f"**{user} has been unbanned.**")
                return

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"**{member} has been kicked.** Reason: {reason}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if member.id not in warnings:
            warnings[member.id] = []
        warnings[member.id].append(reason or "No reason provided.")
        count = len(warnings[member.id])
        await ctx.send(f"**{member} has been warned.** Warning count: {count}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unwarn(self, ctx, member: discord.Member):
        if member.id in warnings and warnings[member.id]:
            warnings[member.id].pop()
            await ctx.send(f"**{member}'s last warning has been removed.** Remaining: {len(warnings[member.id])}")
        else:
            await ctx.send(f"**{member} has no warnings.**")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, channel: discord.TextChannel, *, message):
        await channel.send(f"**Announcement:** {message}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False, speak=False)
        await member.add_roles(mute_role)
        await ctx.send(f"**{member.mention} has been muted.**")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"**{member.mention} has been unmuted.**")
        else:
            await ctx.send("**User is not muted.**")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"**Cleared {amount} messages.**", delete_after=3)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        new_channel = await channel.clone(reason="Nuked")
        await channel.delete()
        await new_channel.send("**This channel has been nuked!**")

async def setup(bot):
    await bot.add_cog(Moderation(bot))