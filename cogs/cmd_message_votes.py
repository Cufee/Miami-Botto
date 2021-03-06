import discord
import re
from discord.ext import commands, tasks


async def get_vote_channels(guild_id):
    test_channel = 'memes'
    vote_channels = [test_channel]
    return vote_channels


class message_votes(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[Beta] help cog is ready.')

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel.name
        attachments = message.attachments
        vote_channels = await get_vote_channels('guild_id here')
        re_filter = re.compile('https:\/\/....')

        if re_filter.match(message.clean_content):
            attachments.append('link found')

        if channel in vote_channels and attachments:
            print('new message in memes with an attachment')
            emotes = [discord.utils.get(message.guild.emojis, name='upvote'), discord.utils.get(
                message.guild.emojis, name='downvote')]
            if emotes:
                for emote in emotes:
                    await message.add_reaction(emote)
            else:
                print('failed to find emotes')
        else:
            pass


def setup(client):
    client.add_cog(message_votes(client))
