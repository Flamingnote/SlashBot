from discord.ui import Button, View, Select
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
import datetime, asyncio, discord, sqlite3, os, topgg
import discord, aiohttp, time, datetime, asyncio, psutil, platform, textwrap, urllib, datetime
from discord import Option
from discord import DMChannel
from discord_together import DiscordTogether
from datetime import timedelta
from discord import FFmpegPCMAudio
import translators
import googletrans
from langdetect import detect
from dotenv import load_dotenv
from math import sqrt

intents = discord.Intents.all()
load_dotenv()
token = os.getenv("TOKEN")
gid=[]
client= discord.Bot(intents=intents)
connections = {}

@client.slash_command(guid_ids=gid,name='youtube', description='Watch youtube together in VC.')
async def youtube(ctx):
    try:

        link = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')# type: ignore
        button = Button(label=f"Click here to watch youtube in {ctx.author.voice.channel.name} channel.", url= link,style = discord.ButtonStyle.link)# type: ignore

        view = View()
        view.add_item(button)
        await ctx.defer()
        await ctx.respond('Notice: The button will be delete after 15 secs.',view=view)
        await asyncio.sleep(15)
        await ctx.delete()
    except:
        await ctx.respond(embed=discord.Embed(title=f'❌Error',
                                            description=f"You have to be in a voice channel to use this command.",
                                            color=discord.Color.dark_red()
                                            ))

@client.slash_command(guid_ids=gid,name= 'serverinfo', description = 'Get the information of the server')
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner.mention)
    id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    create = str(ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    role = str(len(ctx.guild.roles))

    icon = str(ctx.guild.icon)

    embed = discord.Embed(
            title=name+"\nServer Information",
            description=description,
            color=discord.Color.random()
    )
    embed.set_thumbnail(url=icon)

    embed.add_field(name=f"ID:", value=id, inline=False)
    embed.add_field(name="Server Owner", value=owner, inline=False)
    embed.add_field(name="Created On", value=create, inline=False)
    embed.add_field(name=f"Roles", value=role, inline=False)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    embed.set_footer(icon_url=str(ctx.author.avatar), text=f"Requested by {ctx.author.name}")

    await ctx.respond(embed=embed)

@client.slash_command(guid_ids=gid,name='record', description='Record a voice in Vc.')
async def record(ctx):  # If you're using commands.Bot, this will also work.
    voice = ctx.author.voice

    if not voice:
        await ctx.respond("You aren't in a voice channel!")

    vc = await voice.channel.connect()# Connect to the voice channel the author is in.
    connections.update({ctx.guild.id: vc})
          # Updating the cache with the guild and channel.

    vc.start_recording(
        discord.sinks.WaveSink(),  # The sink type to use.
        once_done,  # What to do once done.
        ctx.channel  # The channel to disconnect from.
    )
    await ctx.respond("Started recording!\n Note: Bot will send the recording file to the channel that you have used the cmd.")
async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args): # type: ignore # Our voice client already passes these in.
    recorded_users = [  # A list of recorded users
    f"<@{user_id}>"
    for user_id, audio in sink.audio_data.items()# type: ignore
            ]
    await sink.vc.disconnect() # type: ignore # Disconnect from the voice channel.
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()] # type: ignore # List down the files.
    await channel.send(f"finished recording audio for: {', '.join(recorded_users)}.", files=files)  # Send a message with the accumulated files.

@client.slash_command(guid_ids=gid,name='stop_recording', descrption='Stop recording the voice in Vc.')
async def stop_recording(ctx):
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        vc.stop_recording()  # Stop recording, and call the callback (once_done).
        del connections[ctx.guild.id]  # Remove the guild from the cache.
        await ctx.delete()  # And delete.
    else:
        await ctx.respond("I am currently not recording here.")  # Respond with this if we aren't recording.

@client.user_command(guid_ids=gid,name="Account Creation Date")  # create a user command for the supplied guilds
async def account_creation_date(ctx, member: discord.Member):  # user commands return the member
    await ctx.respond(f"{member.name}'s account was created on `{member.created_at}`")

@client.user_command(guid_ids=gid,name="Server Join Date")  # create a user command for the supplied guilds
async def account_join_date(ctx, member: discord.Member):  # user commands return the member
    await ctx.respond(f"{member.name} was joined {ctx.guild} on `{member.joined_at}`")

@client.message_command(guid_ids=gid,name="Get Message ID")  # creates a global message command. use guild_ids=[] to create guild-specific commands.
async def get_message_id(ctx, message: discord.Message):  # message commands return the message
    await ctx.respond(f"Message ID: `{message.id}`")

@client.message_command(guild_ids=gid, name="Translate")
async def translate(ctx: discord.ext.commands.Context, message: discord.Message):
    try:
        translator = googletrans.Translator()
        # Translate the text from English to Spanish
        text = message.content
        translated_text = translator.translate(text, dest='en')
        embed=discord.Embed(title='Translation', color=discord.Color.random())
        embed.add_field(name='Translate from', value=text, inline=True)
        embed.add_field(name='Translation', value=translated_text.text, inline=False)
        await ctx.respond(embed=embed, ephemeral=True)
    except:
        await ctx.respond(f"Sorry, I can't translate this.", ephemeral=True)

@client.slash_command(guild_ids=gid)
async def broadcast(ctx, message: str):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    for guild in client.guilds:
        # Get the channel IDs from the database
        cursor.execute("SELECT channel_id FROM main WHERE guild_id = {}".format(ctx.guild.id))
        result = cursor.fetchone()
        # Iterate over the channel IDs
        for channel_id in result:
            # Get the channel object using the channel ID
            channel = guild.get_channel(channel_id[0])
        # Send the message to the channel
        await channel.send(message)
        await ctx.respond(result[0])

    db.close()

@client.slash_command(guid_ids=gid,name = 'sudo', description='Say as someone.')
async def sudo(ctx, member: Option(discord.Member, description='Get someone'), message: Option(str, description='message'), channel: Option(discord.TextChannel, description='Choose a channel you want to send', required = False)):# type: ignore
    words = ['Nigga', 'nIggA','bitch','BITCH', 'nigga', 'cum', 'dick', 'pussy', 'Dick', 'Pussy', 'CUM', 'DICK', 'PUSSY']
    await ctx.defer(ephemeral=True)
    if any(word in message for word in words):
        await ctx.respond("{} Watch your language! That Word is not Allowed to be used. Please only use SFW words.".format(ctx.author.mention), ephemeral=True)
    else:
        if channel == None:
            webhook = await ctx.channel.create_webhook(name=member.display_name)
            embed=discord.Embed(title=f'Sudo', timestamp=datetime.datetime.now(),
                                                                    description=f"",
                                                                    color=discord.Color.green())
            embed.add_field(name='Sudo as:', value=member, inline=False)
            embed.add_field(name='Message:', value=f"`{message}`", inline=False)
            await ctx.respond(embed=embed,ephemeral=True )
            await webhook.send(str(message),username=member.display_name,avatar_url=member.avatar)
            await webhook.delete()
        else:
            webhook = await channel.create_webhook(name=member.display_name)
            em=discord.Embed(title=f'Sudo', timestamp=datetime.datetime.now(),
                                                                    description=f"",
                                                                    color=discord.Color.green())
            em.add_field(name='Sudo as:', value=member, inline=False)
            em.add_field(name='To:', value=f"<#{channel.id}>", inline=False)
            em.add_field(name='Channel ID:', value=f"`{channel.id}`",inline=False)
            em.add_field(name='Message:', value=f"`{message}`", inline=False)
            await ctx.respond(embed=em, ephemeral=True)
            await webhook.send(str(message),
                                                username=member.display_name,
                                                avatar_url=member.avatar) 
            await webhook.delete()

@client.slash_command(guild_ids=gid, name='whois', description='Get user information')
async def whois(ctx, user: discord.Member = None):# type: ignore
    if user == None:
        user = ctx.author

    rlist = []
    for role in user.roles:
        if role.name != "@everyone":
            rlist.append(role.mention)

    b = ", ".join(rlist)

    embed = discord.Embed(colour=user.color)

    embed.set_author(name=f"User Info - {user}"),# type: ignore
    embed.set_thumbnail(url=user.avatar),# type: ignore
    embed.set_footer(text=f'Requested by - {ctx.author}',
                         icon_url=ctx.author.avatar)

    embed.add_field(name='ID:', value=user.id, inline=False)# type: ignore
    embed.add_field(name='Nickname:', value=user.display_name, inline=False)

    embed.add_field(name='Created at:', value=user.created_at, inline=False)# type: ignore
    embed.add_field(name='Joined at:', value=user.joined_at, inline=False)# type: ignore

    embed.add_field(name='Bot?', value=user.bot, inline=False)# type: ignore

    embed.add_field(name=f'Roles:({len(rlist)})', value=''.join([b]), inline=False)
    embed.add_field(name='Top Role:', value=user.top_role.mention, inline=False)

    await ctx.respond(embed=embed)

@client.slash_command(guild_ids=gid, name='translate', description='google translate')
async def translate(ctx, message, frm, to ):
    await ctx.defer()
    google=translators.google(message, from_language=frm , to_language=to)
    await ctx.respond(google)

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.add_item(discord.ui.InputText(label="Your discord name and tag"))
        self.add_item(discord.ui.InputText(label="What do you want to suggest about?", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):  
        author = interaction.user
        avatar = str(interaction.user.avatar)# type: ignore
        server = interaction.user.guild# type: ignore
    
        serverid = interaction.user.guild.id# type: ignore
        channel = client.get_channel(1038315929978798231)
        embed = discord.Embed(title="Suggestion", color=discord.Color.green())
        embed.set_author(name=author, icon_url=avatar)
        embed.add_field(name="Server", value=f"From: {server}\n Server Id: {serverid}", inline=False)
        embed.add_field(name="Your discord name(ed. Tom#6942", value=self.children[0].value)# type: ignore
        embed.add_field(name="What do you want to suggest about?", value=self.children[1].value, inline=False)# type: ignore
        await channel.send(embeds=[embed])# type: ignore
        await interaction.response.send_message('Thanks for your suggestion.')

@client.slash_command(guild_ids=gid, name='suggest', description='Creates a suggestion')
async def suggest(ctx: discord.ApplicationContext):
    modal = MyModal(title="Suggestion for Slash discord bot.")
    await ctx.send_modal(modal)

@client.slash_command(guild_ids=gid, description='Search lyrics')
async def lyrics(ctx, search: Option(str, "song name")):
    song = urllib.parse.quote(str(search))  # url-encode the song provided so it can be passed on to the API

    async with aiohttp.ClientSession() as lyricsSession:
        async with lyricsSession.get(
                f'https://some-random-api.ml/lyrics?title={song}') as jsondata:  # define jsondata and fetch from API
            if not 300 > jsondata.status >= 200:  # if an unexpected HTTP status code is recieved from the website, throw an error and come out of the command
                return await ctx.send(f'Recieved poor status code of {jsondata.status}')

            lyricsData = await jsondata.json()  # load the json data into its json form

    error = lyricsData.get('error')
    if error:  # checking if there is an error recieved by the API, and if there is then throwing an error message and returning out of the command
        return await ctx.respond(f'Recieved unexpected error: {error}')

    songLyrics = lyricsData['lyrics']  # the lyrics
    songArtist = lyricsData['author']  # the author's name
    songTitle = lyricsData['title']  # the song's title
    songThumbnail = lyricsData['thumbnail']['genius']  # the song's picture/thumbnail

    # sometimes the song's lyrics can be above 4096 characters, and if it is then we will not be able to send it in one single message on Discord due to the character limit
    # this is why we split the song into chunks of 4096 characters and send each part individually
    for chunk in textwrap.wrap(songLyrics, 4096, replace_whitespace=False):
        embed = discord.Embed(
            title=songTitle,
            description=chunk,
            color=discord.Color.random(),
            timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=songThumbnail)
        embed.set_footer(text=f"song artist - {songArtist}")
        await ctx.respond(embed=embed)


math = discord.SlashCommandGroup("math", "Math related commands")

@math.command(description='add')
async def add(ctx, num1: int, num2: int):
  sum = num1 + num2
  await ctx.respond(f"**{num1}** + **{num2}** = `{sum}`")

@math.command(description='subtract')
async def subtract(ctx, num1: int, num2: int):
  sum = num1 - num2
  await ctx.respond(f"**{num1}** - **{num2}** = `{sum}`")

@math.command(description='multiply')
async def multiply(ctx, num1: int, num2: int):
    sum = num1 * num2
    await ctx.respond(f"**{num1}** * **{num2}** = `{sum}`")

@math.command(description='division')
async def division(ctx, num1: int , num2: int):
    sum = num1 / num2
    await ctx.respond(f"**{num1}** ÷ **{num2}** = `{sum}`")

@math.command(description='Square Root')
async def square_root(ctx, x: int):
    await ctx.respond(sqrt(x))

# you'll have to manually add the manually created Slash Command group
client.add_application_command(math)

cogs_list = ['greetings','moderation','fun', 'giveaway', 'wiki', 'uptime', 'test','mongodb']

for cog in cogs_list:
    client.load_extension(f'cogs.{cog}')
    print(f"{cog} has been loaded!")

@client.event
async def on_ready():
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS main(
        guild_id TEXT,
        channel_id TEXT
    )
    ''')
    task_loop.start()
    client.togetherControl = await DiscordTogether(token)# type: ignore
    print('Bot is ready.')
    print(f"Bot is running on {len(client.guilds)} servers.")

@tasks.loop(seconds=5)
async def task_loop():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))

client.run(token)
