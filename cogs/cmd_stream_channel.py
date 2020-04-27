# Discord py
import discord
from discord.ext import commands, tasks

# Cog specific
import os
import json
import asyncio
import datetime
from cogs.core_logger.logger import Logger
logger = Logger()


# Secret Chats cog
class cmd_stream_channel(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'cmd_stream_channel cog is ready.')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        member = after
        guild = after.guild
        activities_after = after.activities
        activities_before = before.activities
        channel = discord.utils.get(
            guild.channels, name='live-streams')
        # Get channel message history, if a channel exists
        if channel:
            messages = await channel.history().flatten()
        else:
            messages = []
        # Ignored role
        ignored_role = discord.utils.get(
            guild.roles, name='live-streams-ignored')
        if ignored_role in member.roles:
            for old_message in messages:
                if member in old_message.mentions:
                    await old_message.delete()
            logger.log(f'{member} has ignored role')
            return
        # Determine user status change
        was_live = False
        is_live = False
        for activity in activities_before:
            if isinstance(activity, discord.Streaming):
                was_live = True
                break
        for activity in activities_after:
            if isinstance(activity, discord.Streaming):
                is_live = True
                break
        # If user status was not changed, check for an existing post and skip or make a new one
        if was_live and is_live:
            logger.log(f'{member} is still streaming')
            for old_message in messages:
                if member in old_message.mentions:
                    logger.log(
                        f'there is a post for {member} already, skipping')
                    return
                else:
                    for activity in activities_after:
                        if isinstance(activity, discord.Streaming):
                            logger.log(f'making a new post for {member}')
                            await channel.send(f'@here\n{member.mention} is live on {activity.platform}!\n{activity.name.strip()}\n{activity.url}')
                    return
            return
        # If user stopped streaming, delete message
        if was_live and not is_live:
            for old_message in messages:
                if member in old_message.mentions:
                    logger.log(f'deleting post for {member}')
                    await old_message.delete()
            logger.log(f'{member} stopped streaming')
            return
        # If user started streaming, make a new post
        if not was_live and is_live:
            logger.log(f'{member} started streaming!')
            for activity in activities_after:
                if isinstance(activity, discord.Streaming):
                    if channel:
                        time_after = datetime.datetime.now() - datetime.timedelta(hours=12)
                        messages = await channel.history(after=time_after).flatten()
                        post = True
                    else:
                        messages = []
                        post = False
                    if post:
                        for old_message in messages:
                            if member in old_message.mentions:
                                logger.log(f'deleting post for {member}')
                                await old_message.delete()
                        await channel.send(f'@here\n{member.mention} is live on {activity.platform}!\n{activity.name.strip()}\n{activity.url}')
            return
        else:
            pass


def setup(client):
    client.add_cog(cmd_stream_channel(client))
