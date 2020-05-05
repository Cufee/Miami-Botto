import discord
from discord.ext import commands, tasks
import random
import string
from cogs.core_logger.logger import Logger
logger = Logger()


async def generate_cid(stringLength=4):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))


class lfg_voice(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'[Beta] lfg_voice cog is ready.')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel_before = before.channel
        if not channel_before or not channel_before.name.startswith('LFG Voice'):
            return
        if not channel_before.members and channel_before.name.startswith('LFG Voice'):
            await channel_before.delete()
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        test_channel = 'lfg-voice'
        member = message.author
        if message.channel.name != test_channel or member == self.client.user:
            return
        if not member.voice:
            await message.channel.send(f'{member.mention}, you need to join a voice channel before posting here!', delete_after=15)
            await message.delete()
            return
        if message.clean_content.startswith('lf'):
            category = discord.utils.get(
                message.guild.categories, id=message.channel.category_id)
            user_message = f'```{message.clean_content}```'
            if len(message.clean_content) < 4:
                user_message = ''

            if message.clean_content[2].isdigit():
                channel_size = int(message.clean_content[2])
            if not message.clean_content[2].isdigit():
                channel_size = 3

            if member.voice.channel.name.startswith('LFG Voice'):
                await member.voice.channel.edit(user_limit=channel_size)
                voice_channel_invite = await member.voice.channel.create_invite(reason=f'LFG channel requested by {member.name}', unique=False)
                await message.channel.send(f'{member.mention} is looking for a group in {category.name}!\n{user_message}{voice_channel_invite}')
                await message.delete()
                return

            channel_name = f'LFG Voice {await generate_cid()}'
            voice_channel = await category.create_voice_channel(channel_name, user_limit=channel_size)
            voice_channel_invite = await voice_channel.create_invite(reason=f'LFG Voice channel requested by {member.mention}', unique=False)
            await message.channel.send(f'{member.mention} is looking for a group in {category.name}!\n{user_message}{voice_channel_invite}')
            await member.move_to(voice_channel, reason='LFG Voice channel requested by {member.name}')
            await message.delete()
            return
        else:
            await message.channel.send(f'{member.mention}! Your message needs to start with **lfg** or **lf(*Channel size*)**.', delete_after=15)
            await message.delete()


def setup(client):
    client.add_cog(lfg_voice(client))
