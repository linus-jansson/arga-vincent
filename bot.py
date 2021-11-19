#!/usr/bin/python3.8
import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import typing
import time
from dotenv import load_dotenv
# from profanity_check import predict, predict_prob


load_dotenv('.env')

i = discord.Intents.default()
i.members = True

client = commands.Bot(command_prefix='v.',intents=i)

game = discord.Game("NULL")

verifed_users = [533582968371806211, 348406262792323072]
privilaged_users = [322015089529978880]

uganda = 525442477365133323


async def is_owner(ctx):
    return ctx.author.id in privilaged_users

async def passedFilter(msg):
    passed = True
    msg = msg.split()
    # Filters messages
    # with open("wordlist.txt", 'r') as f:
    #     words = f.read()
    #     badwords = re.split('\"[a-zA-Z0-9]*\"', words)
    #     print(badwords)
    # print(predict_prob([msg]))
    print("filtering")

    for c in msg:
        if c == "neger" or c == 'nigger':
            passed = False
            break

    return passed


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=game)
    print("Ready to serve!")


@client.event
async def on_member_join(joined_member):
    if joined_member.id in verifed_users and joined_member.guild.id == uganda:
        knuckle = discord.utils.get(joined_member.guild.roles, id=525444324561780737)
        await joined_member.edit(roles=[knuckle])
        print("ADDED ROLE TO ", joined_member)

@client.event
async def on_message(message):
    if message.author.bot:
        pass
    
    if not await passedFilter(message.content):
        await message.delete()
        await message.author.kick()

    
    await client.process_commands(message)

# @client.check
# async def globally_block_dms(ctx):
#     return ctx.guild is not None

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

        
token = os.environ.get('TOKEN', 0)

if token != 0:
    client.run(token)