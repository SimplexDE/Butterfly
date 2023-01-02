import datetime

import nextcord
from loguru import logger as log
from nextcord import Interaction
from nextcord.ext.commands import Cog

guilds = [876844147812728892]




class About(Cog):

	def __init__(self, bot):
		self.bot = bot


	@nextcord.slash_command(name="about-us",
	                        description="About Butterfly",
	                        guild_ids=guilds,
	                        name_localizations={"de": "über-uns"},
	                        description_localizations={"de": "Über Butterfly [ENGLISCH]"},
	                        force_global=True,
	                        dm_permission=True)
	async def about_us(self, interaction: Interaction):

		emb = nextcord.Embed(title="About Butterfly",
		                     description="**Butterfly** is currently in *semi-active development*\n\nCurrently,"
		                                 " you can only use `/about-us`, but this will change in the future when\n"
		                                 " I unlock more features.",
		                     colour=nextcord.Colour.brand_green(),
		                     timestamp=datetime.datetime.utcnow())

		fields = [("Support-Server", "Soon...", False),
		          ("Developer", "Simplex#7008", False)]

		for field in fields:
			emb.add_field(name=field[0], value=field[1], inline=field[2])

		emb.set_thumbnail(self.bot.user.avatar)
		emb.set_footer(text="formerly MyNexus", icon_url=self.bot.user.avatar)

		await interaction.response.send_message(embed=emb, ephemeral=True)
		channel = self.bot.get_channel(979750917249310720)

		try:
			invite = await interaction.guild.invites()
			invite = invite[0].url
		except Exception as e:
			log.exception(e)
			invite = "NaN"
			pass

		await channel.send(
			"<@579111799794958377> ABOUT US COMMAND HAS BEEN USED!\n\nBy: {}#{} \nOn: {}\nInvite: {}".format(
				interaction.user.name,
				interaction.user.discriminator,
				interaction.guild.name,
				invite))


	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("about-us")




def setup(bot):
	bot.add_cog(About(bot))
