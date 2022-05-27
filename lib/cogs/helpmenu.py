from typing import Optional

import nextcord
from loguru import logger
from nextcord import Embed
from nextcord.ext.commands import Cog, Bot, command


class Helpmenu(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @command(name="help",
             brief="Shows help menu",
             description="Shows help for commands",
             aliases=['h'],
             usage="help [<Command>]")
    async def help(self, ctx, cmd: Optional[str]):
        if not cmd:
            HelpMessage = Embed(title="{} Help".format(self.bot.user.name), colour=nextcord.Colour.dark_purple())

            cmds = 0
            last_cmd = ""

            for _item in self.bot.all_commands.keys():
                _item_cmd = self.bot.get_command(_item)
                name = _item_cmd.name
                usage = _item_cmd.usage
                brief = _item_cmd.brief
                hidden = _item_cmd.hidden
                enabled = _item_cmd.enabled

                if _item_cmd == last_cmd:
                    pass

                else:
                    last_cmd = _item_cmd

                    if brief is None:
                        brief = "No Data"

                    if usage is None:
                        usage = name

                    # length = len(brief)
                    # if length >= 22:
                    #     brief = brief[:22]
                    #     brief += "..."

                    if not hidden:
                        if enabled:
                            HelpMessage.add_field(name="{}".format(brief), value="```{}```".format(usage), inline=False)
                            cmds += 1
                        if not enabled:
                            if any([ctx.author.id in self.bot.owner_ids]):
                                cmds += 1
                                HelpMessage.add_field(name="{}".format(brief),
                                                      value="```Disabled...```".format(usage),
                                                      inline=False)
                    if hidden:
                        if any([ctx.author.id in self.bot.owner_ids]):
                            if enabled:
                                cmds += 1
                                HelpMessage.add_field(name="{}".format(brief),
                                                      value="```Hidden...```".format(usage),
                                                      inline=False)

                            if not enabled:
                                cmds += 1
                                HelpMessage.add_field(name="{}".format(brief),
                                                      value="```Hidden & Disabled...```".format(usage),
                                                      inline=False)

            HelpMessage.set_footer(
                text="{} {} | <> Required field, [<>] Optional field".format(self.bot.user.name, self.bot.VERSION),
                icon_url=ctx.author.avatar)

            HelpMessage.set_thumbnail(url=self.bot.user.avatar)

            await ctx.send(embed=HelpMessage)

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

            HelpMessage.set_footer(text="{} {} | <> Required field, [<>] Optional field".format(self.bot.user.name, self.bot.VERSION),
                                   icon_url=ctx.author.avatar)

            HelpMessage.set_thumbnail(url=self.bot.user.avatar)

            await ctx.send(embed=HelpMessage)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("helpmenu")


def setup(bot):
    bot.add_cog(Helpmenu(bot))
