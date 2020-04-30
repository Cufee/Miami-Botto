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
                await asyncio.sleep(120)
                emoji = discord.utils.get(
                    message.guild.emojis, name='remove')
                await message.add_reaction(emoji)
            else:
                emoji = discord.utils.get(
                    message.guild.emojis, name='saved')
                await message.add_reaction(emoji)

    # Tasks
    @tasks.loop(hours=1)
    async def message_cleanup(self):
        logger.log('secret chat clean up starting')
        time_interval_before = 24  # hours
        time_interval_after = 26  # hours
        time_now = datetime.datetime.utcnow()
        time_before = time_now - \
            datetime.timedelta(hours=time_interval_before)
        time_after = time_now - datetime.timedelta(hours=time_interval_after)
        all_channels = self.client.get_all_channels()
        all_messages = []
        try:
            for channel in all_channels:
                if isinstance(channel, discord.channel.TextChannel):
                    messages = await channel.history(before=time_before, after=time_after).flatten()
                    all_messages += messages
            for message in all_messages:
                remove_emoji = reaction = discord.utils.get(
                    message.guild.emojis, name='remove')
                for reaction in message.reactions:
                    users = await reaction.users().flatten()
                    if reaction.emoji == remove_emoji and self.client.user in users:
                        await message.delete()
            logger.log('secret chat clean up done')
        except:
            e = sys.exc_info()[0]
            logger.log(f'{e}\nsecret chat clean up failed')

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
