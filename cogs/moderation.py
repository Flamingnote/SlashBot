import discord
from discord.ext import commands
from discord import Option
from discord.ext.commands import MissingPermissions
from datetime import timedelta
import datetime
import asyncio

gid=[]

class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids = gid, name = "ban", description = "Bans a member")
    @commands.has_permissions(ban_members = True, administrator = True)
    async def ban(self, ctx, member: Option(discord.Member, description = "Who do you want to ban?"), reason: Option(str, description = "Why?", required = False)):# type: ignore
            if member.id == ctx.author.id: #checks to see if they're the same
                await ctx.respond("BRUH! You can't ban yourself!")
            elif member.guild_permissions.administrator:
                await ctx.respond("Stop trying to ban an admin! :rolling_eyes:")
            else:
                if reason == None:
                    await member.ban(reason = reason)
                    await ctx.respond(f'<@{member.id}> has been banned from {ctx.guild}\nReason: {reason}')

    @commands.slash_command(guild_ids = gid, name = "kick", description = "Kicks a member")
    @commands.has_permissions(kick_members = True, administrator = True)
    async def kick(self, ctx, member: Option(discord.Member, description = "Who do you want to kick?"), reason: Option(str, description = "Why?", required = False)):# type: ignore
        if member.id == ctx.author.id: #checks to see if they're the same
            await ctx.respond("BRUH! You can't kick yourself!")
        elif member.guild_permissions.administrator:
            await ctx.respond("Stop trying to kick an admin! :rolling_eyes:")
        else:
            if reason == None:
                reason = f"None provided by {ctx.author}"
            await member.kick(reason = reason)
            await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> has been kicked from this server!\n\nReason: {reason}")


    @commands.slash_command(guild_ids = gid, name = "bans", description = "Get a list of members who are banned from this server!")
    @commands.has_permissions(ban_members = True)
    async def bans(self, ctx):
        bans = ctx.guild.bans()
        embed = discord.Embed(title = f"List of Bans in {ctx.guild}", timestamp = datetime.datetime.now(), color = discord.Colour.red())
        async for entry in bans:
            if len(embed.fields) >= 25:
                break
            if len(embed) > 5900:
                embed.add_field(name = "Too many bans to list")# type: ignore
            else:
                embed.add_field(name = f"Ban", value = f"Username: {entry.user.name}#{entry.user.discriminator}\nReason: {entry.reason}\nUser ID: {entry.user.id}\nIs Bot: {entry.user.bot}", inline = False)
                await ctx.respond(embed = embed)

    @commands.slash_command(guild_ids = gid, name = "unban", description = "Unbans a member")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, id: Option(str,description= 'User id', required = True)):# type: ignore
        await ctx.defer()
        member = await self.client.fetch_user(id)
        await ctx.guild.unban(member)
        await ctx.respond(f"I have unbanned {member.mention}.")

    @commands.slash_command(guild_ids = gid, name = 'timeout', description = "mutes/timeouts a member")
    @commands.has_permissions(moderate_members = True)
    async def timeout(self, ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)):# type: ignore #setting each value with a default value of 0 reduces a lot of the code
        if member.id == ctx.author.id:
            await ctx.respond("You can't timeout yourself!")
            return
        if member.guild_permissions.moderate_members:
            await ctx.respond("You can't do this, this person is a moderator!")
            return
        duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
        if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
            await ctx.respond("I can't mute someone for more than 28 days!", ephemeral = True) #responds, but only the author can see the response
            return
        if reason == None:
            await member.timeout_for(duration)
            await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
        else:
            await member.timeout_for(duration, reason = reason)
            await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

    @commands.slash_command(guild_ids = gid, name = 'unmute', description = "unmutes/untimeouts a member")
    @commands.has_permissions(moderate_members = True)
    async def unmute(self, ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):# type: ignore
        if reason == None:
            await member.remove_timeout()
            await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
        else:
            await member.remove_timeout(reason = reason)
            await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")

    @commands.slash_command(guid_ids=gid,name='clear', description='Clear the messages')
    async def clear(self, ctx, amount: Option(int, max_value= 100, description='Amount')): # type: ignore
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f'`{amount}` messages have been cleared.', ephemeral=True)

def setup(client): # this is called by Pycord to setup the cog
    client.add_cog(moderation(client)) # add the cog to the bot