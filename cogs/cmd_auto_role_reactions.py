import discord
from discord.ext import commands, tasks
import os
import re

async def get_enabled_messages(guild_id):
    reactions_message_ids = []
    with open(f"{os.getcwd()}/cogs/cmd_auto_role_reactions/messages.txt") as file:
        for line in file:
            final_data = line[:-1]
            reactions_message_ids.append(final_data)
    return reactions_message_ids

async def add_enabled_message(guild_id, message_id):
    with open(f"{os.getcwd()}/cogs/cmd_auto_role_reactions/messages.txt", 'a') as file:
        file.write(f'{message_id}\n')

async def remove_enabled_message(guild_id, message_id):
    reactions_message_ids = []
    with open(f"{os.getcwd()}/cogs/cmd_auto_role_reactions/messages.txt") as file:
        for line in file:
            final_data = line[:-1]
            reactions_message_ids.append(final_data)
    if message_id in reactions_message_ids:
        message_index = reactions_message_ids.index(message_id)
        reactions_message_ids = reactions_message_ids.pop(message_index)
        with open(f"{os.getcwd()}/cogs/cmd_auto_role_reactions/messages.txt", 'a') as file:
            for msg in reactions_message_ids:
                file.write(f'{msg}\n')
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
        
        #Logic to prevent people from setting all the roles in one category
        role_search_tag = payload.emoji.name[-6:]
        member_roles = []
        for role in member.roles:
            member_roles.append(role.name)
        r = re.compile(f'.*{role_search_tag}')
        matched_roles = list(filter(r.match, member_roles))

        #Dev reaction
        if payload.emoji.name == 'dev':
            print('detected dev emoji')
            channel = await member.create_dm()
            await channel.send(f'Message ID {message_id}')

        role = discord.utils.get(guild.roles, name=payload.emoji.name)
        if message_id in reactions_message_ids:
            print(f'Message was in reaction_messages {message_id}, role {role}')
            if role != None:
                #Logic to prevent people from setting all the roles in one category
                for old_role in matched_roles:
                    old_role = discord.utils.get(guild.roles, name=old_role)
                    await member.remove_roles(old_role)
                    print(f'Removed {old_role}')
                await member.add_roles(role)
                print(f'Added {role}')
            else:
                print(f'Removing reaction {payload.emoji.name} from {message_id}')
                channel = self.client.get_channel(payload.channel_id)
                message = await channel.fetch_message(message_id)
                await message.remove_reaction(payload.emoji, member)
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
    async def msginit(self, ctx):
        print('ran init')
        guild_id = ''
        await add_enabled_message(guild_id, ctx.message.id)
        await ctx.send(f'Your last message was enrolled, feel free to edit it :)')

    #Commands
    @commands.command(hidden=True)
    async def msgadd(self, ctx, msg_id):
        guild_id = ''
        await add_enabled_message(guild_id, msg_id)
        await ctx.send(f'Your message {msg_id} was enrolled, feel free to edit it :)')

    #Commands
    @commands.command(hidden=True)
    async def msgremove(self, ctx, option=None):
        guild_id = ''
        if option == None:
            await ctx.send(f'I will need a message id as well, use ```mr-arr remove id```')
        else:
            removed_bool = await remove_enabled_message(guild_id, option)
            if removed_bool == True:
                await ctx.send(f'Message with ID {option} was removed.')
            else:
                await ctx.send(f'Something failed, remove_enabled_message returned {removed_bool}. ```Your input was {option}```')

def setup(client):
    client.add_cog(auto_role_reactions(client))