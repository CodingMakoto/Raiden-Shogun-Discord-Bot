import discord
from discord.ext import commands
from discord import Option
from discord.commands import SlashCommandGroup
from discord.ui import Select, View, Button
import random

import mysql.connector
import json

class StoryCog(discord.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_color = 0x37266a
        self.mydb = mysql.connector.connect(
            host="HOST",
            user="USER",
            password="PASSWORD",
            database="DATABASE",
            auth_plugin="METHOD"
        )
        self.cursor = self.mydb.cursor()
        self.chapter = open('chapters.json')
        self.chapter_loaded = json.load(self.chapter)
        self.quests = open('quests.json')
        self.quests_loaded = json.load(self.quests)

    account = SlashCommandGroup(
        "account", "Everything about your Account"
    )

    story = SlashCommandGroup(
        "story", "Your adventure with Raiden Shogun"
    )

    @account.command(name="start", description="🔍 Want to discover a new adventure ?")
    async def a_start(self, ctx, language: Option(str, "What language do you want ?", choices=["Français","English"]), uid: Option(str, "You can enter your real UID to be used with other commands", required=False), name: Option(str, "You can choose a name for this adventure", required=False)):
        self.mydb.ping(reconnect=True)
        self.cursor.execute(f"SELECT `LANG` FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
        account_exist = self.cursor.fetchone()

        if account_exist is not None:
            self.cursor.execute(f"SELECT `LANG` FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
            lang_fetch = self.cursor.fetchall()
            for langs in lang_fetch:
                lang = langs[0]
            if lang == "English":
                warning = discord.Embed(description="<:raidenangry:1080897820854329376> Your account is already open, to reset it use : `/account end`", color=self.default_color)
                await ctx.respond(embed=warning, ephemeral=True)
            elif lang == "Français":
                warning = discord.Embed(description="<:raidenangry:1080897820854329376> Votre compte est déjà ouvert, pour le réinitialiser utilisez : `/account end`", color=self.default_color)
                await ctx.respond(embed=warning, ephemeral=True)
        else:
            if language == "English":
                if uid is not None:
                    if len(uid) == 9:
                        if name is not None:
                            self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `UID`, `NAME`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '{uid}', '{name}', 'English')")
                            self.mydb.commit()
                            creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Your account has been created successfully {ctx.author.mention}, you chose: `{name}` as adventure name and `{language}` as language. Now you can start your adventure in Inazuma with: `/story mode`", color=self.default_color)
                            await ctx.respond(embed=creation)
                        else:
                            self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `UID`, `NAME`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '{uid}', '{ctx.author.name}', 'English')")
                            self.mydb.commit()
                            creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Your account has been created successfully {ctx.author.mention}, you chose: `{language}` as language. Now you can start your adventure in Inazuma City with: `/story mode`", color=self.default_color)
                            await ctx.respond(embed=creation)
                    else:
                        warning = discord.Embed(description="<:raidenangry:1080897820854329376> **Error**: The UID doesn't seem to be correct, UID is the 9-digit number of your in-game account", color=self.default_color)
                        await ctx.respond(embed=warning)
                else:
                    if name is not None:
                        self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `UID`, `NAME`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '0', '{name}', 'English')")
                        self.mydb.commit()
                        creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Your account has been created successfully {ctx.author.mention}, you chose: `{name}` as adventure name and `{language}` as language. Now you can start your adventure in Inazuma with: `/story mode`", color=self.default_color)
                        await ctx.respond(embed=creation)
                    else:
                        self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `UID`, `NAME`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '0', '{ctx.author.name}', 'English')")
                        self.mydb.commit()
                        creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Your account has been created successfully {ctx.author.mention}, you chose: `{language}` as language. Now you can start your adventure in Inazuma City with: `/story mode`", color=self.default_color)
                        await ctx.respond(embed=creation)

            elif language == "Français":
                if uid is not None:
                    if len(uid) == 9:
                        if name is not None:
                            self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `UID`, `NAME`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '{uid}', '{name}', 'Français')")
                            self.mydb.commit()
                            creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Votre compte a été créé avec succès {ctx.author.mention}, vous avez choisi: `{name}` comme nom d’aventure et `{language}` comme langue. Maintenant vous pouvez commencer votre aventure à Inazuma avec: `/story mode`", color=self.default_color)
                            await ctx.respond(embed=creation)
                        else:
                            self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `UID`, `NAME`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '{uid}', '{ctx.author.name}', 'Français')")
                            self.mydb.commit()
                            creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Votre compte a été créé avec succès {ctx.author.mention}, vous avez choisi: `{language}` comme langue. Maintenant vous pouvez commencer votre aventure à Inazuma avec: `/story mode`", color=self.default_color)
                            await ctx.respond(embed=creation)
                    else:
                        warning = discord.Embed(description="<:raidenangry:1080897820854329376> **Erreur**: L'UID ne semble pas être correct, l'UID est le numéro à 9 chiffres de votre compte en jeu", color=self.default_color)
                        await ctx.respond(embed=warning)
                else:
                    if name is not None:
                        self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `UID`, `NAME`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '0', '{name}', 'Français')")
                        self.mydb.commit()
                        creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Votre compte a été créé avec succès {ctx.author.mention}, vous avez choisi: `{name}` comme nom d’aventure et `{language}` comme langue. Maintenant vous pouvez commencer votre aventure à Inazuma avec: `/story mode`", color=self.default_color)
                        await ctx.respond(embed=creation)
                    else:
                        self.cursor.execute(f"INSERT INTO `Account` (`ID`, `GUILD`, `UID`, `NAME`, `LANG`) VALUES ('{ctx.author.id}', '{ctx.guild.id}', '0', '{ctx.author.name}', 'Français')")
                        self.mydb.commit()
                        creation = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Votre compte a été créé avec succès {ctx.author.mention}, vous avez choisi: `{language}` comme langue. Maintenant vous pouvez commencer votre aventure à Inazuma avec: `/story mode`", color=self.default_color)
                        await ctx.respond(embed=creation)

    @account.command(name="end", description="🧳 Stop your adventure with Raiden Shogun")
    async def a_end(self, ctx):
        self.mydb.ping(reconnect=True)
        self.cursor.execute(f"SELECT `LANG` FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
        account_exist = self.cursor.fetchone()

        if account_exist is not None:
            self.cursor.execute(f"SELECT `LANG` FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
            lang_fetch = self.cursor.fetchall()
            for langs in lang_fetch:
                lang = langs[0]
            if lang == "Français":
                async def yes_callback(interaction):
                    delete = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Votre compte a été supprimé avec succès {ctx.author.mention}", color=self.default_color)
                    self.cursor.execute(f"DELETE FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
                    self.mydb.commit()
                    await interaction.response.send_message(embed=delete, ephemeral=True)

                async def no_callback(interaction):
                    stop = discord.Embed(description=f"Supression du compte annulée {ctx.author.mention}", color=self.default_color)
                    await interaction.response.send_message(embed=stop, ephemeral=True)

                confirm = discord.Embed(description=f"Êtes-vous sûr de vouloir supprimer votre compte ? {ctx.author.mention}", color=self.default_color)
                no = Button(label="C'etait une erreur", style=discord.ButtonStyle.danger)
                yes = Button(label="Oui", style=discord.ButtonStyle.green)
                no.callback = no_callback
                yes.callback = yes_callback
                view = View()
                view.add_item(no)
                view.add_item(yes)
                await ctx.respond(embed=confirm, view=view, ephemeral=True)

            elif lang == "English":
                async def yes_callback(interaction):
                    delete = discord.Embed(description=f"<:raidenlaugh:1080898399336931429> Your account has been deleted successfully {ctx.author.mention}", color=self.default_color)
                    self.cursor.execute(f"DELETE FROM `Account` WHERE `ID` = '{ctx.author.id}' AND `GUILD` = '{ctx.guild.id}'")
                    self.mydb.commit()
                    await interaction.response.send_message(embed=delete, ephemeral=True)

                async def no_callback(interaction):
                    stop = discord.Embed(description=f"Account deletion cancelled {ctx.author.mention}", color=self.default_color)
                    await interaction.response.send_message(embed=stop, ephemeral=True)

                confirm = discord.Embed(description=f"Are you sure you want to delete your account? {ctx.author.mention}", color=self.default_color)
                no = Button(label="That's an error", style=discord.ButtonStyle.danger)
                yes = Button(label="Yes", style=discord.ButtonStyle.green)
                no.callback = no_callback
                yes.callback = yes_callback
                view = View()
                view.add_item(no)
                view.add_item(yes)
                await ctx.respond(embed=confirm, view=view, ephemeral=True)

        else:
            warning = discord.Embed(description="<:raidenangry:1080897820854329376> You do not have an account to delete", color=self.default_color)
            await ctx.respond(embed=warning, ephemeral=True)

def setup(bot):
    bot.add_cog(StoryCog(bot))
