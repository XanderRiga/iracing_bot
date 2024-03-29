from ..html_builder import *
from ..interactors.image_from_string import image_from_string
import traceback
from ..db_helpers import init_tortoise, Guild, Tortoise


class CurrentSeriesDb:
    def __init__(self, log):
        self.log = log

    async def call(self, ctx):
        try:

            guild = await Guild.get(discord_id=ctx.guild.id)

            favorite_series = await guild.favorite_series.all()
            if not favorite_series:
                await ctx.send('Follow the directions by calling `!setfavseries` to set favorite'
                               'series before using this command')
                return

            this_week_string = await build_race_week_string_db(favorite_series, 'This Week', self.log, 0)
            next_week_string = await build_race_week_string_db(favorite_series, 'Next Week', self.log, 1)

            if not this_week_string and not next_week_string:
                await ctx.send('Looks like there are no combos right now. '
                               'It might be week 13 or iRacing might be down. '
                               'If neither of those are the issue, try again soon')
                return

            if this_week_string:
                this_week_filename = f'{ctx.guild.id}_this_week.jpg'
                image_from_string(this_week_string, this_week_filename)
                try:
                    await ctx.send(file=discord.File(this_week_filename))
                except Exception as e:
                    if e.status == 403:
                        await ctx.send('This channel does not permit file upload. '
                                       'Please enable `Attach Files` in settings or use another channel and try again')
                        return
                    else:
                        raise e
                cleanup_file(this_week_filename)

            if next_week_string:
                next_week_filename = f'{ctx.guild.id}_next_week.jpg'
                image_from_string(next_week_string, next_week_filename)
                await ctx.send(file=discord.File(next_week_filename))
                cleanup_file(next_week_filename)

        except Exception as e:
            self.log.warning(f'Current series failed: {e}')
            traceback.print_exc()
