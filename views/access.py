import discord
import config
import database




class Access(discord.ui.view):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label = "Accepter", style = discord.ButtonStyle.primary, emoji = "✅")
    async def on_accept_callback(self, button, interaction):
        dbInfo = await database.get_messages(interaction.message.id)

        if dbInfo is not None :
            await interaction.response.send_message("Vous avez déjà répondu à cette demande.", ephemeral = True)
            return
        
        user = self.bot.fetch_user(dbInfo[1])
        await user.send("Votre demande d'accès à été acceptée !")

        embed = discord.Embed(
            title = "Demande accéptée",
            description = f"**User :** {user.mention}\n**Par :** {interaction.user.mention}",
            color = discord.Color.green()
        )

        interaction.message.edit(embed = embed)