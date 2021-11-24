from ..html_builder import *
from ..interactors.image_from_string import image_from_string
from ..models import Stat, Driver, StatsType, Category


class YearlyStatsDb:
    def __init__(self, pyracing, log):
        self.pyracing = pyracing
        self.log = log

    async def call(self, ctx, iracing_id):
        try:
            async with ctx.typing():
                user_id = str(ctx.author.id)
                if not iracing_id:
                    try:

                        driver = await Driver.get(discord_id=user_id)
                        iracing_id = driver.iracing_id
                        if not iracing_id:
                            await ctx.send('Please send an iRacing ID after the command or '
                                           'link your own with `!saveid`')
                            return
                    except:
                        await ctx.send('Please send an iRacing ID after the command or '
                                       'link your own with `!saveid`')
                        return

                try:
                    driver = await Driver.get(iracing_id=iracing_id)
                    yearly_stats = await Stat.filter(driver=driver, stat_type=StatsType.yearly)
                except:
                    yearly_stats = await self.build_stats(iracing_id)

                if yearly_stats:
                    yearly_stats.sort(key=lambda x: x.year, reverse=True)
                    yearly_stats_html = get_yearly_stats_html_db(yearly_stats, iracing_id)
                    filename = f'{iracing_id}_yearly_stats.jpg'
                    image_from_string(yearly_stats_html, filename)
                    try:
                        await ctx.send(file=discord.File(filename))
                    except Exception as e:
                        if e.status == 403:
                            await ctx.send('This channel does not permit file upload. '
                                           'Please enable `Attach Files` in settings or use another channel and try again')
                        else:
                            raise e
                    cleanup_file(filename)
                else:
                    await ctx.send('No yearly stats found for user: ' + str(iracing_id))
        except Exception as e:
            self.log.info(f'Failed yearly stats(db) for {ctx}, exception: {e}')

    async def build_stats(self, iracing_id):
        """When we get a query for a user not in our DB, we have to do an API request"""
        yearly_stats_list = await self.pyracing.yearly_stats(iracing_id)
        stat_model_list = []

        for stat in yearly_stats_list:
            stat_model_list.append(Stat(
                category=Category.from_name(stat.category),
                stat_type=StatsType.yearly,
                avg_incidents=stat.incidents_avg,
                total_laps=stat.laps,
                laps_led=stat.laps_led,
                laps_led_percentage=stat.laps_led_pcnt,
                points_avg=stat.points_avg,
                points_club=stat.points_club,
                poles=stat.poles,
                avg_start_pos=stat.pos_start_avg,
                avg_finish_pos=stat.pos_finish_avg,
                total_starts=stat.starts,
                top_five_percentage=stat.top_5_pcnt,
                total_top_fives=stat.top_5s,
                win_percentage=stat.win_pcnt,
                total_wins=stat.wins,
                year=stat.year
            ))

        return stat_model_list
