import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from utils import config, database
from views import access, choice

# Loading environment variables
load_dotenv()

# Creating bot instance
intents = discord.Intents.default()
bot = discord.Bot(intents=intents)


# Bot event (ready event)
@bot.event
async def on_ready():
    print("Checking guild...")
    target_guild_id = int(os.getenv("GUILD"))
    bot_guilds = bot.guilds
    for guild in bot_guilds:
        if guild.id != target_guild_id:
            await guild.leave()
    print("done !")
    print("Updating views...")
    db = await database.get_database()
    alert_channel_id = config.get_config()["roles"]["alertChannelId"]
    alert_channel = bot.get_channel(alert_channel_id)
    for Id in db["messages"].keys():
        try:
            message = await alert_channel.fetch_message(int(Id))
            await message.edit(view=access.Access(bot))
        except Exception as e:
            print(f"Error updating message {id}: {e}")

    try:
        channel_id, message_id = db['init']
        channel = bot.get_channel(channel_id) or await bot.fetch_channel(channel_id)
        message = await channel.fetch_message(message_id)
        await message.edit(view=choice.Choice(bot))
    except Exception as e:
        print(f"Unable to fetch init message: {e}")
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        embed = discord.Embed(
            title="Error",
            description="You don't have the permission to use this command!",
            color=discord.Color.red()
        )

    elif isinstance(error, commands.errors.BotMissingPermissions):
        embed = discord.Embed(
            title="Error",
            description="I don't have enough permission to execute this command!",
            color=discord.Color.red()
        )

    else:
        embed = discord.Embed(
            title="Error",
            description="An unknown error has occurred!",
            color=discord.Color.red()
        )

    await ctx.respond(embed=embed, ephemeral=True)


@bot.event
async def on_guild_join(guild):
    if guild.id != int(os.getenv("GUILD")):
        await guild.leave()


@bot.command(
    name="deleteme",
    description="Delete all your personal information in the database"
)
@commands.guild_only()
async def deleteme(ctx):
    if await database.delete_user(ctx.author.id):
        await ctx.respond("Data deleted", ephemeral=True)
    else:
        await ctx.respond("No data to delete!", ephemeral=True)


bot.load_extension("cogs.roles")

# Bot running function
bot.run(os.getenv('DISCORD_TOKEN'))
