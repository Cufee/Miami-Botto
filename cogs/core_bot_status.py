import discord
from discord.ext import commands

# customize_bot cog

class bot_status(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'bot_status cog is ready.')

    #Commands
    @commands.command()
    async def setgame(self, ctx, *, game=''):
        '''Set game playing status.'''
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(game))
        print(f'Ran setgame')

    @commands.command(aliases=['ping'])
    async def pulse(self, ctx):
        '''Test if the bot is alive, returns ping.'''
        await ctx.send(f'I live! My latency is {round(self.client.latency * 1000)}ms')
        print('Ran pulse')

def setup(client):
    client.add_cog(bot_status(client))