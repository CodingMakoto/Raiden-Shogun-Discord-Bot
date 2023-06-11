import random

import discord
from discord.ext import commands

import mysql.connector

from help import *
from story import *
#from personnal import *

# ---------------- Intents & Init ---------------- #

intents = discord.Intents.default()
intents.members = True
client = discord.Client()
bot = commands.Bot()

default_color = 0x402c4c

bot.remove_command('help')

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
async def on_ready():
    print("Raiden Shogun is Ready")
    print(f"Servers Count: {len(bot.guilds)}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Inazuma 🌸 /help"))

@bot.event
async def on_guild_join(guild):
    file = discord.File("/media/bot/images/avatar-wb.png", filename="avatar.png")
    title = "<:raidenangry:1080897820854329376> So... you want to start a new adventure with me ?"
    welcoming = discord.Embed(
        title=title,
        description="Well... thanks you for adding me to your server !\n\n・ Raiden Shogun Discord Bot is using ONLY Slash Commands\n・ So now, you can start a new adventure and start exploring Inazuma Island by using : `/account start`, if you want to reset your account you can use : `/account end`\nWhen your account is created use : `/story mode` and enjoy the adventure ! <:raidenbird:1080897824440455288>\n・ You can fight Bosses, recover your health with Archons Statues, Fight Hilichurls and more !\n・ I let you discover that by yourself using : `/help` <:raidenlaugh:1080898399336931429>\n・ You have more questions ? Well then I let you enter in Raiden Shogun City ⚡ : https://discord.gg/2AePNcphrs",
        color=default_color
    )
    welcoming.set_thumbnail(url="attachment://avatar.png")
    welcoming.set_footer(text="Created and Developed by Makoto#7116")

    channel = discord.utils.get(guild.text_channels, permissions_for=guild.me.send_messages)
    if channel:
        await channel.send(embed=welcoming, file=file)
    else:
        await guild.owner.send(embed=welcoming, file=file)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (discord.ext.commands.CommandError, discord.DiscordException)):
        errors = discord.Embed(
            title="There was an error while executing command",
            description=f"Error: `{error}`",
            color=default_color
        )
        await ctx.respond(embed=errors)

# ---------------- Run & Cogs ---------------- #

bot.add_cog(HelpCog(bot))
bot.add_cog(StoryCog(bot))
#bot.add_cog(PersonnalCog(bot))
bot.run("TOKEN")
