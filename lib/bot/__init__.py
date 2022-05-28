import asyncio
import os

import nextcord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from boto.s3.connection import S3Connection
from loguru import logger as log
from nextcord import Embed, Intents, Colour
from nextcord.errors import HTTPException, Forbidden
from nextcord.ext.commands import Bot as BotBase, Context
from nextcord.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown, \
    DisabledCommand

from ..db import db

PREFIX = "-"
OWNER_IDS = [
    579111799794958377,  # Simplex#7008
]
COGS = []

for file in os.listdir("./lib/cogs"):
    if file.endswith(".py"):
        if not file.startswith("-"):
            COGS += [file[:-3]]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


class Ready(object):

    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
            log.info("{} changed READY Status to: {}".format(cog.capitalize(), False))

    def ready_up(self, cog):
        setattr(self, cog, True)
        log.info("{} changed READY Status to: {}".format(cog.capitalize(), True))
        log.success("Ready [{}]".format(cog.upper()))

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_ACCESS'])
token = os.environ['TOKEN']


class Bot(BotBase):

    def __init__(self):
        self.PREFIX = PREFIX
        self.VERSION = ""
        self.TOKEN = token
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.blocked = []

        db.autosave(self.scheduler)
        super().__init__(command_prefix=PREFIX,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all())

    def setup(self):
        for cog in COGS:
            try:
                log.info("Loading {}".format(cog))
                self.load_extension("lib.cogs.{}".format(cog))
            except Exception as e:
                log.info("Error occoured during loading of {}".format(cog))
                log.exception(e)

    def run(self, version):
        self.VERSION = version

        log.info("Starting setup...")
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
                                      name="Booting up..."))
        log.success("Connected.")

    async def on_disconnect(self):
        log.warning("Disconnected!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong. Please contact the Developer or check the console.")

        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, DisabledCommand):
            await ctx.send("> <:highpriority:979853981222309928> | That command is disabled.")

        elif isinstance(exc, CommandOnCooldown):
            user_id = str(ctx.message.author.id)

            if not self.blocked.get(user_id):
                self.blocked[user_id] = []

            if ctx.command.name in self.blocked[user_id]:
                return

            await ctx.send(
                f"> <:mediumpriority:979853981281042483> | That command is on {str(exc.type).split('.')[-1]} cooldown.\n"
                f"> <:info:979853981545299968> | You can execute it again in {exc.retry_after:,.2f} seconds.")

            self.blocked[user_id].append(ctx.command.name)
            await asyncio.sleep(2)  # 2 Sekunden blocken
            self.blocked[user_id].remove(ctx.command.name)

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("> <:mediumpriority:979853981281042483> | You're missing required arguments.")

        elif isinstance(exc.original, HTTPException):
            await ctx.send("> <:highpriority:979853981222309928> | Unable to send message.")

        elif isinstance(exc.original, Forbidden):
            await ctx.send(
                "> <:restrictionshield:979853982296055848> | I do not have the required permission for that.")

        else:
            raise exc.original

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(876844147812728892)
            self.scheduler.start()

            developer = ""
            for owner_id in OWNER_IDS:
                owner = self.get_user(owner_id)
                developer += owner.name + "#"
                developer += owner.discriminator + ", "
            developer = developer[:-2]

            embed_done = Embed(title="Ready!",
                               description="{} is ready.".format(bot.user.name),
                               colour=Colour.brand_green())

            fields = [("Developer", developer, True),
                      ("Version", "`" + self.VERSION + "`", True)]

            for name, value, inline in fields:
                embed_done.add_field(name=name, value=value, inline=inline)

            embed_done.set_footer(text="{} | {}".format(bot.user.name, self.VERSION), icon_url=bot.user.avatar)

            counter = 15
            halfcounter = round(counter / 2)

            errorsduringload = False

            while not self.cogs_ready.all_ready():
                await asyncio.sleep(0.5)
                counter -= 1
                if counter == halfcounter:
                    log.warning("It already took {} seconds to load.".format(halfcounter))
                if counter <= -1:
                    log.error("Errors encountered during startup, not all cogs are available.")
                    errorsduringload = True
                    break

            if errorsduringload:
                embed_done.add_field(name=":warning: Completed with errors",
                                     value="The bot started with errors,"
                                           " check console for more information",
                                     inline=False)
            else:
                embed_done.add_field(name=":white_check_mark: Completed without errors.",
                                     value="No errors during loading detected.",
                                     inline=False)

            log.success("Ready [{}@{}]".format(bot.user.name, self.VERSION))
            self.ready = True
            await bot.change_presence(status=nextcord.Status.online,
                                      activity=nextcord.Activity(
                                          type=nextcord.ActivityType.watching,
                                          name="the flowers | Version {}".format(self.VERSION)))

            channel = self.get_channel(979750917249310720)
            await channel.send(embed=embed_done)

        else:
            log.success("Reconnected.")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
