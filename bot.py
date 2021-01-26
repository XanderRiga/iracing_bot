import discord
from discord.ext import commands
from iracing_cog import Iracing
import dotenv
import os

dotenv.load_dotenv()


description = "iRacing Bot to compare yourself to your friends and keep up to date on weekly combos"

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', description=description, intents=intents)

bot.load_extension('iracing_cog.iracing')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

bot.run(os.getenv('BOT_TOKEN'), bot=True, reconnect=True)
