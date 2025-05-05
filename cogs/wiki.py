import discord, wikipedia  # Import necessary libraries. Pycord for Discord interaction, and Wikipedia API.
from discord import Option  # For defining options in slash commands.
from discord.ext import commands  # Import commands extension from Pycord to create bot commands.
import datetime  # For working with dates and times.
import asyncio  # For handling asynchronous code.
from datetime import timedelta  # For working with time deltas.
import time  # Time-related functions.

gid = []  # List to store guild (server) IDs for command restrictions.

class wiki(commands.Cog):  # Define the 'wiki' cog. A Cog is a module that organizes related commands.
    
    def __init__(self, client):  # Constructor method that is called when the cog is initialized.
        self.client = client  # Assign the bot client to the instance of the class.

    # Slash command to return a Wikipedia summary.
    @commands.slash_command(guild_ids=gid, name='summary_wikipedia', description='Returns a Wikipedia summary')
    async def summary_wikipedia(self, ctx, search: Option(str, description="What do you want to get a summary for?", required=True)):  # Define the command with a required 'search' option.
        await ctx.channel.trigger_typing()  # Show the typing indicator to indicate the bot is processing the request.
        
        try:  # Try block to fetch Wikipedia summary.
            thesummary = wikipedia.summary(search, chars=1950)  # Fetch a Wikipedia summary with a 1950 character limit.
            
            try:
                await ctx.respond(thesummary)  # Respond with the summary as a slash command message.
            except:
                await ctx.send(thesummary)  # If the response fails, send the summary as a normal message.
        except:
            # If an error occurs (e.g., no article found), suggest a similar article based on search terms.
            searchsummary = str(wikipedia.search(search, suggestion=True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '')
            try:
                await ctx.respond(f"I can't seem to find a summary for that.. Did you mean: {searchsummary}")  # Suggest a similar search result.
            except:
                await ctx.send(f"I can't seem to find a summary for that.. Did you mean: {searchsummary}")  # Send as a regular message if responding fails.

    # Slash command to search Wikipedia.
    @commands.slash_command(guild_ids=gid, name="search_wikipedia", description="Search Wikipedia")
    async def search_wikipedia(self, ctx, search: Option(str, description="What do you want to search for?", required=True)):  # Define the search command with a required 'search' option.
        await ctx.channel.trigger_typing()  # Show the typing indicator.
        
        # Search for Wikipedia pages related to the search term and return suggestions.
        searchsearch = str(wikipedia.search(search, suggestion=True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '')
        try:
            await ctx.respond(searchsearch)  # Respond with the search results.
        except:
            await ctx.send(searchsearch)  # If responding fails, send the search results as a normal message.

    # Slash command to get the URL of a Wikipedia page.
    @commands.slash_command(guild_ids=gid, name="url_wikipedia", description="Get a URL to a page on Wikipedia")
    async def url_wikipedia(self, ctx, search: Option(str, description="What do you want to get a URL for?", required=True)):  # Define the URL retrieval command.
        await ctx.channel.trigger_typing()  # Show the typing indicator.
        
        try:  # Try block to fetch the summary and form the URL.
            urlsummary = wikipedia.summary(search, auto_suggest=False)  # Fetch summary with auto-suggest off.
            search = search.lower().replace(' ', '_').replace('  ', '_')  # Format the search term for URL.
            try:
                await ctx.respond(f'https://en.wikipedia.org/wiki/{search}')  # Respond with the Wikipedia URL.
            except:
                await ctx.send(f'https://en.wikipedia.org/wiki/{search}')  # If responding fails, send the URL as a normal message.
        except:
            # If an error occurs (e.g., no article found), suggest a similar article based on search terms.
            urlsearch = str(wikipedia.search(search, suggestion=True)).replace('(', '').replace(')', '').replace("'", "").replace('[', '').replace(']', '')
            try:
                await ctx.respond(f"I can't find what you're talking about, did you mean: {urlsearch}")  # Suggest a similar search result.
            except:
                await ctx.send(f"I can't find what you're talking about, did you mean: {urlsearch}")  # Send as a regular message if responding fails.

    # Slash command to get a random Wikipedia article.
    @commands.slash_command(guild_ids=gid, name="random_wikipedia", description="Returns a random Wikipedia article")
    async def random_wikipedia(self, ctx):
        await ctx.channel.trigger_typing()  # Show the typing indicator.
        
        randomtitle = wikipedia.random()  # Fetch a random Wikipedia article title.
        randomsummary = wikipedia.summary(randomtitle, chars=1950)  # Fetch a summary for the random article with a 1950 character limit.
        link = randomtitle.replace(' ', '_')  # Format the title for the Wikipedia URL.
        
        try:
            await ctx.respond(f"**{randomtitle}** \n\n{randomsummary}\n\nhttps://en.wikipedia.org/wiki/{link}")  # Respond with the article title, summary, and URL.
        except:
            await ctx.send(f"**{randomtitle}** \n\n{randomsummary}\n\nhttps://en.wikipedia.org/wiki/{link}")  # If responding fails, send as a regular message.

# Setup function to load the cog when the bot starts up.
def setup(client):
    client.add_cog(wiki(client))  # Add the 'wiki' cog to the bot client, allowing the bot to use the commands.
