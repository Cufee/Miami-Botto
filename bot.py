import discord
import os
from discord.ext import commands

TOKEN = open(f'{os.path.dirname(os.path.realpath(__file__))}/TOKEN.txt', 'r').read()

#Mode selection to adjust prefix
mode = open(f'{os.path.dirname(os.path.realpath(__file__))}/mode.txt', 'r').read()
if mode == 'master': client = commands.Bot(command_prefix = '-')
if mode == 'staging': client = commands.Bot(command_prefix = '.')

#Startup
@client.event
async def on_ready():
    print(f'{client.user.name} online!')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('with Rachels'))

async def on_command_error(ctx, error):
    print(f'Error! {error}')

#Cog managment
@client.command(hidden=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension} extension.')

@client.command(hidden=True)
async def unload(ctx, extension='null'):
    if extension == 'null':
        await ctx.send(f'No extension name specified.')
    else:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded {extension} extension.')

@client.command(hidden=True)
async def reload(ctx, extension='null'):
    if extension == 'null':
        await ctx.send(f'No extension name specified.')
    else:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded {extension} extension.')

@client.command(hidden=True)
async def listcogs(ctx):
    cogs = []
    for filename in os.listdir(f'{os.path.dirname(os.path.realpath(__file__))}/cogs'):
        if filename.endswith('.py'):
            cogs.append(f'{filename[:-3]}')
    await ctx.send(f'Found these cogs:\n{cogs}')

for filename in os.listdir(f'{os.path.dirname(os.path.realpath(__file__))}/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#Run
client.run(TOKEN)