import random

import discord
from discord.ext import commands

import mysql.connector

from story import *

# ---------------- Intents & Init ---------------- #

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

default_color = 0x37266a

# ---------------- Database ---------------- #

mydb = mysql.connector.connect(
      host="HOST",
      user="USER",
      password="PASSWORD",
      database="DATABASE",
      auth_plugin="METHOD"
)

cursor = mydb.cursor()

# ---------------- Events ---------------- #

@bot.event
async def on_guild_join(guild):
    file = discord.File("/home/acourant/bots/beta/images/avatar-wb.png", filename="avatar.png")
    title = "<:raidenbird:1080897824440455288>  Raiden Shogun Discord Bot"
    welcoming = discord.Embed(
        title=title,
        description="So... you want to start a new adventure with me ?\n\n> ・ Raiden Shogun Discord Bot is an Unofficial Genshin Impact Discord Bot using ONLY Slash Commands\n> ・ So now, you can start a new adventure and start exploring the New Inazuma Island by using : `/account start`, if you want to reset your account you can use : `/account end`\n> ・ When your account is created use : `/story mode` and enjoy the adventure ! <:raidenangry:1080897820854329376>\n> ・ You can fight Bosses, recover your health with Archons Statues, Fight Hilichurls and more !\n> ・ I let you discover that by yourself using : `/help` <:raidenlaugh:1080898399336931429>\n> ・ You have more questions ? Well then I let you enter in Raiden Shogun City ⚡ : https://discord.gg/2AePNcphrs",
        color=default_color
    )
    welcoming.set_thumbnail(url="attachment://avatar.png")
    welcoming.set_footer(text="Created and Developed by Makoto#7116")

    channel = discord.utils.get(guild.text_channels)
    if channel.permissions_for(guild.me).send_messages:
        await channel.send(embed=welcoming, file=file)
    else:
        await guild.owner.send(embed=welcoming, file=file)

@bot.event
async def on_command_error(ctx, error):
    #await ctx.send('This command is on cooldown, you can use it in {round(error.retry_after, 2)}')
    if isinstance(error, (discord.ext.commands.CommandError, discord.DiscordException, discord.errors.ApplicationCommandInvokeError)):
        errors = discord.Embed(
            title="There was an error while executing command",
            description=f"Error: `{error}`",
            color=default_color
        )
        await ctx.respond(embed=errors)

# ---------------- Run & Cogs ---------------- #

bot.load_extension("story")

@bot.event
async def on_connect():
    await bot.sync_commands()

@bot.event
async def on_ready():
    print("Raiden Shogun Beta is Ready")

bot.run("TOKEN")
