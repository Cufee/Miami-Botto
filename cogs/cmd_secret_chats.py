import discord
import re
import asyncio
from discord.ext import commands

# Setup Guild
guild_id = ''


# Secret Chats cog

class secret_chats(commands.Cog):

    def __init__(self, client):
        self.client = client

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
                await asyncio.sleep(1800)
                await message.delete()
            else:
                emoji = discord.utils.get(
                    message.guild.emojis, name='beta_feature')
                await message.add_reaction(emoji)

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
