import discord
from discord.ext import commands, tasks
import os

async def get_enabled_messages(guild_id):
    with open(f"{os.getcwd()}/cogs/cmd_auto_role_reactions/messages.txt") as file:
        reactions_message_ids = file.readlines()
    return reactions_message_ids

class auto_role_reactions(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'role_reactions cog is ready.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print('reaction')
        message_id = f'{payload.message_id}'
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        reactions_message_ids = await get_enabled_messages(guild_id)
        if message_id in reactions_message_ids:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            if role != None:
                await member.add_roles(role)
            else:
                pass
        else:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = f'{payload.message_id}'
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        reactions_message_ids = await get_enabled_messages(guild_id)

        if message_id in reactions_message_ids:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            if role != None:
                await member.remove_roles(role)
            else:
                pass
        else:
            pass

def setup(client):
    client.add_cog(auto_role_reactions(client))