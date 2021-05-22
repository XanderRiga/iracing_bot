from ..db_helpers import remove_user_from_guild

class RemoveUser:
  def __init__(self, pyracing, log):
    self.pyracing = pyracing
    self.log = log

  async def call(self, ctx, discord_id):
    await remove_user_from_guild(ctx.guild.id, discord_id)

    await ctx.send('Successfully removed the user from the leaderboard')
