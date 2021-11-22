#!/usr/bin/python3.8
import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import typing
import time
from dotenv import load_dotenv
from profanity_check import predict, predict_prob
from datetime import datetime
from log import Logger

load_dotenv('.env')

i = discord.Intents.default()
i.members = True

client = commands.Bot(command_prefix='v.',intents=i)

game = discord.Game("NULL")

verifed_users = [533582968371806211, 348406262792323072]
privilaged_users = [322015089529978880]

uganda = 525442477365133323


time_window_milliseconds = 1000
max_msg_per_window = 3
# A dict of users to prevent spam
author_msg_times = {}

logger = Logger(os.environ.get('DROPBOX_TOKEN', 0))

async def is_owner(ctx):
    return ctx.author.id in privilaged_users

async def profanityLevel(msg):

    msgsplit = msg.split()    
    for c in msgsplit:
        if c == "neger" or c == "negrar" or c == "n3g3r" or c == "n3ger" or c == "neg3r":
            return 1.0
    else:
        # Use AI to detect profanity level. if over a % return False.
        return predict_prob([msg])[0]

async def detect_spam(msg):
    global author_msg_counts

    author_id = msg.author.id
    # Get current epoch time in milliseconds
    curr_time = datetime.now().timestamp() * 1000

    # Make empty list for author id, if it does not exist
    if not author_msg_times.get(author_id, False):
        author_msg_times[author_id] = []

    # Append the time of this message to the users list of message times
    author_msg_times[author_id].append(curr_time)

    # Find the beginning of our time window.
    expr_time = curr_time - time_window_milliseconds

    # Find message times which occurred before the start of our window
    expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
    ]

    # Remove all the expired messages times from our list
    for msg_time in expired_msgs:
        author_msg_times[author_id].remove(msg_time)
    # ^ note: we probably need to use a mutex here. Multiple threads
    # might be trying to update this at the same time. Not sure though.

    if len(author_msg_times[author_id]) > max_msg_per_window:
        # await msg.delete()
        await msg.author.send("Din lilla snorunge sluta spamma")
        return True


def removeMessageEmbed(msg):

    channel_link = f"https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}"
    embed = discord.Embed(title="Message from user deleted",URL=channel_link, colour=discord.Colour.red())
        
    embed.add_field(name=f"User", value=f"{msg.author.name}#{msg.author.discriminator}", inline=False)
    embed.add_field(name="Content", value=f"'{msg.content}'", inline=False)
    embed.add_field(name="Where?", value=f"#{msg.channel.name} in {msg.guild.name}", inline=False)

    embed.timestamp = datetime.utcnow()
    embed.set_footer(text='\u200b', icon_url=msg.author.avatar_url)

    return embed


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=game)
    print("Ready to serve!")
    global owner
    owner = await client.fetch_user(322015089529978880)


@client.event
async def on_member_join(joined_member):
    if joined_member.id in verifed_users and joined_member.guild.id == uganda:
        knuckle = discord.utils.get(joined_member.guild.roles, id=525444324561780737)
        await joined_member.edit(roles=[knuckle])
        print("ADDED ROLE TO ", joined_member)

@client.event
async def on_message(message):
    if message.author.bot:
        return
    pfLevel = await profanityLevel(message.content)
    
    if pfLevel >= 1.0:
        await message.author.kick()

    if pfLevel > .8:
        deletionEmbed = removeMessageEmbed(message)
        await message.delete()
        await owner.send(embed = deletionEmbed)
    else:

        if await detect_spam(message):
            await owner.send(f"{message.author.name} spamar")

        await client.process_commands(message)

# Block all dms
# @client.check
# async def globally_block_dms(ctx):
#     return ctx.guild is not None

# Remove already existing command
client.remove_command("help")
@client.command()
async def help(ctx):
    await ctx.send("Lol")

# Quick ping pong test
@client.command()
async def ping(ctx):    
    await ctx.send("pong")

# Mute a user's ability to write in text channels.
@client.command()
async def mute(ctx, *args):
    pass

# Server mute a user
@client.command()
async def smute(ctx, *args):
    pass    

# Remove messages in channel (amount) from a specific user or from all users
@client.command()
@has_permissions(manage_messages=True)
async def purge(ctx, amount: int, members: commands.Greedy[discord.Member] = None):
    messages = []
    if 1 >= amount <= 100:
        await ctx.send("Purge amount needs to be in the range of 1-100")
        return

    async for message in ctx.channel.history(limit=amount):
        # len of messages + 1 as it wants to delete org message to
        if len(messages) + 1 >= amount: break
        
        if members != None:
            if message.author in members:
                messages.append(message)
        else:
            messages.append(message)
        # messages = discord.utils.get(await ctx.channel.history(limit=amount).flatten(), authors=members)
    
    print(f"Doing a purge with {len(messages)} messages")

    await ctx.channel.delete_messages(messages)    


@client.command()
async def testCount(ctx, amount: int):
    for n in range(1, amount - 1):
        await ctx.send(str(n))
        time.sleep(1)

# @client.command()
# async def remember(ctx, content):
#     logger.title = "test_log"
#     logger.log(content)
#     await ctx.send(f"I'll remember: {content}")


        
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN', 0)

if DISCORD_TOKEN != 0:
    client.run(DISCORD_TOKEN)