import asyncio

import discord
import nextcord
from nextcord.ext.commands import Bot as BotBase, CommandNotFound, Context
from nextcord import Embed, Intents, Colour, __version__

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

from loguru import logger as log

from ..db import db

PREFIX = "+"
OWNER_IDS = [
    579111799794958377,  # Simplex#7008
]
COGS = []
for file in os.listdir("./lib/cogs"):
    if file.endswith(".py"):
        if not file.startswith("-"):
            COGS += [file[:-3]]


class Ready(object):

    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        log.success("Ready [{}]".format(cog.upper()))

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):

    def __init__(self):
        self.PREFIX = PREFIX
        self.VERSION = ""
        self.TOKEN = ""
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all())

    def setup(self):
        for cog in COGS:
            try:
                self.load_extension("lib.cogs.{}".format(cog))
            except Exception as e:
                log.exception(e)

    def run(self, version):
        self.VERSION = version

        log.info("Running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        log.info("Initializing.")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("Currently starting up...")

    async def on_connect(self):
        await bot.change_presence(status=nextcord.Status.do_not_disturb,
                                  activity=nextcord.Activity(
                                      type=nextcord.ActivityType.playing,
                                      name="Startup Sequence..."))
        log.success("Connected.")

    async def on_disconnect(self):
        log.warning("Disconnected!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Wrong command")

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(917094047494074398)
            self.scheduler.start()

            channel = self.get_channel(978004248723873893)
            developer = ""
            for owner_id in OWNER_IDS:
                owner = self.get_user(owner_id)
                developer += owner.name + "#"
                developer += owner.discriminator + ", "
            developer = developer[:-2]

            embed = Embed(title="Startup complete",
                          description="{} is now Online.".format(bot.user.name),
                          colour=Colour.brand_green())

            fields = [("Name", bot.user.name, True),
                      ("Developer", developer, True),
                      ("Version", "`" + self.VERSION + "`", True),
                      ("Nextcord", "`" + __version__ + "`", True)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.set_footer(text="{} | {}".format(bot.user.name, self.VERSION), icon_url=bot.user.avatar)

            while not self.cogs_ready.all_ready():
                await asyncio.sleep(0.5)

            log.success("Ready [{}@{}]".format(bot.user.name, self.VERSION))
            self.ready = True
            await bot.change_presence(status=nextcord.Status.online,
                                      activity=nextcord.Activity(
                                          type=nextcord.ActivityType.watching,
                                          name="the sky | Version {}".format(self.VERSION)))
            await channel.send("Now online... :wave: || <@579111799794958377> ||", embed=embed)

        else:
            log.success("Reconnected.")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
