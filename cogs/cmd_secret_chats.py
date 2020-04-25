import discord
import re
import asyncio
import sys
from discord.ext import commands, tasks
import datetime

# Setup Guild
guild_id = ''


# Secret Chats cog

class secret_chats(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.message_cleanup.start()

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'secret_chats cog is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        message_text = message.clean_content
        if channel.name == 'selfie-channel' and ':beta_feature:' not in message_text:
            attachments = message.attachments
            re_filter = re.compile('https:\/\/....')
            if re_filter.match(message_text):
                attachments.append('link found')
            if not attachments:
                emoji = discord.utils.get(
                    message.guild.emojis, name='trg_removing30')
                await message.add_reaction(emoji)
            else:
                emoji = discord.utils.get(
                    message.guild.emojis, name='beta_feature')
                await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = f'{payload.message_id}'
        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(message_id)
        guild_id = payload.guild_id
        guild = discord.utils.find(
            lambda g: g.id == guild_id, self.client.guilds)
        member = discord.utils.find(
            lambda m: m.id == payload.user_id, guild.members)
        reaction = discord.utils.get(
            message.guild.emojis, name='trg_removing30')
        for role in member.roles:
            if role.name[-4:] == '_mod' and 'trg_removing' in payload.emoji.name:
                await message.add_reaction(reaction)
                await message.remove_reaction(payload.emoji, member)
                break

    # Tasks

    @tasks.loop(minutes=15)
    async def message_cleanup(self):
        print('clean up')
        time_interval = 31
        time_now = datetime.datetime.now()
        time_before = time_now - datetime.timedelta(minutes=time_interval)
        time_after = time_now - datetime.timedelta(minutes=time_interval*3)
        all_channels = self.client.get_all_channels()
        all_messages = []
        try:
            for channel in all_channels:
                if isinstance(channel, discord.channel.TextChannel):
                    messages = await channel.history(before=time_now, after=time_after).flatten()
                    all_messages = all_messages + messages
            for message in all_messages:
                remove_emoji = 'trg_removing'
                for reaction in message.reactions:
                    if remove_emoji in str(reaction.emoji) and reaction.me:
                        await message.delete()
            print('clean up done')
        except:
            e = sys.exc_info()[0]
            print(e, 'clean up failed')

    # Commands
    @commands.command(aliases=['pt'])
    async def purgetext(self, ctx, message_count):
        channel = ctx.channel
        if channel.name == 'selfie-channel':
            async for message in channel.history(limit=int(message_count)):
                message_text = message.clean_content
                attachments = message.attachments
                re_filter = re.compile('https:\/\/....')
                if re_filter.match(message_text):
                    attachments.append('link found')
                if not attachments:
                    await message.delete()
                else:
                    pass


def setup(client):
    client.add_cog(secret_chats(client))
