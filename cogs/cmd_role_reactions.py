import discord
from discord.ext import commands, tasks
import json
import os

def get_message_settings(guild_id, message_id):
    guild_settings_path = f"{os.getcwd()}/cogs/cmd_role_reactions/guild_settings_beta.json"
    with open(guild_settings_path, 'r') as all_guild_settings_json:
        print('sucvc')
        all_guild_settings = json.load(all_guild_settings_json)

    guild_id = f'{guild_id}'
    message_id = f'{message_id}'

    if guild_id in all_guild_settings.keys():
        guild_messages = all_guild_settings.get(guild_id)
        if message_id in guild_messages.keys():
            message_settings = guild_messages.get(message_id)
            return (message_settings)
    else:
        return None

class role_reactions(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'role_reactions cog is ready.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        message_settings = get_message_settings(guild_id, message_id)

        if message_settings != None:
            if payload.emoji.name in message_settings.keys():
                role_name = message_settings.get(payload.emoji.name)
                role = discord.utils.get(guild.roles, name=role_name)
                print(member)
                if member != None:
                    await member.add_roles(role)
                else:
                    print('Member not found')
        else: 
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, self.client.guilds)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        message_settings = get_message_settings(guild_id, message_id)

        if message_settings != None:
            if payload.emoji.name in message_settings.keys():
                role_name = message_settings.get(payload.emoji.name)
                role = discord.utils.get(guild.roles, name=role_name)
                print(member)
                if member != None:
                    await member.remove_roles(role)
                else:
                    print('Member not found')
        else: 
            pass

    #Commands
    @commands.command(aliases=[''])
    async def rr(self, ctx, command = None):
        if command != None:
            if command == 'init':
                await ctx.send(f'Guild {ctx.guild.id}\nMessage {ctx.message.id}')
        else:
            await ctx.send('Please specify a command')

def setup(client):
    client.add_cog(role_reactions(client))