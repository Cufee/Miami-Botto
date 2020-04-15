import discord
from discord.ext import commands, tasks
import os

async def get_enabled_messages(guild_id):
    with open(f"{os.getcwd()}/cogs/cmd_auto_role_reactions/messages.txt") as file:
        reactions_message_ids = file.readlines()
    return reactions_message_ids

async def add_enabled_message(guild_id, message_id):
    with open(f"{os.getcwd()}/cogs/cmd_auto_role_reactions/messages.txt", 'a') as file:
        file.write(f'{message_id}')

async def remove_enabled_message(guild_id, message_id):
    with open(f"{os.getcwd()}/cogs/cmd_auto_role_reactions/messages.txt") as file:
        reactions_message_ids = file.readlines()
    if message_id in reactions_message_ids:
        message_index = reactions_message_ids.index(message_id)
        reactions_message_ids = reactions_message_ids.pop(message_index)
        with open(f"{os.getcwd()}/cogs/cmd_auto_role_reactions/messages.txt", 'w') as file:
            for msg_id in reactions_message_ids:
                file.write("".join(f'{msg_id}') + "\n")
        return True
    else:
        return False

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

        #Dev reaction
        if payload.emoji.name == 'dev':
            print('detected dev emoji')
            channel = await member.create_dm()
            await channel.send(f'Message ID {message_id}')

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

    #Commands
    @commands.command(hidden=True)
    async def arr(self, ctx, command=None, option=None):
        guild_id = ''
        if command != None:
            if command == 'init':
                await add_enabled_message(guild_id, ctx.message.id)
                await ctx.send(f'Your last message was enrolled, feel free to edit it :)\nGuild {ctx.guild.id}\nMessage {ctx.message.id}')
            elif command == 'remove':
                if option == None:
                    await ctx.send(f'I will need a message id as well, use ```mr-arr remove id```')
                else:
                    removed_bool = await remove_enabled_message(guild_id, option)
                    if removed_bool == True:
                        await ctx.send(f'Message with ID {option} was removed.')
                    else:
                        await ctx.send(f'Something failed, remove_enabled_message returned {removed_bool}. ```Your input was {option}```')
            else:
                await ctx.send('No such command')
        else:
            await ctx.send('Please specify a command')

def setup(client):
    client.add_cog(auto_role_reactions(client))