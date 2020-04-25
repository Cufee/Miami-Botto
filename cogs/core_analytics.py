import discord
from discord.ext import commands

# Dev cog


class analytics(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Cog loaded
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'analytics cog is ready.')

    # on_typing
    @commands.Cog.listener()
    async def on_typing(self):
        pass

    # on_message
    @commands.Cog.listener()
    async def on_message(self):
        pass

    # on_raw_message_delete
    @commands.Cog.listener()
    async def on_raw_message_delete(self):
        pass

    # on_raw_message_edit
    @commands.Cog.listener()
    async def on_raw_message_edit(self):
        pass

    # on_raw_reaction_add
    @commands.Cog.listener()
    async def on_raw_reaction_add(self):
        pass

    # on_raw_reaction_clear
    @commands.Cog.listener()
    async def on_raw_reaction_clear(self):
        pass

    # on_guild_join
    @commands.Cog.listener()
    async def on_guild_join(self):
        pass

    # on_guild_remove
    @commands.Cog.listener()
    async def on_guild_remove(self):
        pass

    # on_member_join
    @commands.Cog.listener()
    async def on_member_join(self):
        pass

    # on_member_remove
    @commands.Cog.listener()
    async def on_member_remove(self):
        pass

    # on_user_update
    @commands.Cog.listener()
    async def on_user_update(self):
        pass

    # on_voice_state_update
    @commands.Cog.listener()
    async def on_voice_state_update(self):
        pass


def setup(client):
    client.add_cog(analytics(client))
