import discord
from discord.ext import commands
from iracing_cog import Iracing

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

bot.run('NzA2NzMwNjYwNzg1NTUzNTE4.Xq-gNw.3bh26MNxmyiNsqa1k74SnSGXoJ4', bot=True, reconnect=True)
