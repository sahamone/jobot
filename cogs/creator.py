import discord
from discord.ext import commands
from views import embedmodals


class Creator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    creator = discord.SlashCommandGroup(
        name = "creator",
        description = "Embed creator commands"
    )


    @creator.command(
        name="new",
        descriptipn="Génère un nouvel embed dans ce salon"
    )
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def new(self, ctx):
        modal = embedmodals.EmbedModals(title="Création d'un embed personalisé")
        await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(Creator(bot))
