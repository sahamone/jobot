import discord
from discord.ext import commands
from dotenv import load_dotenv
import config
import database
from views import choice


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.get_config()




    @commands.Cog.listener()
    async def on_member_joint(self, member):
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
            title = "Demande d'accès",
            description = "Si vous êtes un membre de l'option cinéma, cliquez sur le bouton ci-dessous afin de demander les accès nécéssaire à l'équipe d'administration de ce serveur Discord.",
            color = discord.Color.blue()
        )

        view = choice.Choice(self.bot)

        message = await ctx.send(embed = embed, view = view)
        await message.pin()


        await database.init_conf((ctx.channel.id, message.id))

        await ctx.respond("Message initialisé !", ephemeral = True)




def setup(bot):
    bot.add_cog(Roles(bot))

        