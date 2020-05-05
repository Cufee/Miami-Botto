import discord
from discord.ext import commands, tasks
import os
import csv
import re
from cogs.core_logger.logger import Logger
logger = Logger()


class role_weight(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.log(f'role_weight cog is ready.')

    # Commands
    @commands.command(hidden=True)
    @commands.has_permissions(view_audit_log=True)
    async def role(self, ctx, member_raw, role_raw):
        await ctx.message.delete()
        mod_member = ctx.author
        member_id_str = re.findall(r'\d+', member_raw)
        role_id_str = re.findall(r'\d+', role_raw)
        # Check if member_id and role_id match regex filter
        if not role_id_str or not member_id_str:
            await ctx.send(
                f'Looks like there is no such Member or Role. Make sure you are using @Member and @Role', delete_after=10)
            return
        member_id = int(member_id_str[0])
        role_id = int(role_id_str[0])
        member = discord.utils.get(ctx.guild.members, id=member_id)
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        # Check if member and role exist in guild
        if not member or not role:
            await ctx.send(
                f'Looks like there is no such Member or Role. Make sure you are using @Member and @Role', delete_after=10)
            return

        weight_filter = re.compile(r'#\d{2}')
        mod_highest_weight = 0
        for mod_role in mod_member.roles:
            mod_role_weight = re.findall(weight_filter, mod_role.name)
            if mod_role_weight and int(mod_role_weight[0][1:]) > mod_highest_weight:
                mod_highest_weight = int(mod_role_weight[0][1:])

        role_weight_str = re.findall(weight_filter, role.name)
        if not role_weight_str:
            await ctx.send(
                f'{role.mention} cannot be assigned manually.', delete_after=10)
            return
        role_weight = int(role_weight_str[0][1:])
        if mod_highest_weight < role_weight:
            await ctx.send(
                f'You do not have permission to assign {role.mention} to {member.mention}', delete_after=10)
            return

        print(mod_highest_weight)
        if mod_highest_weight > role_weight:
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f'Removed {role.mention} from {member.mention}.', delete_after=10)
                return
            if role not in member.roles:
                await member.add_roles(role)
                await ctx.send(f'Assigned {role.mention} to {member.mention}.', delete_after=10)
                return


def setup(client):
    client.add_cog(role_weight(client))
