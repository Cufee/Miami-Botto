import discord
from discord.ext import commands, tasks


class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'help cog is ready.')

    # Commands
    # @commands.command(aliases=[''])
    @commands.command(aliases=['help'])
    async def _(self):
        pass


def setup(client):
    client.remove_command("help")
    client.add_cog(help(client))
