import discord
from discord.ext import commands, tasks


class message_votes(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'help cog is ready.')

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        print(channel, message)


def setup(client):
    client.add_cog(message_votes(client))
