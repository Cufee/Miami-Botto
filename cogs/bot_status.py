import discord
from discord.ext import commands

# customize_bot cog

class bot_status(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'bot_status cog is ready!')

    #Commands
    @commands.command(aliases=[''])
    async def setgame(self, ctx, *, game):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game(game))

    @commands.command(aliases=[''])
    async def ping(self, ctx):
        await ctx.send(f'Pong! My latency is {round(self.client.latency * 1000)}ms')

def setup(client):
    client.add_cog(bot_status(client))