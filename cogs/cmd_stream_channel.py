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
                print(f'{member} was live')
                was_live = True
                break
        for activity in activities_after:
            if isinstance(activity, discord.Streaming):
                print(f'{member} is live')
                is_live = True
                break

        if was_live and is_live:
            print(f'{member} is still streaming')
            for old_message in messages:
                if member in old_message.mentions:
                    print(f'there is a post for {member} already, skipping')
                    return
                else:
                    for activity in activities_after:
                        if isinstance(activity, discord.Streaming):
                            print(f'making a new post for {member}')
                            await channel.send(f'@here\n{member.mention} is live on {activity.platform}!\n{activity.name.strip()}\n{activity.url}')
                    return
            return

        if was_live and not is_live:
            for old_message in messages:
                if member in old_message.mentions:
                    print(f'deleting post for {member}')
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
                            if member in old_message.mentions:
                                print(f'deleting post for {member}')
                                await old_message.delete()
                        await channel.send(f'@here\n{member.mention} is live on {activity.platform}!\n{activity.name.strip()}\n{activity.url}')
            return
        else:
            pass


def setup(client):
    client.add_cog(cmd_stream_channel(client))
