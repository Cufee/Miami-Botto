import discord
from discord.ext import commands, tasks
from cogs.core_logger.logger import Logger
logger = Logger()


class error_handle(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'error_handle cog is ready.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command not found.', delete_after=5)
        raise error

    # Commands
    @commands.command(aliases=[''])
    @commands.is_owner()
    async def error_handle(self, ctx, *, arg='null'):
        logger.log('Ran error_handle')


def setup(client):
    client.add_cog(error_handle(client))
