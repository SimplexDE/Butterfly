from aiohttp import request
from nextcord.ext.commands import Cog, command, cooldown, BucketType
from nextcord import Embed
from loguru import logger as log


class Fun(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="ping",
             brief="Sends a \"Hi <user>\" message",
             description="Sends a \"Hi <user>\" message",
             aliases=['p'],
             usage="ping")
    async def ping(self, ctx):
        await ctx.send("Hi {}".format(ctx.author.mention))

    @command(name="joke",
             brief="Shows a joke",
             description="Shows a random joke",
             aliases=['j'],
             usage="joke")
    @cooldown(2, 15, BucketType.user)
    async def joke(self, ctx):
        URL = "https://some-random-api.ml/joke"

        async with request("GET", URL) as response:
            if response.status == 200:
                data = await response.json()

                fact_embed = Embed(title="Random joke",
                                   colour=ctx.author.colour)
                fact_embed.add_field(value=data["joke"],
                                     name="Joke")
                fact_embed.set_footer(icon_url=ctx.author.avatar,
                                      text="Jokes by: https://some-random-api.ml/")

                await ctx.send(embed=fact_embed)

            else:
                await ctx.send("API returned a {} status.".format(response.status))

    @command(name="fact",
             brief="Shows animal facts",
             description="Shows random facts for some animals",
             aliases=['f'],
             usage="fact <dog|cat|panda|fox|bird|koala>")
    @cooldown(2, 15, BucketType.user)
    async def fact(self, ctx, animal: str):
        if animal.lower() in ("dog", "cat", "panda", "fox", "bird", "koala"):
            URL = "https://some-random-api.ml/animal/{}".format(animal)

            async with request("GET", URL) as response:
                if response.status == 200:
                    data = await response.json()

                    fact_embed = Embed(title="{} Fact".format(animal),
                                       colour=ctx.author.colour)
                    fact_embed.add_field(value=data["fact"],
                                         name="Fact")
                    fact_embed.set_image(url=data["image"])
                    fact_embed.set_footer(icon_url=ctx.author.avatar,
                                          text="Facts by: https://some-random-api.ml/")

                    await ctx.send(embed=fact_embed)

                else:
                    await ctx.send("API returned a {} status.".format(response.status))
        else:
            await ctx.send(
                "No facts are available for {} | Available facts are: dog, cat, panda, fox, bird, koala".format(animal))

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
