import discord
from discord.ext import commands, tasks

class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    #@commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'help cog is ready.')


    #Commands
    #@commands.command(aliases=[''])

def setup(client):
    client.add_cog(help(client))