import discord
from discord.ext import commands

# Moderation cog

class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'moderation cog is ready.')

    #Commands
    @commands.command()
    async def modtest(self, ctx, *, arg = 'null'):
        '''Test extension'''
        await ctx.send(arg)
    print('Ran modtest')

def setup(client):
    client.add_cog(moderation(client))
