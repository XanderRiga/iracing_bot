from ..db_helpers import init_tortoise
from datetime import datetime


async def get_irating_dicts(guild, category):
    irating_dicts = []
    async for driver in guild.drivers:
        irating_list = await driver.iratings.filter(category=category)
        current_irating = await get_current_irating_now(driver, category)
        irating_list.append(current_irating)
        irating_dicts.append({driver.discord_id: irating_list})

    # This sorts by the most recent irating, highest first
    return sorted(irating_dicts, key=lambda hash: list(hash.items())[0][1][-1].value, reverse=True)


async def get_current_irating_now(driver, category):
    """This takes the most recent irating and adds another data point of it
    for when this is run. That allows the graphs to not fall off if a driver
    hasn't raced super recently"""
    current_irating = await driver.current_irating(category)
    current_irating.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return current_irating
