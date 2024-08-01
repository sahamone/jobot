import discord
from discord.ext import commands
from utils import config, database
from views import choice


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.get_config()




    @commands.Cog.listener()
    async def on_member_join(self, member):
        memberRole = discord.utils.get(member.guild.roles, id = self.config.get("roles").get("memberRoleId"))
        await member.add_roles(memberRole)

    rolesetup = discord.SlashCommandGroup(
        name = "rolesetup", 
        description = "Commandes de configuration des rôles"
    )

    @rolesetup.command(
        name = "init",
        description = "Initialise le message de demande d'accès"
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def init(self, ctx):
        embed = discord.Embed(
            title = self.config.get("messages").get("init").get("title"),
            description = self.config.get("messages").get("init").get("description"),
            color = discord.Color.blue()
        )

        view = choice.Choice(self.bot)

        message = await ctx.send(embed = embed, view = view)
        await message.pin()


        await database.init_conf((ctx.channel.id, message.id))

        await ctx.respond("Message initialisé !", ephemeral = True)


    @rolesetup.command(
        name = "giveall",
        description="Donne un certains rôle à tous les membres du serveur"
    )
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def giveall(self, ctx, role = discord.Option(discord.Role, "role", required = True)):
        guild = ctx.guild
        await ctx.respond(content = "Mise à jour en cours...", ephemeral = True)
        for member in guild.members:
            if role not in member.roles:
                await member.add_roles(role)

        await ctx.author.send(
            content="La mise à jour a été effectuée",
            ephemeral=True
        )









def setup(bot):
    bot.add_cog(Roles(bot))

        