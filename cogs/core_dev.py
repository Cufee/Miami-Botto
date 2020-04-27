import rapidjson
import os
import discord
from discord.ext import commands

from cogs.core_logger.logger import Logger
from cogs.core_multi_guild.guild_settings_parser import GetSettings

logger = Logger()
settings = GetSettings()


async def settings_parser(guild_id):
    # Parse settings per guild
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/cogs/core_multi_guild/cache/guild_settings.json') as settings_json:
        try:
            guild_settings = rapidjson.load(settings_json).get(guild_id)
        except:
            guild_settings = rapidjson.load(settings_json).get('default')
    return guild_settings

# Dev cog


class dev(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'dev cog is ready.')

    # Commands
    @commands.command(hidden=True)
    @commands.is_owner()
    # Gett current guid_id, channel_id, channel
    async def whereiam(self, ctx):
        guild_id = ctx.message.guild.id
        channel = ctx.message.channel
        channel_id = ctx.message.channel.id
        await ctx.send(f"guild_id: {guild_id}, channel_id: {channel_id}, channel: {channel}")

    @commands.command(hidden=True)
    @commands.is_owner()
    # Gett current guid_id, channel_id, channel
    async def listemoji(self, ctx):
        embed = discord.Embed(
            title=f'{ctx.message.guild} emoji list',
            colour=discord.Colour.blue()
        )
        for emoji in ctx.guild.emojis:
            embed.add_field(name=emoji, value=emoji.id, inline=False)
        await self.client.say(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    # Gett current guid_id, channel_id, channel
    async def getemote(self, ctx, arg):
        arg = str(arg)
        logger.log(arg)
        await ctx.send(arg)

    @commands.command(hidden=True)
    @commands.is_owner()
    # Gett current guid_id, channel_id, channel
    async def split(self, ctx, arg: str):
        result = str(arg).split(':')
        await ctx.send(result)

    @commands.command(hidden=True)
    @commands.is_owner()
    # Gett current guid_id, channel_id, channel
    async def getroles(self, ctx):
        result = ctx.message.author.roles
        await ctx.send(result)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def toggle(self, ctx, feature):
        key = 'enabled'
        feature = f'cmd_{feature}'
        guild = ctx.guild
        result = await settings.update_feature(guild, feature, key)
        if result is None:
            await ctx.send(f'Unable to toggle {feature}, not a bool.')
            return
        await ctx.send(f'{feature} was set to {result}')

    @commands.command(hidden=True, aliases=['update-feature'])
    @commands.is_owner()
    async def update_feature(self, ctx, feature, key, value):
        feature = f'cmd_{feature}'
        guild = ctx.guild
        result = await settings.update_feature(guild, feature, key, value)
        if result is None:
            await ctx.send(f'Unable to toggle {feature}, result was {result}.')
            return
        await ctx.send(f'{feature} was set to {result}')


def setup(client):
    client.add_cog(dev(client))
