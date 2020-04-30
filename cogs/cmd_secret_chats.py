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
                # Waiting 24 hours before deleting message
                await asyncio.sleep(84600)
                emoji = discord.utils.get(
                    message.guild.emojis, name='remove')
                # Adding a reaction 30 minutes before deletion
                await message.add_reaction(emoji)
                # await asyncio.sleep(1800)
                # await message.delete()
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

    @tasks.loop(hours=1)
    async def message_cleanup(self):
        logger.log('clean up')
        time_interval_before = 0.5  # hours
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
