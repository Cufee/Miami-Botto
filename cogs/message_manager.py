import discord
from discord.ext import commands

class message_manager(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('message_manager cog is ready.')

    #Commands
    @commands.command()
    async def test(self, ctx):
        '''Test'''
        await ctx.send('ok')

def setup(client):
    client.add_cog(message_manager(client))