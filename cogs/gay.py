import discord
import random
from discord.ext import commands

# Gay cog

class gay(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'gay cog is ready.')

    #Commands
    @commands.command()
    async def gay(self, ctx, *, arg = 'null'):
        '''Check if a user is gay.'''
        responses = ['As I see it, yes.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Concentrate and ask again.',
                    'I like trains.',
                    'Don’t count on it.',
                    'It is certain.',
                    'It is decidedly so.',
                    'Most likely.',
                    'My reply is no.',
                    'My sources say no.',
                    f'Outlook not so good.',
                    'Reply hazy, try again.',
                    'Dicks point to yes.',
                    'Very doubtful.',
                    'Without a doubt.',
                    'Yes.',
                    'Yes – definitely.',
                    'You may rely on it. :smirk:']
        if arg == 'null':
            await ctx.send('Are you?\nUse -gay @name')
        else:
            await ctx.send(random.choice(responses))
        print('Ran gay')

def setup(client):
    client.add_cog(gay(client))



