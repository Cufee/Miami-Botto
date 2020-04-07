import discord
from discord.ext import commands

# Dev cog

class dev(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'dev cog is ready.')

    #Commands
    @commands.command()
    #Gett current guid_id, channel_id, channel
    async def whereiam(self, ctx):
        guild_id = ctx.message.guild.id
        channel = ctx.message.channel
        channel_id = ctx.message.channel.id
        await ctx.send(f"guild_id: {guild_id}, channel_id: {channel_id}, channel: {channel}")

    @commands.command()
    #Gett current guid_id, channel_id, channel
    async def listemoji(self, ctx):
        embed = discord.Embed(
            title = f'{ctx.message.guild} emoji list',
            colour = discord.Colour.blue()
        )
        for emoji in ctx.guild.emojis:
            embed.add_field(name=emoji, value=emoji.id, inline=False)
        await self.client.say(embed=embed)

    @commands.command()
    #Gett current guid_id, channel_id, channel
    async def getid(self, ctx, arg:str):
            await ctx.send(f'{arg[3:-1]}')

    @commands.command()
    #Gett current guid_id, channel_id, channel
    async def split(self, ctx, arg:str):
            result = str(arg).split(':')
            await ctx.send(result)


def setup(client):
    client.add_cog(dev(client))
