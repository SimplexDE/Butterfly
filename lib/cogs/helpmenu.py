from typing import Optional

import nextcord
from nextcord import Embed
from nextcord.ext import menus
from nextcord.ext.commands import Cog, command


class buildHelpmenu(menus.ListPageSource):
    def __init__(self, data, thumbnail, botname):
        super().__init__(data, per_page=5)
        self.thumbnail = thumbnail
        self.botname = botname

    async def format_page(self, menu, entries):
        embed = Embed(title="{} Help".format(self.botname), colour=nextcord.Colour.dark_purple())
        for _item in entries:
            embed.add_field(name=_item[0], value="```{}```".format(_item[1]), inline=False)
        embed.set_footer(
            text=f'Page {menu.current_page + 1}/{self.get_max_pages()} | <> Required field, [<>] Optional field')
        embed.set_thumbnail(
            url=self.thumbnail)
        return embed


class Helpmenu(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @command(brief="Test baum", usage="TEst", hidden=True, enabled=False)
    async def button_embed_field(self, ctx):
        fields = []
        last_cmd = ""
        for _item in self.bot.all_commands.keys():
            _item_cmd = self.bot.get_command(_item)
            name = _item_cmd.name
            usage = _item_cmd.usage
            brief = _item_cmd.brief

            enabled = _item_cmd.enabled
            hidden = _item_cmd.hidden

            if _item_cmd == last_cmd:
                pass

            else:
                last_cmd = _item_cmd

                if brief is None:
                    brief = "No description"

                if usage is None:
                    usage = name

                elif not enabled:
                    if any([ctx.author.id in self.bot.owner_ids]):
                        usage = "Disabled..."
                        fields += [(brief, usage)]
                    pass

                elif hidden:
                    if any([ctx.author.id in self.bot.owner_ids]):
                        usage = "Hidden..."
                        fields += [(brief, usage)]
                    pass

                else:
                    fields += [(brief, usage)]

        pages = menus.ButtonMenuPages(
            source=self.MyEmbedFieldPageSource(fields),
            clear_buttons_after=True,
        )
        await pages.start(ctx)

    @command(name="help",
             brief="Shows help menu",
             description="Shows help for commands",
             aliases=['h'],
             usage="help [<Command>]")
    async def help(self, ctx, cmd: Optional[str]):
        if not cmd:
            fields = []
            last_cmd = ""
            for _item in self.bot.all_commands.keys():
                _item_cmd = self.bot.get_command(_item)
                name = _item_cmd.name
                usage = _item_cmd.usage
                brief = _item_cmd.brief

                enabled = _item_cmd.enabled
                hidden = _item_cmd.hidden

                if _item_cmd == last_cmd:
                    pass

                else:
                    last_cmd = _item_cmd

                    if brief is None:
                        brief = "No description"

                    if usage is None:
                        usage = name

                    elif not enabled:
                        if any([ctx.author.id in self.bot.owner_ids]):
                            usage = "Disabled..."
                            fields += [(brief, usage)]
                        pass

                    elif hidden:
                        if any([ctx.author.id in self.bot.owner_ids]):
                            usage = "Hidden..."
                            fields += [(brief, usage)]
                        pass

                    else:
                        fields += [(brief, usage)]

            pages = menus.ButtonMenuPages(
                source=buildHelpmenu(fields, self.bot.user.avatar, self.bot.user.name),
                clear_buttons_after=True,
            )
            await pages.start(ctx)

        if cmd:
            try:
                _item = self.bot.get_command(cmd)
            except None:
                return await ctx.send("Couldn't find that command.")
            name = _item.name
            brief = _item.brief
            desc = _item.description
            hidden = _item.hidden
            cog_name = _item.cog_name
            enabled = _item.enabled
            usage = _item.usage
            aliases = _item.aliases

            text = ""
            for _alias in aliases:
                text += "`" + _alias + "`, "
            length = len(text)
            length = length - 2
            text = text[:length]

            if desc is None:
                desc = "No description"

            HelpMessage = Embed(title="{} Help".format(self.bot.user.name), colour=nextcord.Colour.dark_purple())

            HelpMessage.add_field(name=
                                  "Basic Information about {}".format(name).capitalize(),
                                  value=
                                  "> `{}`\n"
                                  "\n"
                                  "> Name: `{}`\n"
                                  "> Usage: `{}`\n"
                                  "> Aliases: {}\n"
                                  "".format(desc, name, usage, text),
                                  inline=False)

            if any([ctx.author.id in self.bot.owner_ids]):
                HelpMessage.add_field(name=
                                      "Advanced Information about {}".format(name).capitalize(),
                                      value=
                                      "> Brief: `{}`\n"
                                      "> Hidden: `{}`\n"
                                      "> Cog Name: `{}`\n"
                                      "> Enabled: `{}`\n"
                                      "".format(brief, hidden, cog_name, enabled),
                                      inline=False)

            #
            # if usage is not None:
            #     HelpMessage.add_field(name="Usage", value="`{}`".format(usage), inline=False)
            # if enabled:
            #     HelpMessage.add_field(name="Active", value=":white_check_mark:", inline=False)
            # if not enabled:
            #     HelpMessage.add_field(name="Active", value=":negative_squared_cross_mark:", inline=False)
            # if hidden:
            #     HelpMessage.add_field(name="Hidden", value=":white_check_mark:", inline=False)
            # if ctx.author.id == 579111799794958377:
            #     if cog_name:
            #         HelpMessage.add_field(name="Cog", value='{}'.format(cog_name), inline=False)
            # if aliases:
            #     text = ""
            #     for _alias in aliases:
            #         text += "`" + _alias + "`, "
            #     length = len(text)
            #     length = length - 2
            #     text = text[:length]
            #     HelpMessage.add_field(name="Aliases", value='{}'.format(text), inline=False)

            HelpMessage.set_footer(
                text="{} {} | <> Required field, [<>] Optional field".format(self.bot.user.name, self.bot.VERSION),
                icon_url=ctx.author.avatar)

            HelpMessage.set_thumbnail(url=self.bot.user.avatar)

            await ctx.send(embed=HelpMessage)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("helpmenu")


def setup(bot):
    bot.add_cog(Helpmenu(bot))
