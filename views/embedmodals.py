import discord


class EmbedModals(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Titre"))
        self.add_item(discord.ui.InputText(label="Contenu", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.children[0].value,
            description=self.children[1].value,
            color=discord.Color.orange()
        )

        await interaction.channel.send(embed=embed)
        await interaction.response.send_message(content="Envoyé avec succès !", ephemeral=True)


