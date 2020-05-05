# Discord py
import discord
from discord.ext import commands, tasks

# Cog specific
import os
import asyncio
from datetime import datetime, timedelta
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
        logger.log(f'[Beta] cmd_stream_channel cog is ready.')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        member = after
        guild = after.guild
        all_activities = before.activities + after.activities
        streaming = False
        for activity in all_activities:
            if isinstance(activity, discord.Streaming):
                streaming = True
                break
            continue
        if not streaming:
            return
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

        # Generates a lot of spam, disabling
        # Discord generates too many events and this code will spam DMs due to this. Setting a cool down timer did not help to resolve this issue, as those events drop at the same time
        # # Check if member in voice channel in current guild
        # dm_message = f':exploding_head: Wow, cool stream!\n\nIt will be announced in #{channel_name} on {guild} if you join a voice channel on our server during your stream :)'
        # if member.voice == None:
        #     # Remove post
        #     for old_message in messages:
        #         if member in old_message.mentions:
        #             await old_message.delete()
        #     # Send DM
        #     dm_channel = await member.create_dm()
        #     time_check = datetime.utcnow() - timedelta(minutes=15)
        #     dm_history = await dm_channel.history(after=time_check).flatten()
        #     if dm_history:
        #         return
        #     await dm_channel.send(dm_message)
        #     return
        # elif member.voice.channel.guild != guild:
        #     # Remove post
        #     for old_message in messages:
        #         if member in old_message.mentions:
        #             await old_message.delete()
        #     # Send DM
        #     dm_channel = await member.create_dm()
        #     time_check = datetime.utcnow() - timedelta(minutes=15)
        #     dm_history = await dm_channel.history(after=time_check).flatten()
        #     if dm_history:
        #         return
        #     await dm_channel.send(dm_message)
        #     return

        # # Determine user status change
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
            logger.log(f'{guild} {member} is still streaming')
            for old_message in messages:
                if member in old_message.mentions:
                    logger.log(
                        f'there is a post for {member} already, skipping')
                    return
            if channel:
                logger.log(f'making a new post for {member}')
                await channel.send(f'{member.mention} is playing {activity.game} on {activity.platform}!\n{activity.name.strip()}\n{activity.url}')
            return
        # If user stopped streaming, wait and check their status again
        if was_live and not is_live:
            logger.log(f'{member} stopped streaming')
            # Waiting
            await asyncio.sleep(300)
            current_activities = member.activities
            messages = await channel.history().flatten()
            is_live = False
            # Check current status again, to make sure the channel is actually offline
            for activity in current_activities:
                if isinstance(activity, discord.Streaming):
                    is_live = True
                    break
            if not is_live:
                for old_message in messages:
                    if member in old_message.mentions:
                        logger.log(f'deleting post for {member}')
                        await old_message.delete()
            return
        # If user started streaming, make a new post
        if not was_live and is_live:
            logger.log(f'{member} started streaming!')
            # Send announcement
            if channel:
                messages = await channel.history().flatten()
            else:
                messages = []
            for old_message in messages:
                if member in old_message.mentions:
                    logger.log(f'deleting post for {member}')
                    await old_message.delete()
            if channel:
                await channel.send(f'{member.mention} is playing {activity.game} on {activity.platform}!\n{activity.name.strip()}\n{activity.url}')
            return
        else:
            pass

    # Refresh user status event on channel join and leave, disabled due to issues with code above
    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #     guild = member.guild
    #     all_activities = member.activities
    #     streaming = False
    #     for activity in all_activities:
    #         if isinstance(activity, discord.Streaming):
    #             streaming = True
    #             break
    #         continue
    #     if not streaming:
    #         return
    #     if after.channel is None:
    #         role = discord.utils.get(guild.roles, name='refresh_event')
    #         await member.add_roles(role)
    #         await asyncio.sleep(1)
    #         await member.remove_roles(role)
    #         return
    #     if after.channel.guild is guild:
    #         role = discord.utils.get(guild.roles, name='refresh_event')
    #         await member.add_roles(role)
    #         await asyncio.sleep(1)
    #         await member.remove_roles(role)
    #         return


def setup(client):
    client.add_cog(cmd_stream_channel(client))
