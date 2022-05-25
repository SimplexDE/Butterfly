import nextcord.http
from nextcord.ext.commands import Bot as BotBase, CommandNotFound
from nextcord import Embed, Intents, Colour, __version__

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loguru import logger as log

PREFIX = "+"
OWNER_IDS = [
    579111799794958377, # Simplex#7008
    ]


class Bot(BotBase):

    def __init__(self):
        self.PREFIX = PREFIX
        self.VERSION = ""
        self.TOKEN = ""
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all())

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        log.info("Initializing.")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
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
            self.ready = True
            self.guild = self.get_guild(917094047494074398)
            log.success("Ready [{}]".format(self.VERSION))

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

            await channel.send("Now online... :wave: || <@579111799794958377> ||", embed=embed)

        else:
            log.success("Reconnected.")

    async def on_message(self, message):
        pass


bot = Bot()
