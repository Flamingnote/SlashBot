import discord #imports discord.py
import datetime, time #this is the important set for generating an uptime
from discord.ext import commands

gid=[]

class uptime(commands.Cog):
    def __init__(self, client):
        self.client = client
    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.respond('```arm\nAn error occurred: {}\n```'.format(str(error)))# type: ignore

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime #global variable to be used later in cog
        startTime = time.time() # snapshot of time when listener sends on_ready

    #create a command in the cog
    @commands.slash_command(guild_ids=gid, name='uptime')
    async def uptime(self,ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        await ctx.respond(uptime)

#needed or the cog won't run
def setup(client): # this is called by Pycord to setup the cog
    client.add_cog(uptime(client)) # add the cog to the bot