import discord
from discord.ext import commands
import config
import database




class Access(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot



    @discord.ui.button(label = "Accepter", style = discord.ButtonStyle.primary, emoji = "✅")
    async def on_accept_callback(self, button, interaction):        
        dbInfo = await database.get_messages(interaction.message.id)
        print(dbInfo)

        if dbInfo is None :
            await interaction.response.send_message("Cette demande d'accès a deja été traitée !", ephemeral = True)
            return
        

        role = discord.utils.get(interaction.guild.roles, id = config.get_config()["roles"]["videasteRoleId"])
        member = await interaction.guild.fetch_member(dbInfo[1])
        user = await self.bot.fetch_user(dbInfo[1])
        await member.add_roles(role)
        
        await user.send("Votre demande d'accès à été acceptée !")

        embed = discord.Embed(
            title = "Demande accéptée",
            description = f"**User :** {user.mention}\n**Par :** {interaction.user.mention}",
            color = discord.Color.green()
        )

        await interaction.message.edit(embed = embed)
        await database.remove_message(interaction.message.id, dbInfo[1])


    @discord.ui.button(label = "Refuser", style = discord.ButtonStyle.danger, emoji = "❌")
    async def on_refuse_callback(self, button, interaction):
        dbInfo = await database.get_messages(interaction.message.id)

        if dbInfo is not None :
            await interaction.response.send_message("Vous avez déjà répondu à cette demande.", ephemeral = True)
            return
        
        user = await self.bot.fetch_user(dbInfo[1])
        await user.send("Votre demande d'accès à été refusée.")

        embed = discord.Embed(
            title = "Demande refusée",
            description = f"**User :** {user.mention}\n**Par :** {interaction.user.mention}",
            color = discord.Color.red()
        )

        await interaction.message.edit(embed = embed)
        await database.remove_message(interaction.message.id, dbInfo[1])