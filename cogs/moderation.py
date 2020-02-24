import discord
from discord.ext import commands

name = 'moderation'

class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Moderation cog is ready!')

    #Commands
    @commands.command(aliases=[''])
    async def ping(self, ctx):
        await ctx.send(f'Pong! My latency is {round(self.client.latency * 1000)}ms')

def setup(client):
    client.add_cog(moderation(client))
