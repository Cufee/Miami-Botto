# Discord py
import discord
from discord.ext import commands, tasks

# Cog specific
import os
import json
import asyncio
from datetime import datetime, timedelta
import rapidjson
from cogs.core_logger.logger import Logger
from cogs.core_multi_guild.guild_settings_parser import GetSettings

logger = Logger()
settings = GetSettings()


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
        # Check if user is/was streaming
        all_activities = before.activities + after.activities
        streaming = False
        for activity in all_activities:
            if isinstance(activity, discord.Streaming):
                streaming = True
                break
            continue
        if not streaming:
            return
        member = after
        guild = after.guild
        # Import guild setting
        guild_settings = await settings.parse(guild)
        channel_name = guild_settings.get('feature_flags').get(
            'cmd_stream_channel').get('channel_name')
        # Check if feature is enabled for guild
        feature_flag = guild_settings.get(
            'feature_flags').get('cmd_stream_channel')
        if not feature_flag:
            return
        activities_after = after.activities
        activities_before = before.activities
        channel = discord.utils.get(
            guild.channels, name=channel_name)
        # Get channel message history, if a channel exists
        if channel:
            messages = await channel.history().flatten()
        else:
            messages = []
        # Ignored role
        ignored_role = discord.utils.get(
            guild.roles, name=f'{channel_name}-ignored')
        if ignored_role in member.roles:
            for old_message in messages:
                if member in old_message.mentions:
                    await old_message.delete()
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
            if channel:
                time_after = datetime.now() - timedelta(hours=12)
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
