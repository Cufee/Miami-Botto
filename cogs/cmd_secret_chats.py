import discord
import re
import asyncio
import sys
from discord.ext import commands, tasks
import datetime
from cogs.core_logger.logger import Logger
logger = Logger()


# Secret Chats cog
class secret_chats(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.message_cleanup.start()

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'secret_chats cog is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        message_text = message.clean_content
        if channel.name == 'selfie-channel':
            attachments = message.attachments
            re_filter = re.compile('https:\/\/....')
            if re_filter.match(message_text):
                attachments.append('link found')
            if not attachments:
                emoji = discord.utils.get(
                    message.guild.emojis, name='trg_removing30')
                # Adding a reaction 30 minutes before deletion
                await asyncio.sleep(1800)
                await message.add_reaction(emoji)
                # Waiting 24 hours before deleting message
                await asyncio.sleep(84600)
                await message.delete()
            else:
                emoji = discord.utils.get(
                    message.guild.emojis, name='saved')
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
            message.guild.emojis, name='remove')
        for role in member.roles:
            if role.name[-4:] == '_mod' and 'remove' in payload.emoji.name:
                await message.add_reaction(reaction)
                await message.remove_reaction(payload.emoji, member)
                break

    # Tasks

    @tasks.loop(minutes=15)
    async def message_cleanup(self):
        logger.log('clean up')
        time_interval = 31
        time_now = datetime.datetime.now()
        time_before = time_now - datetime.timedelta(minutes=time_interval)
        time_after = time_now - datetime.timedelta(minutes=time_interval*3)
        all_channels = self.client.get_all_channels()
        all_messages = []
        try:
            for channel in all_channels:
                if isinstance(channel, discord.channel.TextChannel):
                    messages = await channel.history().flatten()
                    all_messages = all_messages + messages
            for message in all_messages:
                remove_emoji = reaction = discord.utils.get(
                    message.guild.emojis, name='remove')
                for reaction in message.reactions:
                    if remove_emoji == reaction and reaction.me:
                        await reaction.message.delete()
            logger.log('clean up done')
        except:
            e = sys.exc_info()[0]
            logger.log(f'{e}\nclean up failed')

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
