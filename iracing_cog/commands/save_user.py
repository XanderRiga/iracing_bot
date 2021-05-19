class SaveUser:
  def __init__(self, save_name, save_id, pyracing, log):
    self.save_name = save_name
    self.save_id = save_id
    self.pyracing = pyracing
    self.log = log

  async def call(self, ctx, discord_member, iracing_name_or_id):
    if iracing_name_or_id.isnumeric():
      await self.save_id.call(ctx, discord_member, iracing_name_or_id)
    else:
      await self.save_name.call(ctx, discord_member, iracing_name_or_id)
