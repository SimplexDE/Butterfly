from discord.ext.commands import Cog

from ..db import db


class Welcome(Cog):

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        await self.bot.get_channel(876844147812728895).send("Welcome {}..".format(member.mention))
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)

    @Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.get_channel(876844147812728895).send("{} left...".format(member.name))
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)


def setup(bot):
    bot.add_cog(Welcome(bot))
