import discord, wikipedia # type: ignore #uses Pycord
from discord import Option
from discord.ext import commands
import datetime
import asyncio
from datetime import timedelta
import time

gid=[]

class wiki(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, client): # this is a special method that is called when the cog is loaded
        self.client = client

    @commands.slash_command(guild_ids=gid,name = 'summary_wikipedia', description='Returns a Wikipedia summary')
    async def summary_wikipedia(self, ctx, search: Option(str, description="What do you want to get a summary for?", required = True)):# type: ignore
        await ctx.channel.trigger_typing() #shows that the client is typing 
        try: #tries to get a summary
            thesummary = wikipedia.summary(search, chars = 1950) # type: ignore #limits the summary to a maximum of 1950 characters, discord's limit is 2,000 per message 
            try:
                await ctx.respond(thesummary)#responds to the slash command (client must respond within 3 seconds)
            except:
                await ctx.send(thesummary) #sends as a regular message, if it cannot send as a slash command 
        except:
            searchsummary = str(wikipedia.search(search, suggestion = True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '') # type: ignore #usually returns a list, so we turn it into a string, suggestion = true includes suggestions
            try:
                await ctx.respond(f"I can't seem to find a summary for that.. Did you mean: {searchsummary}")
            except:
                await ctx.send(f"I can't seem to find a summary for that.. Did you mean: {searchsummary}")

    @commands.slash_command(guild_ids=gid,name="search_wikipedia", description="search wikipedia")
    async def search_wikipedia(self, ctx,search: Option(str, description="What do you want to search for?", required = True)):# type: ignore
        await ctx.channel.trigger_typing() #shows that the client is typing 
        searchsearch = str(wikipedia.search(search, suggestion = True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '')# type: ignore #usually returns a list, so we turn it into a string, suggestion = true includes suggestions
        try:
            await ctx.respond(searchsearch)
        except:
            await ctx.send(searchsearch)

    @commands.slash_command(guild_ids=gid,name = "url_wikipedia", description = "Get a URL to a page on Wikipedia")
    async def url_wikipedia(self, ctx, search: Option(str, description="What do you want to get a URL for?", required = True)):# type: ignore
        await ctx.channel.trigger_typing()
        try: #tries to get a summary to see if we can get a link 
            urlsummary = wikipedia.summary(search, auto_suggest = False) # type: ignore #i think auto suggest is on by default
            search = search.lower().replace(' ', '_').replace('  ', '_')
            try:
                await ctx.respond(f'https://en.wikipedia.org/wiki/{search}')
            except:
                await ctx.send(f'https://en.wikipedia.org/wiki/{search}')
        except:
            urlsearch = str(wikipedia.search(search, suggestion = True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '') # type: ignore
            try:
                await ctx.respond(f"I can't find what you're talking about, did you mean: {urlsearch}")
            except:
                await ctx.send(f"I can't find what you're talking about, did you mean: {urlsearch}")
        
    @commands.slash_command(guild_ids=gid,name = "random_wikipedia", description= "Returns a random Wikipedia article")
    async def random_wikipedia(self, ctx):
        await ctx.channel.trigger_typing()
        randomtitle = wikipedia.random()# type: ignore #returns a title 
        randomsummary = wikipedia.summary(randomtitle, chars = 1950)# type: ignore
        link = randomtitle.replace(' ', '_')
        try:
            await ctx.respond(f"**{randomtitle}** \n\n{randomsummary}\n\nhttps://en.wikipedia.org/wiki/{link}")
        except:
            await ctx.send(f"**{randomtitle}** \n\n{randomsummary}\n\nhttps://en.wikipedia.org/wiki/{link}")

def setup(client): # this is called by Pycord to setup the cog
    client.add_cog(wiki(client)) # add the cog to the bot