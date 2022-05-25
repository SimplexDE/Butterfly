from nextcord.ext.commands import Cog, command
from loguru import logger as log


class Fun(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="ping", aliases=["p"])
    async def ping(self, ctx):
        await ctx.send("Hi")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
