from datetime import datetime

from nextcord import Embed
from nextcord.ext.commands import Cog


# IMPORTANT NOTICE:
#
# This is not done.
# More functions are planned, because of that it is in its own branch atm.
# ~ Simplex
#


class Log(Cog):

    def __init__(self, bot):
        self.log_channel = None
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel = self.bot.get_channel(979750917249310720)
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:

            embed = Embed(title="Member updated",
                          description="Nickname change",
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            pass
        if before.message != after.message:

            embed = Embed(title="Message updated",
                          description="Message updated by {}".format(after.author.name),
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.message, False),
                      ("After", after.message, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = Embed(title="Message delete",
                          description="Message deleted by {}".format(message.author.name),
                          colour=message.author.colour,
                          timestamp=datetime.utcnow())

            fields = [("Deleted message", message.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Log(bot))
