import discord
from dotenv import load_dotenv
import os



# Loading environment variables
load_dotenv()


# Creating bot instance
intents = discord.Intents.all()
bot = discord.Bot(intents = intents)


# Bot event (ready event)
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')



# Bot running function
bot.run(os.getenv('DISCORD_TOKEN'))