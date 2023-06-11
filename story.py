import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
from discord.ui import Select, View, Button

import mysql.connector
import json

class StoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_color = 0x402c4c
        self.mydb = mysql.connector.connect(
            host="HOST",
            user="USER",
            password="PASSWORD",
            database="DATABASE",
            auth_plugin="METHOD"
        )
        self.cursor = self.mydb.cursor()
        self.file = open('chapters.json')
        self.user_chapter = json.load(self.file)

    account = SlashCommandGroup(
        "account", "Everything about your Account"
    )

    story = SlashCommandGroup(
        "story", "Your adventure with Raiden Shogun"
    )

    @account.command(name="start", description="🔍 Want to discover a new adventure ?")
    async def start(self, ctx, language: discord.Option(str, "What language do you want ?", choices=[Option(str, "Défini la langue en Français", name="Français", value="Français"), Option(str, "Set English language", name="English", value="English")]), name=None):
        self.cursor.execute(f"SELECT `NAME`, `LANG` FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
        account_exists = self.cursor.fetchone()

        if account_exists:
            lang = account_exists["LANG"]
            if lang == "English":
                warning = discord.Embed(description="<:raidenangry:1080897820854329376> Your account is already open, to reset it use : `/account end`", color=self.default_color)
                await ctx.respond(embed=warning, ephemeral=True)
            elif lang == "Français":
                warning = discord.Embed(description="<:raidenangry:1080897820854329376> Votre compte est déjà ouvert, pour le réinitialiser utilisez : `/account end`", color=self.default_color)
                await ctx.respond(embed=warning, ephemeral=True)
        else:
            if language == "English":
                if name is not None:
                    self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `NAME`, `CHAPTER`, `MORAS`, `PRIMOS`, `BOSSES`, `HEALTH`, `STATUES`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '{name}', '1', '0', '0', '0', '10000', '0', 'English')")
                    self.mydb.commit()
                    creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Your account has been created successfully {ctx.author.mention}, you chose: `{name}` as adventure name and `{language}` as language. Now you can start your adventure in Inazuma with: `/story mode`", color=self.default_color)
                    await ctx.respond(embed=creation)
                else:
                    self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `NAME`, `CHAPTER`, `MORAS`, `PRIMOS`, `BOSSES`, `HEALTH`, `STATUES`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '{ctx.author.name}', '1', '0', '0', '0', '10000', '0', 'English')")
                    self.mydb.commit()
                    creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Your account has been created successfully {ctx.author.mention}, you chose: `{language}` as language. Now you can start your adventure in Inazuma City with: `/story mode`", color=self.default_color)
                    await ctx.respond(embed=creation)

            elif language == "Français":
                if name is not None:
                    self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `NAME`, `CHAPTER`, `MORAS`, `PRIMOS`, `BOSSES`, `HEALTH`, `STATUES`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '{name}', '1', '0', '0', '0', '10000', '0', 'Français')")
                    self.mydb.commit()
                    creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Votre compte a été créé avec succès {ctx.author.mention}, vous avez choisi: `{name}` comme nom d’aventure et `{language}` comme langue. Maintenant vous pouvez commencer votre aventure à Inazuma avec: `/story mode`", color=self.default_color)
                    await ctx.respond(embed=creation)
                else:
                    self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `NAME`, `CHAPTER`, `MORAS`, `PRIMOS`, `BOSSES`, `HEALTH`, `STATUES`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '{ctx.author.name}', '1', '0', '0', '0', '10000', '0', 'Français')")
                    self.mydb.commit()
                    creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Votre compte a été créé avec succès {ctx.author.mention}, vous avez choisi: `{language}` comme langue. Maintenant vous pouvez commencer votre aventure à Inazuma avec: `/story mode`", color=self.default_color)
                    await ctx.respond(embed=creation)

    @account.command(name="end", description="🚪 Close the door of Inazuma City")
    async def end(self, ctx):
        self.cursor.execute(f"SELECT `NAME`, `LANG` FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
        account_exists = self.cursor.fetchone()

        if account_exists:
            language = account_exists["LANG"]
            if language == "Français":
                async def yes_callback(interaction):
                    delete = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Votre compte a été supprimé avec succès {ctx.author.mention}", color=self.default_color)
                    self.cursor.execute(f"DELETE FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
                    self.mydb.commit()
                    await interaction.response.send_message(embed=delete, ephemeral=True)

                async def no_callback(interaction):
                    stop = discord.Embed(description=f"Supression du Compte Annulée {ctx.author.mention}", color=self.default_color)
                    await interaction.response.send_message(embed=stop, ephemeral=True)

                confirm = discord.Embed(description=f"Êtes-vous sûr de vouloir supprimer votre compte ? {ctx.author.mention}", color=self.default_color)
                no = Button(label="Nonnnn", style=discord.ButtonStyle.danger)
                yes = Button(label="Oui avec une grande tristesse...", style=discord.ButtonStyle.green)
                no.callback = no_callback
                yes.callback = yes_callback
                view = View()
                view.add_item(no)
                view.add_item(yes)
                await ctx.respond(embed=confirm, view=view, ephemeral=True)

            elif language == "English":
                async def yes_callback(interaction):
                    delete = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Your account has been deleted successfully {ctx.author.mention}", color=self.default_color)
                    self.cursor.execute(f"DELETE FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
                    self.mydb.commit()
                    await interaction.response.send_message(embed=delete, ephemeral=True)

                async def no_callback(interaction):
                    stop = discord.Embed(description=f"Account Supression Cancelled {ctx.author.mention}", color=self.default_color)
                    await interaction.response.send_message(embed=stop, ephemeral=True)

                confirm = discord.Embed(description=f"Are you sure you want to delete your account? {ctx.author.mention}", color=self.default_color)
                no = Button(label="Nooooo", style=discord.ButtonStyle.danger)
                yes = Button(label="Yes unfortunately...", style=discord.ButtonStyle.green)
                no.callback = no_callback
                yes.callback = yes_callback
                view = View()
                view.add_item(no)
                view.add_item(yes)
                await ctx.respond(embed=confirm, view=view, ephemeral=True)

        else:
            warning = discord.Embed(description="<:raidenangry:1080897820854329376> You do not have an account to delete", color=self.default_color)
            await ctx.respond(embed=warning, ephemeral=True)

    @story.command(name="mode", description="🗺️ Explore the New Inazuma City !")
    async def mode(self, ctx):
        self.cursor.execute(f"SELECT `NAME`, `LANG`, `CHAPTER` FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
        account_exists = self.cursor.fetchone()

        if account_exists:
            lang = account_exists["LANG"]
            chapter = int(account_exists["CHAPTER"])

            if lang == "English":
                if chapter == 1:
                    no = Button(label="Wait... I'm not sure", style=discord.ButtonStyle.danger, emoji="<:raidenangry:1080897820854329376>")
                    yes = Button(label="I'm ready!", style=discord.ButtonStyle.primary, emoji="<:raidenbird:1080897824440455288>")
                    view = View()
                    view.add_item(no)
                    view.add_item(yes)

                elif chapter == 2:
                    button = Button(label="Test", style=discord.ButtonStyle.primary, emoji="<:raidenbird:1080897824440455288>")
                    view = View()
                    view.add_item(button)

                story = discord.Embed(description=self.user_chapter["English"][f"{chapter}"]["story"], color=self.default_color)
                file = discord.File(f"/media/bot/images/story/{chapter}-english.jpg", filename="story-english.jpg")
                story.set_image(url="attachment://story-english.jpg")

            elif lang == "Français":
                if chapter == 1:
                    no = Button(label="Attends... je ne suis pas sûr", style=discord.ButtonStyle.danger, emoji="<:raidenangry:1080897820854329376>")
                    yes = Button(label="Je suis prêt(e)!", style=discord.ButtonStyle.primary, emoji="<:raidenbird:1080897824440455288>")
                    view = View()
                    view.add_item(no)
                    view.add_item(yes)

                elif chapter == 2:
                    button = Button(label="Test", style=discord.ButtonStyle.primary, emoji="<:raidenbird:1080897824440455288>")
                    view = View()
                    view.add_item(button)

                story = discord.Embed(description=self.user_chapter["Francais"][f"{chapter}"]["story"], color=self.default_color)
                file = discord.File(f"/media/bot/images/story/{chapter}.jpg", filename="story.jpg")
                story.set_image(url="attachment://story.jpg")

            await ctx.respond(file=file, embed=story, view=view)

        else:
            warning = discord.Embed(description="<:raidenangry:1080897820854329376> You do not have an account to explore Inazuma Island", color=self.default_color)
            await ctx.respond(embed=warning, ephemeral=True)
