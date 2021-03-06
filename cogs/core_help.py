import discord
from discord.ext import commands, tasks
from cogs.core_logger.logger import Logger
logger = Logger()


class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'help cog is ready.')

    # Commands
    # @commands.command(aliases=[''])
    @commands.command(aliases=['help'])
    async def _(self, ctx):
        await ctx.send('Help command is currently disabled', delete_after=10)
        await ctx.message.delete()


def setup(client):
    client.remove_command("help")
    client.add_cog(help(client))
