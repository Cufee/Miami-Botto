#Discord py
import discord
from discord.ext import commands, tasks

#Cog specific
import os
import json

    #Settings
#Set simp_list_json_path
global simp_list_json_path
simp_list_json_path = f"{os.getcwd()}/cogs/simp/simp_list.json"

#Set emote list
global emote_list_json_path
emote_list_json_path = f"{os.getcwd()}/cogs/simp/guild_emotes.json"


#Loop to check if guild_id and user_id pair is in simp_list
def check_if_simp(guild_id, user_id):
    guild_id = f'{guild_id}'
    user_id = f'{user_id}'
    #Import simp list as Object
    with open(simp_list_json_path) as simp_list_json:
        big_simp_list = json.load(simp_list_json)
        #Check if guild_id exists in simp_list_json
    if guild_id in big_simp_list:
        simp_list = big_simp_list.get(guild_id)
        #Check if user_id exists in simp_list[guild_id]
        if user_id in simp_list:
            return True
        else:
            return False
    else:
        return False

#Add guid_id and user_id to simp_list.json
def declare_simp(guild_id, user_id):
    guild_id = f'{guild_id}'
    user_id = f'{user_id}'
    #Import simp list as Object
    with open(simp_list_json_path, 'r') as simp_list_json:
        big_simp_list = json.load(simp_list_json)
    #Import simp_list
    if guild_id in big_simp_list:
        simp_list = big_simp_list.get(guild_id)
    else:
        simp_list = []
    #Check if user_id in simp_list
    if user_id in simp_list:
        #Returning 409 Conflicts
        return 409
    else:
        #Add user_id to list
        simp_list.append(user_id)
        #Add guild_id user_id pair to Object
        simp_in_guild = {guild_id: simp_list}
        big_simp_list.update(simp_in_guild)
        #Write Object to json
        with open(simp_list_json_path, 'w') as simp_list_json:
            json.dump(big_simp_list, simp_list_json)
        #Returning 200 OK
        return 200

#Remove guid_id and user_id from simp_list.json
def remove_simp(guild_id, user_id):
    guild_id = f'{guild_id}'
    user_id = f'{user_id}'
    #Import simp list as Object
    with open(simp_list_json_path, 'r') as simp_list_json:
        big_simp_list = json.load(simp_list_json)
    #Import simp_list
    simp_list = big_simp_list.get(guild_id)
    #Check if user_id in simmp_list
    if user_id in simp_list:
        #Remove guild_id user_id pair from Object
        simp_list.remove(user_id)
        simp_in_guild = {guild_id: simp_list}
        big_simp_list.update(simp_in_guild)
        #Write Object to json
        with open(simp_list_json_path, 'w') as simp_list_json:
            json.dump(big_simp_list, simp_list_json)
        #Returning 200 OK
        return 200
    else:
        #Returning 404 Not Found
        return 404

# Secret Chats cog
class simp(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    #@commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'simp cog is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            pass
        else:
            #Get guid_id and user_id
            guild_id = f'{message.guild.id}'
            user_id = f'{message.author.id}'
            #Check if guild and user are in simp_list
            simp_detected = check_if_simp(guild_id, user_id)
            #If user in simp_list, react to message with emote
            if simp_detected == True:
                #Get emopte_id from guild_id
                with open(emote_list_json_path) as emotes_json:
                    emotes = json.load(emotes_json)
                    #React
                    if guild_id in emotes:
                        emote_id = emotes.get(guild_id)
                        emote = self.client.get_emoji(emote_id)
                        await message.add_reaction(emote)
                    else:
                        pass
            else:
                pass


    #Loops
    #@tasks.loop(seconds=5.0)


    #Commands
    #@commands.command()
    
    @commands.command()
    @commands.has_role("SimpKing")
    #Declare a user as simp
    async def simp(self, ctx, arg):
        guild_id = str(ctx.message.guild.id)
        user_id = f'{arg[3:-1]}'
        exists = False
        for guild in self.client.guilds:
            for member in guild.members:
                if str(member.id) == user_id:
                    exists = True
        if exists == True:
            result = declare_simp(guild_id, user_id)
            if result == 200:
                await ctx.send(f'{arg} is now a registered simp!')
            if result == 409:
                await ctx.send(f'{arg} is already a registered simp!')
            else:
                await ctx.send(f'Weird... {result}')
        else:
            await ctx.send('User not found :C')

    #Remove user from simp list
    @commands.command()
    @commands.has_role("SimpKing")
    async def notsimp(self, ctx, arg):
        guild_id = str(ctx.message.guild.id)
        user_id = f'{arg[3:-1]}'
        exists = False
        for guild in self.client.guilds:
            for member in guild.members:
                if str(member.id) == user_id:
                    exists = True
        if exists == True:
            result = remove_simp(guild_id, user_id)
            if result == 200:
                await ctx.send(f'{arg} is not a simp anymore :C')
            if result == 404:
                await ctx.send(f'{arg} is not a simp!')
            else:
                await ctx.send(f'Weird... {result}')
        else:
            await ctx.send('User not found :C')

    #Remove user from simp list
    @commands.command(aliases=['isimp'])
    async def issimp(self, ctx):
        guild_id = str(ctx.message.guild.id)
        user_id = str(ctx.message.author.id)
        result = check_if_simp(guild_id, user_id)
        await ctx.send(result)


def setup(client):
    client.add_cog(simp(client))
