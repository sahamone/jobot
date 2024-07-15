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
        channel = self.bot.get_channel(self.config.get("roles").get("alertChannelId"))
        if channel is None : channel = await self.bot.fetch_channel(self.config.get("roles").get("alertChannelId"))


        embed = discord.Embed(
            title = "Nouvelle demande d'accès vidéastes",
            description = f"**User :** {interaction.user.mention}",
            color = discord.Color.blue()
        )


        message = await channel.send(f"<@{self.config.get('roles').get('adminRoleId')}>", embed = embed, view = access.Access(self.bot))
        await database.add_message(message.id, interaction.user.id)

        await interaction.response.send_message("Votre demande d'accès à été envoyée avec succès. Vous recevrez un message de confirmation bientôt !", ephemeral = True)