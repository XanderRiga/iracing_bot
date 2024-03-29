from ..html_builder import *
from ..helpers import *
from bokeh.plotting import figure, output_file, save
from bokeh.io import export_png
from bokeh.palettes import Category20
from bokeh.models import Legend
import itertools
from selenium import webdriver
from datetime import datetime
from ..queries.irating_dicts import get_irating_dicts
from ..db_helpers import Guild
from ..models import Category


class IratingsDb:
    def __init__(self, log):
        self.log = log

    async def call(self, ctx, category):
        async with ctx.typing():
            if category not in ['road', 'oval', 'dirtroad', 'dirtoval']:
                ctx.send('The category should be one of `road`, `oval`, `dirtroad`, `dirtoval`')
                return

            try:
                guild = await Guild.get(discord_id=str(ctx.guild.id))
            except:
                await ctx.send('Looks like no one in this discord has data yet. '
                               'Try `!saveid` and `!update` to make sure at least one person is saved.')
                return

            category_model = Category.from_name(category)
            today = datetime.now()
            date_6mo_ago = months_before(today, 6)
            all_irating_dicts = await get_irating_dicts(guild, category_model)

            split_irating_dicts = [all_irating_dicts[x:x + 10] for x in range(0, len(all_irating_dicts), 10)]
            for irating_dicts in split_irating_dicts:
                await self.build_and_post_chart(ctx, irating_dicts, category_model, date_6mo_ago)

    async def build_and_post_chart(self, ctx, irating_dicts, category_model, date_6mo_ago):
        p = figure(
            title=f'{category_model.friendly_name()} iRatings',
            x_axis_type='datetime',
            x_range=(date_6mo_ago, datetime.now())
        )
        p.toolbar.logo = None
        p.toolbar_location = None
        legend = Legend(location=(0, -10))
        p.add_layout(legend, 'right')
        output_file('output_iratings.html')

        colors = itertools.cycle(Category20[20])

        for irating_dict in irating_dicts:
            for user_id, iratings_list in irating_dict.items():
                try:
                    member = ctx.guild.get_member(int(user_id))
                    datetimes = []
                    iratings = []
                    for irating in iratings_list:
                        datetimes.append(irating.datetime())
                        iratings.append(irating.value)

                    p.line(
                        datetimes,
                        iratings,
                        legend_label=member.display_name,
                        line_width=2,
                        color=next(colors)
                    )
                except:
                    continue

        filename = f'irating_graph_{ctx.guild.id}.png'
        export_png(p, filename=filename, webdriver=webdriver.Chrome(options=self.webdriver_options()))
        try:
            await ctx.send(file=discord.File(filename))
        except Exception as e:
            if e.status == 403:
                await ctx.send('This channel does not permit file upload. '
                               'Please enable `Attach Files` in settings or use another channel and try again')
            else:
                raise e
        cleanup_file(filename)

    def webdriver_options(self):
        options = webdriver.chrome.options.Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--headless")
        options.add_argument("--hide-scrollbars")
        return options
