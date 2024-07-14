import discord
from discord.ext import commands
from dotenv import load_dotenv
import config


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.get_config()




    @commands.Coh.listener()
    async def on_member_joint(self, member):
        memberRole = discord.utils.get(member.guild.roles, id = self.config.get("roles").get("memberRoleId"))
        await member.add_roles(memberRole)