import discord
from discord.ext import commands
from discord import Option
import random
import datetime
import json, aiohttp
import asyncio
from datetime import timedelta
from discord import DMChannel
import requests
from bs4 import BeautifulSoup
import sqlite3
from discord.ext.commands import IDConverter

gid=[]
timers = []

class fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.respond('```arm\nAn error occurred: {}\n```'.format(str(error)))# type: ignore

    @commands.slash_command(guid_ids=gid, name = 'ping', description= "Bot's ping")
    async def ping(self, ctx):
        if self.client.latency == range(1, 80):
            embed=discord.Embed(title='Pong!', color=discord.Color.green())
            embed.add_field(name="Latency: ", value=f"{round(self.client.latency * 1000)}ms")
            await ctx.respond(embed=embed)
        elif self.client.latency == range(80, 500):
            embed=discord.Embed(title='Pong!', color=discord.Color.orange())
            embed.add_field(name="Latency: ", value=f"{round(self.client.latency * 1000)}ms")
            await ctx.respond(embed=embed)
        else:
            embed=discord.Embed(title='Pong!', color=discord.Color.dark_red())
            embed.add_field(name="Latency: ", value=f"{round(self.client.latency * 1000)}ms")
            await ctx.respond(embed=embed)

    @commands.slash_command(guid_ids=gid,name='magic8ball', description='magic 8ball')
    async def magic8ball(self, ctx, *, question: Option(str, description='Ask question.')):  # type: ignore
        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.",
                     "Very doubtful.", "Without a doubt.",
                     "Yes.", "Yes – definitely.", "You may rely on it."]
        await ctx.respond(embed=discord.Embed(title=f'Question: {question}', timestamp=datetime.datetime.now(),
                                           description=f"Answer: {random.choice(responses)}",
                                           color=discord.Color.random()))

    @commands.slash_command(guild_ids=gid , name= 'cat', description='Send a random cat picture.')
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search')as response:
                raw = await response.text()
                cat = json.loads(raw)[0]
                embed = discord.Embed(title= "🐱 Meow.." , url=cat['url'], color=discord.Color.random())
                embed.set_image(url = cat['url'])
                await ctx.respond(embed=embed)

    @commands.slash_command(guild_ids=gid , name= 'dog', description='Send a random doggo picture.')
    async def dog(self, ctx):
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random')as response:
                raw = await response.text()
                dog = json.loads(raw)
                embed = discord.Embed(title= "🐶 Woof!", url=dog['message'], color=discord.Color.random())
                embed.set_image(url = dog['message'])
                await ctx.respond(embed=embed)
    
    @commands.slash_command(guid_ids=gid,name='count', description='countdown a number')
    async def count(self, ctx, number: int):
        try:
            if number < 0:
                await ctx.send(embed=discord.Embed(title=f'Count', timestamp=datetime.datetime.utcnow(),
                                                   description=f"**Number can't be a negative.**",
                                                   color=discord.Color.dark_red()
                                                   ))
            elif number > 5000:
                await ctx.send(embed=discord.Embed(title=f'Count', timestamp=datetime.datetime.utcnow(),
                                                   description=f"**Number must be under 5000.**",
                                                   color=discord.Color.dark_red()
                                                   ))
            else:
                await ctx.respond(f'Started counting down from `{number}`', ephemeral=True)
                message = await ctx.send(number)
                while number != 0:
                    number -= 1
                    await message.edit(content=f"{number}")
                    await asyncio.sleep(1)
                await message.edit(content='Ended')

        except ValueError:
            await ctx.send(embed=discord.Embed(title='Error', timestamp=datetime.datetime.utcnow(),
                                               description=f"time was not a number",
                                               color=discord.Color.dark_red()))

    @commands.slash_command(guid_ids=gid,name = 'dm', description='Dm your friends.')
    async def dm(self, ctx, user: Option(discord.Member, description='Choose someone.'), msg: Option(str, description='message please :')):# type: ignore
        try:
            db = sqlite3.connect('user.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM user WHERE guild_id = {}".format(ctx.guild.id))
            result = cursor.fetchone()
            id = int(result[0])
            if id == user.id:
                await ctx.respond('You have been blocked by {}'.format(user))
            else:
                embed=discord.Embed(title=f'📥DM',timestamp=datetime.datetime.utcnow(),description='You got Dm 📬',
                                            color=discord.Color.green())
                embed.add_field(name="Server:", value=f"{ctx.guild}", inline=False)
                embed.add_field(name="From:", value=f"{ctx.author}", inline=False)
                embed.add_field(name="Message:", value=f"`{msg}`", inline=False)
                await DMChannel.send(user, embed=embed)
                em=discord.Embed(title=f'📤DM',timestamp=datetime.datetime.utcnow(),description='',
                                            color=discord.Color.green())
                em.add_field(name="To:", value=f"{ctx.user}", inline=False)
                em.add_field(name="Message:", value=f"`{msg}`", inline=False)
                await ctx.respond(embed=em, ephemeral=True)
        except discord.Forbidden:
            await ctx.respond(embed=discord.Embed(title=f'❌Error', timestamp=datetime.datetime.utcnow(),
                                                description=f"User closed their dm or block the client.",
                                                color=discord.Color.dark_red()
                                                ))

    @commands.slash_command(guild_ids=gid, name='timer', description='Timer')
    async def timer(self, ctx, time: Option(str, description='Use s for second , m for minute , h for hour and d for day')):# type: ignore
        convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
        time = int(time[:-1]) * convertTimeList[time[-1]]
        if time >= 3600:
            message = await ctx.author.send(f"Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
        elif time >= 60:
            message = await ctx.author.send(f"Timer: {time//60} minutes {time%60} seconds")
        elif time < 60:
            message = await ctx.author.send(f"Timer: {time} seconds")
        await ctx.respond(f'Timer has started. Check your DMs!\n Timer ID: {timers}', ephemeral=True)# type: ignore
        while True:
            try:
                await asyncio.sleep(1)
                time -= 1
                if time >= 3600:
                    await message.edit(content=f"Timer: {time//3600} hours {time %3600//60} minutes {time%60} seconds")# type: ignore
                elif time >= 60:
                    await message.edit(content=f"Timer: {time//60} minutes {time%60} seconds")# type: ignore
                elif time < 60:
                    await message.edit(content=f"Timer: {time} seconds")# type: ignore
                if time <= 0:
                    await message.edit(content="Ended!")# type: ignore
                    await ctx.author.send(f"{ctx.author.mention} Your Timer Has ended!")# type: ignore
                    break
            except:
                break

    @commands.slash_command(guild_ids=gid, name='delete-timer', description='Delte the Timer')
    async def deletetimer(self, ctx, timer_id: Option(str, "Id of the timer", choices = timers)):# type: ignore
        msg = await DMChannel.fetch_message(ctx.author, timer_id)
        await ctx.respond('Timer has been deleted.', ephemeral=True)
        await msg.delete() # Deleting

    @commands.slash_command(guild_ids=gid, name='say', description='Makes the bot say in chat')
    async def say(self, ctx, message: Option(str, description='what do you want to say?'), channel: Option(discord.TextChannel, description='where do you want the bot to say it?', required=False)):# type: ignore
        if channel == None:
            await ctx.respond('Sent!', ephemeral=True)
            await ctx.send(message)
        else:
            await ctx.respond('Sent to ```{}```.'.format(channel), ephemeral=True)
            await channel.send(message)
            
    @commands.slash_command(guild_ids=gid, name='random_number', description='Generate a random number between 0 and 100.')
    async def randomnumber(self, ctx):
        randomlist = random.sample(range(0, 100), 1)
        await ctx.respond(embed=discord.Embed(title='Random Number', description=randomlist, color=discord.Color.random()))
    
    @commands.slash_command(guid_ids=gid,name='announce', description='Announce in the channel with the client.')
    async def announce(self, ctx, message: Option(str, description='Message'), # type: ignore
    channel: Option(discord.TextChannel, description='Choose one channel', required=False)):# type: ignore
        if channel == None:
            embed=discord.Embed(title='', description=f"{message}",timestamp=datetime.datetime.now(), color=discord.Color.random())
            await ctx.send(embed=embed)
            await ctx.respond(f'I have announced `{message}` in `{ctx.channel}` channel.', ephemeral=True)
        else:
            embed=discord.Embed(title='', description=f"{message}",timestamp=datetime.datetime.now(), color=discord.Color.random())
            await channel.send(embed=embed)
            await ctx.respond(f'I have announced `{message}` in `{channel}` channel.', ephemeral=True)

    @commands.slash_command(guild_ids=gid, description='Block the User')
    async def block(self, ctx, user: Option(discord.Member, description='choose channel to setup')):
        db = sqlite3.connect('user.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM user WHERE guild_id = {}".format(ctx.guild.id))
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO user(guild_id, user_id) VALUES(?,?)")
            val = (ctx.guild.id, user.id)
            await ctx.respond(f"{user} has been blocked!", ephemeral=True)
        elif result is not None:
            sql = ("UPDATE user SET user_id = ? WHERE guild_id = ? ")
            val = (user.id, ctx.guild.id)
            await ctx.respond(f"{user} has been blocked", ephemeral=True)
        if ctx.author == ctx.guild:
            sql = ("INSERT INTO user(guild_id, user_id) VALUES(?,?)")
            val = (ctx.guild.id, user.id)
            await ctx.respond(f"{user}has been blocked", ephemeral=True)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.slash_command(guild_ids=gid, description='Unblock user')
    async def unblock(self, ctx, user: Option(discord.Member, description='Choose the channel that you want to remove.')):
        db = sqlite3.connect('user.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM user WHERE guild_id = {} ".format(ctx.guild.id))
        result = cursor.fetchone()
        if result:
            cursor.execute(f"DELETE FROM user WHERE user_id = {user.id} AND guild_id = {ctx.guild.id}")
            await ctx.respond(f"{user.mention} has been unblocked!", ephemeral=True)

    @commands.slash_command(guild_ids=gid)
    async def randomuser(self, ctx):
        users = ctx.guild.members
        choice = random.choice(users)
        role = discord.utils.get(ctx.guild.roles, id=1038828234952937663)
        for member in role.members:
            await member.remove_roles(role)
        await ctx.respond(embed=discord.Embed(title=f'Old user: {member.mention}',description=f'New user: {choice.mention}', color=discord.Color.green()))
        role_add = discord.utils.get(ctx.guild.roles, id=1038828234952937663)  
        await choice.add_roles(role_add)
        print({choice})

    @commands.slash_command(guild_ids=gid)
    async def insult(self, ctx):
        await ctx.defer()
        response = requests.get("http://autoinsult.datahamster.com/index.php?style=3").text
        site = BeautifulSoup(response, "lxml")
        await ctx.respond("{}!".format(site.select("div.insult")[0].text))
        
def setup(client): # this is called by Pycord to setup the cog
    client.add_cog(fun(client)) # add the cog to the bot