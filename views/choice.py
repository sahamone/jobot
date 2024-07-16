import discord
from discord.ext import commands
import config
import database
from views import access


class Choice(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.config = config.get_config()

    @discord.ui.button(label = "Vidéaste", style = discord.ButtonStyle.primary, emoji = "🎥")
    async def on_videaste_callback(self, button, interaction):
        if await database.is_waiting(interaction.user.id) :
            embed = discord.Embed(
                title = "Erreur",
                description = "Vous ne pouvez pas adresser d'autres demandes d'accès tant que votre précédente demande est toujours en cours de vérification !",
                color = discord.Color.yellow()
            )

            await interaction.response.send_message(embed = embed, ephemeral = True)
            

        else :
            channel = self.bot.get_channel(self.config.get("roles").get("alertChannelId"))
            if channel is None : channel = await self.bot.fetch_channel(self.config.get("roles").get("alertChannelId"))


            embed = discord.Embed(
                title = "Nouvelle demande d'accès vidéastes",
                description = f"**User :** {interaction.user.mention}",
                color = discord.Color.blue()
            )


            adminRole = discord.utils.get(interaction.guild.roles, id = self.config.get("roles").get("adminRoleId"))
            message = await channel.send(content = adminRole.mention, embed = embed, view = access.Access(self.bot))
            await database.add_message(message.id, interaction.user.id)

            await interaction.response.send_message("Votre demande d'accès à été envoyée avec succès. Vous recevrez un message de confirmation bientôt !", ephemeral = True)