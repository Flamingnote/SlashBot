from discord.ext import commands
import discord
import datetime
import discord.utils
import asyncio
import random
from datetime import timedelta
import time
from discord import Option
from os import times_result
import discord
from discord.ext import commands
import datetime
import asyncio
from discord import Option
from discord import FFmpegPCMAudio
import platform
import psutil
from datetime import timedelta
import time
import aiohttp

gid=[]

class giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.respond('```arm\nAn error occurred: {}\n```'.format(str(error)))

    @commands.slash_command(guild_ids=gid, description='Get help with Giveaway.')
    async def helpmegiveaway(self, ctx):
        # Help command that lists the current available commands and describes what they do
        embed = discord.Embed(color=5793266)
        embed.set_author(name='Commands/Help', icon_url='')
        embed.add_field(name='helpme', value='This command took you here!', inline=False)
        embed.add_field(name='giveaway',
                        value='Starts a giveaway for the server! This command will ask the host 6 questions.  The host will have 10 minutes per question to answer or they will be timed out!',
                        inline=False)
        embed.add_field(name='reroll `#channel_name` `message id`',
                        value='Host must follow the command with the copied message id from the giveaway.',
                        inline=False)
        await ctx.respond(embed=embed)

    def convert(self, time):
        pos = ["s", "m", "h", "d"]
        time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}
        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return val * time_dict[unit]

    @commands.slash_command(guild_ids=gid, name='giveaway', description='Create giveaway')
    async def giveaway(self, ctx):
        # Giveaway command requires the user to have a "Giveaway Host" role to function properly

        # Stores the questions that the bot will ask the user to answer in the channel that the command was made
        # Stores the answers for those questions in a different list
        giveaway_questions = ['Which channel will I host the giveaway in?', 'What is the prize?',
                              'How long should the giveaway run for (in day)(type 0 for none)?',
                              'How long should the giveaway run for (in hour)(type 0 for none)?',
                              'How long should the giveaway run for (in minute)(type 0 for none)?',
                              'How long should the giveaway run for (in second)?', 'What do you want to say in the description?']
        giveaway_answers = []

        # Checking to be sure the author is the one who answered and in which channel
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Askes the questions from the giveaway_questions list 1 by 1
        # Times out if the host doesn't answer within 30 seconds
        for question in giveaway_questions:
            await ctx.respond(question)
            try:
                message = await self.client.wait_for('message', timeout=600.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(
                    'You didn\'t answer in time.  Please try again and be sure to send your answer within 30 seconds of the question.')
                return
            else:
                giveaway_answers.append(message.content)

        # Grabbing the channel id from the giveaway_questions list and formatting is properly
        # Displays an exception message if the host fails to mention the channel correctly
        try:
            c_id = int(giveaway_answers[0][2:-1])
        except:
            await ctx.send(
                f'You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}')
            return

        # Storing the variables needed to run the rest of the commands
        channel = self.client.get_channel(c_id)
        prize = str(giveaway_answers[1])
        day = int(giveaway_answers[2])
        hour = int(giveaway_answers[3])
        minute = int(giveaway_answers[4])
        second = int(giveaway_answers[5])
        msg = str(giveaway_answers[6])
        total_time = 86400*day +3600*hour + 60*minute + second
        timestamp = int(time.time()) + total_time

        # Giveaway embed message 
        give = discord.Embed(title=prize, description=msg, color=3066993)
        give.set_author(name=f'GIVEAWAY TIME!', icon_url='https://i.imgur.com/VaX0pfM.png')
        give.add_field(name=f'{ctx.author.name} is giving away: {prize}!',
                       value=f'React with 🎉 to enter!\n Ends <t:{timestamp}:R>', inline=False)
        give.set_footer(icon_url=str(ctx.author.avatar), text=f"Giveaway created by {ctx.author.name}")
        my_message = await channel.send(embed=give)

        await ctx.respond(
            f'The giveaway for `{prize}` will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {total_time//3600} hours {total_time%3600//60} minutes {total_time%60} seconds!\n Giveaway ID: {my_message.id}', ephemeral=True)
        # Reacts to the message
        await my_message.add_reaction("🎉")
        await asyncio.sleep(total_time)
        ed = discord.Embed(title='Giveaway has Ended!', description='Thanks for entering.', color=discord.Color.dark_red())
        ed.add_field(name='Ended', value=f'<t:{timestamp}:R>')
        await my_message.edit(embed=ed)

        new_message = await channel.fetch_message(my_message.id)

        # Picks a winner
        users = await new_message.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        winner = random.choice(users)

        # Announces the winner
        winning_announcement = discord.Embed(color=15158332)
        winning_announcement.set_author(name=f'THE GIVEAWAY HAS ENDED!', icon_url='https://i.imgur.com/DDric14.png')
        winning_announcement.add_field(name=f'🎉 Prize: {prize}',
                                       value=f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}',
                                       inline=False)                   
        winning_announcement.set_footer(text='Thanks for entering!')
        await channel.send(embed=winning_announcement)
        await channel.send(f'Congratulations {winner.mention}! You won the **{prize}**!')

    @commands.slash_command(guild_ids=gid, name='reroll', description='Reroll the giveaway.')
    async def reroll(self, ctx, channel: discord.TextChannel, id_: int):
        # Reroll command requires the user to have a "Giveaway Host" role to function properly
        try:
            new_message = await channel.fetch_message(id_)
        except:
            await ctx.send("Incorrect id.")
            return

        # Picks a new winner
        users = await new_message.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        winner = random.choice(users)

        # Announces the new winner to the server
        reroll_announcement = discord.Embed(color=5793266)
        reroll_announcement.set_author(name=f'The giveaway was re-rolled by the host!',
                                       icon_url='https://i.imgur.com/DDric14.png')
        reroll_announcement.add_field(name=f'🥳 New Winner:', value=f'{winner.mention}', inline=False)
        await channel.send(embed=reroll_announcement)

        self.client.ticket_configs = {}

    @commands.slash_command(guild_ids=gid, description='Delete a giveaway.')
    async def delete_giveaway(self, ctx, giveaway_id:Option(str, description='Giveaway id')):
        msg = await ctx.fetch_message(giveaway_id)
        await ctx.respond('Giveaway has been deleted.', ephemeral=True)
        await msg.delete() # Deleting

def setup(client): # this is called by Pycord to setup the cog
    client.add_cog(giveaway(client)) # add the cog to the bot