# Discord py
import discord
from discord.ext import commands, tasks

# Cog specific
import os
import json
import asyncio
import datetime


# Secret Chats cog
class cmd_stream_channel(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'cmd_stream_channel cog is ready.')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        member = after
        activities_after = after.activities
        activities_before = before.activities
        guild = after.guild
        channel = discord.utils.get(
            guild.channels, name='live-streams')
        if channel:
            messages = await channel.history().flatten()
        else:
            messages = []

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

        if was_live and is_live:
            print(f'{member} was live and is live')
            return
        if was_live and not is_live:
            for old_message in messages:
                if member.mentioned_in(old_message):
                    await old_message.delete()
            print(f'{member} stopped streaming')
            return

        if not was_live and is_live:
            print(f'{member} started streaming!')
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
                            if member.mentioned_in(old_message):
                                await old_message.delete()
                        await channel.send(f'@here\n{member.mention} is live on {activity.platform}!\n{activity.url}')
            return
        else:
            pass


def setup(client):
    client.add_cog(cmd_stream_channel(client))
