import discord
from dotenv import load_dotenv
import os
import database
import config
from views import access, choice



# Loading environment variables
load_dotenv()


# Creating bot instance
intents = discord.Intents.all()
bot = discord.Bot(intents = intents)


# Bot event (ready event)
@bot.event
async def on_ready():
    print("Checking guild...")
    for guild in bot.guilds:
        if guild.id != config.get_config()["guild"]:
            await guild.leave()
    print("done !")
    print("Updating views...")
    db = await database.get_database()
    for id in db["messages"].keys():
        message = await bot.get_channel(config.get_config()["roles"]["alertChannelId"]).fetch_message(int(id))
        await message.edit(view = access.Access(bot))


    try :
        channel = bot.get_channel(db['init'][0])
        if channel is None : channel = await bot.fetch_channel(db['init'][0])

        message = await channel.fetch_message(db['init'][1])
        await message.edit(view = choice.Choice(bot))
    except :
        print("Unable to fetch init message !")
    print(f'{bot.user} has connected to Discord!')



@bot.event
async def on_application_command_error(ctx, error):
    embed = discord.Embed(
        title = "Une erreur est survenue",
        description = f"```{error}```",
        color = discord.Color.red()
    )


    await ctx.respond(embed = embed, ephemeral = True)


@bot.event
async def on_guild_join(guild):
    if guild.id != config.get_config()["guild"]:
        await guild.leave()



@bot.event
async def on_message_delete(message):
    await database.remove_message(message.id, message.author.id)

bot.load_extension("cogs.roles")

# Bot running function
bot.run(os.getenv('DISCORD_TOKEN'))