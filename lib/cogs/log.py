from datetime import datetime

import nextcord
from nextcord import Embed
from nextcord.ext.commands import Cog


# Still work in progress, but most of the events are in here now..

def buildembed(title: str, description: str, colour: nextcord.Colour):
    return Embed(
        title=title,
        description=description,
        colour=colour,
        timestamp=datetime.utcnow()
    )


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
        embed = None
        fields = [()]

        if before.roles != after.roles:
            currentRoles = []
            newRoles = []

            for _role in before.roles:
                currentRoles += [_role]

            for _role in after.roles:
                newRoles += [_role]

            for _role in currentRoles:  # Role removed
                if _role not in newRoles:
                    embed = buildembed("{}#{} Updated".format(before.name, before.discriminator), "",
                                       nextcord.Colour.red())
                    fields = [("Removed from Role", _role.mention, False)]

            for _role in newRoles:  # Role added
                if _role not in currentRoles:
                    embed = buildembed("{}#{} Updated".format(before.name, before.discriminator), "",
                                       nextcord.Colour.green())
                    fields = [("Added to Role", _role.mention, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

        if before.display_name != after.display_name:
            embed = buildembed("{}#{} Updated".format(before.name,
                                                      before.discriminator),
                               "",
                               nextcord.Colour.orange())

            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.avatar != after.avatar:  # fixme (on_user_update, avatar update)
            embed = buildembed("{}#{} Updated".format(before.name,
                                                      before.discriminator),
                               ":warning: **THIS DOES NOT WORK CORRECTLY**",
                               # If you fix this, please set this(^) to ""
                               nextcord.Colour.orange())

            fields = [("Before", "[[before]]({})".format("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                       False),
                      ("After", "[[after]]({})".format("https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                       False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = buildembed("{}#{} Updated".format(before.name,
                                                      before.discriminator),
                               "* The title has the old discriminator and name",
                               nextcord.Colour.orange())

            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

        if before.name != after.name:
            embed = buildembed("{}#{} Updated".format(before.name,
                                                      before.discriminator),
                               "* The title has the old discriminator and name",
                               nextcord.Colour.orange())

            fields = [("Before", before.name, False),
                      ("After", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text=self.bot.VERSION)
            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, before, after):  # todo
        pass

    @Cog.listener()
    async def on_member_remove(self, before, after):  # todo
        pass

    @Cog.listener()
    async def on_message_edit(self, before, after):  # todo (rework)
        if not after.author.bot:
            pass
        if before.message != after.message:

            embed = Embed(title="Message Update",
                          description="Message updated by {}".format(after.author.name),
                          colour=after.colour,
                          timestamp=datetime.utcnow())

            fields = [("Before", before.message, False),
                      ("After", after.message, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):  # todo (rework)
        if not message.author.bot:
            embed = Embed(title="Message Deletion",
                          description="Message deleted by {}".format(message.author.name),
                          colour=message.author.colour,
                          timestamp=datetime.utcnow())

            fields = [("Deleted message", message.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_bulk_message_delete(self, messages):  # todo
        pass


def setup(bot):
    bot.add_cog(Log(bot))
