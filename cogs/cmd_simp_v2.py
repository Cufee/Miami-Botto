# Discord py
import asyncio
import json
import os
import discord
from discord.ext import commands, tasks
from cogs.core_logger.logger import Logger
logger = Logger()

# Cog specific

# Debug mode for printig additional info
global debug
debug = True

# Server settings json path
global guild_settings_json
guild_settings_json = f"{os.getcwd()}/cogs/cmd_simp_v2/guild_settings.json"

# Fetch guild settings


def fetch_guild_settings(guild_id):
    # Open json file and find settings by guild_id
    with open(guild_settings_json, 'r') as all_guild_settings_json:
        all_guild_settings = json.load(all_guild_settings_json)
    for guild in all_guild_settings:
        # Return settings as Object and status code
        if all_guild_settings.get(guild).get('guild_id') == guild_id:
            guild_settings = all_guild_settings.get(guild)
            status_code = 200
            break
        else:
            guild_settings = {404: "Not found"}
            status_code = 404
    return guild_settings, status_code


# Secret Chats cog
class simp(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'[Beta] simp_v2 cog is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id = f'{message.guild.id}'
        channel = message.channel
        message_author = message.author
        message_author_roles = message.author.roles

        # Ignore messages sent by this bot
        if message_author == self.client.user:
            logger.log(f'Message was sent by {self.client.user}')
        else:
            # Fetch guild settings
            guild_settings, status_code = fetch_guild_settings(guild_id)
            if status_code != 200:
                # Check response code
                logger.log(f'fetch_guild_settings returned {status_code}')
            else:
                simp_enabled = guild_settings.get('simp_enabled')
                ignored_roles = guild_settings.get('ignored_roles')
                simp_role = guild_settings.get('simp_role')
                simp_emote = guild_settings.get('simp_emote')

                if simp_enabled == False:
                    # Check if simp module is enabled on a server
                    logger.log(f'simp_enabled {simp_enabled}')
                elif all(role in ignored_roles for role in str(message_author_roles)) == True:
                    # Check if a user role is in ignored_roles
                    logger.log(
                        f'User role is in ignored_roles {ignored_roles}')
                elif simp_role in str(message_author_roles):
                    message_history = []
                    async for old_message in channel.history(limit=5):
                        if old_message.author == message_author:
                            message_history.append(old_message)
                    if len(message_history) > 1:
                        last_message = message_history[1]
                        logger.log(f'Removing reaction')
                        await last_message.remove_reaction(simp_emote, self.client.user)
                    logger.log('Adding reaction')
                    await message.add_reaction(simp_emote)
                else:
                    pass

    # Loops
    # @tasks.loop(seconds=5.0)

    # Commands
    # @commands.command()
    @commands.command(aliases=['simp?'])
    async def _simp(self, ctx):
        # Check if user has simp role
        guild_id = f'{ctx.message.guild.id}'
        message_author_roles = f'{ctx.message.author.roles}'
        guild_settings, status_code = fetch_guild_settings(guild_id)
        simp_role = guild_settings.get('simp_role')
        if status_code != 200:
            logger.log(f'fetch_guild_settings returned {status_code}')
            result = False
        elif simp_role in message_author_roles:
            result = True
        else:
            result = False
        await ctx.send(result)


def setup(client):
    client.add_cog(simp(client))
