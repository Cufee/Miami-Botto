import discord
from discord.ext import commands

#Setup Guild
guild_id = ''


# Secret Chats cog

class secret_chats(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'secret_chats cog is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        pass


    #Commands

def setup(client):
    client.add_cog(secret_chats(client))
