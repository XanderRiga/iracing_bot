import discord
from discord.ext import commands
import dotenv
import os
import sys
import traceback
import logging
from logdna import LogDNAHandler
from tortoise import Tortoise
from iracing_cog.db_helpers import generate_schemas

dotenv.load_dotenv()
logdna_key = os.getenv("LOGDNA_INGESTION_KEY")
log = logging.getLogger('logdna')
log.setLevel(logging.DEBUG)
handler = LogDNAHandler(logdna_key, {'hostname': os.getenv("LOG_LOCATION")})
log.addHandler(handler)

description = "iRacing Bot to compare yourself to your friends and keep up to date on weekly combos"

intents = discord.Intents.default()
intents.members = True


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, description=description, intents=intents)


@bot.event
async def on_ready():
    await generate_schemas()
    try:
        bot.load_extension('iracing_cog.iracing')
    except Exception as e:
        print(f'Failed to load iracing_cog.', file=sys.stderr)
        traceback.print_exc()
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_name = message.content[1:].split(' ')[0]  # ignore the ! and get the first word
    command_names = list(map(lambda c: c.name, list(bot.commands)))
    if message_name not in command_names:
        return

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, exception):
    traceback.print_exc()
    log.warning(f'command failed: {ctx.message.content} with exception: {exception}')
    await ctx.send('Whoops! Looks like something went wrong. '
                   'Use `!help` to learn about each command or wait and try again soon.')


bot.run(os.getenv('BOT_TOKEN'), bot=True, reconnect=True)
