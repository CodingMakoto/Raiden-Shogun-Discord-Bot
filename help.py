import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from discord.ui import Select, View

import mysql.connector

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_color = 0x402c4c
        self.db = mysql.connector.connect(
            host="HOST",
            user="USER",
            password="PASSWORD",
            database="DATABASE",
            auth_plugin="METHOD"
        )
        self.cursor = self.db.cursor()

    @slash_command(name="help", description="⚡ Request Raiden Shogun Help")
    async def help_command(self, ctx, command: Option(str, description="Get help about a specific command", required = False, default = '')):
        if command is None:
            title = "<:raidenchibi:1080897827238060053> So... you requested Raiden Shogun Help?"
            file = discord.File("/media/bot/images/avatar-wb.png", filename="avatar.png")
            help_embed = discord.Embed(
                title=title,
                description="You need my help? Well then select a category down there that can help you with your request <:raidenbird:1080897824440455288>\n\n**Help per Command**:\nAlso use: `/help <command name>` to get more information about a specific command. Details are also available on the Bot Website.\n\n**Useful Links**:\n• Raiden Shogun City ⚡: https://discord.gg/2AePNcphrs\n• Bot Website: https://raidenshogun.gitbook.io/docs",
                color=self.default_color
            )
            help_embed.set_thumbnail(url="attachment://avatar.png")
            category_select = Select(
                options=[
                    discord.SelectOption(label="Story", value="H", description="Start a new day in Inazuma", emoji="<:heizouimthebest:1081239099039547472>"),
                    discord.SelectOption(label="Shops", value="S", description="Meet new people and buy objects to collect them", emoji="<:ayatomilkteatime:1081241425846472704>"),
                    discord.SelectOption(label="Daily Quests", value="Q", description="Check your Daily Quests", emoji="<:paimonrelieved:1081240022423974008>"),
                    discord.SelectOption(label="Personnal", value="P", description="Everything about your Adventure and Real Genshin Impact Stats", emoji="<:raidenbird:1080897824440455288>")
                ],
                placeholder="Select a category...",
                min_values=1,
                max_values=1
            )

            async def category_select_callback(interaction):
                selected_value = interaction.data["values"][0]
                if selected_value == "H":
                    title = "<:heizouimthebest:1081239099039547472> Oh! You want to discover Inazuma Island?"
                    story_commands = discord.Embed(
                        title=title,
                        description="Here are the commands related to the Story. All of these commands are explained on the Bot Website <:raidenexplaining:1080898396342194208>\n> /story mode\n> /story profile\n> /story chapters\n> /story quests",
                        color=self.default_color
                    )
                    await interaction.response.send_message(embed=story_commands, ephemeral=True)

            category_view = View()
            category_view.add_item(category_select)
            category_select.callback = category_select_callback

            await ctx.respond(embed=help_embed, file=file, view=category_view, ephemeral=True)
        else:
            await ctx.respond("Ok.")
