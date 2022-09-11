import os
from dotenv import load_dotenv
import discord
from discord import option
from discord import Option
from discord.commands import SlashCommandGroup
import xml.etree.ElementTree as ET
import sqlite3
import urllib.request
from urllib.request import Request
import asyncio

#import functions
from cogs.src.lookup import *
from cogs.src.db import *
from cogs.src.dice import *
from cogs.src.file_manip import *
#==========================================
load_dotenv()
servers = os.getenv("servers")
#==========================================
class variable_setup(discord.Cog):

    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    set_ = SlashCommandGroup("set", "Set specific variables for later use.")

    @set_.command(guild_ids=servers, description="Set your active Commlink.")
    async def commlink(self, ctx, 
                        name=Option(str, "Character name."), 
                        comm_current = Option(str, "Name of the Commlink model you primarily use. Use exact name."),
                        comm_mode = Option(str, "AR, Hot-Sim VR, or Cold-Sim VR. May be changed later.", choices=["Hot-Sim VR", "AR", "Cold-Sim VR"]),
                        module1 = Option(str, "The first of three modules loaded on your Commlink home screen. May be changed later.", choices=["Biometrics", "Wallet", "Smartlink", "Now Playing"]),
                        module2 = Option(str, "The second of three modules loaded on your Commlink home screen. May be changed later.", choices=["Biometrics", "Wallet", "Smartlink", "Now Playing"]),
                        module3 = Option(str, "The third of three modules loaded on your Commlink home screen. May be changed later.", choices=["Biometrics", "Wallet", "Smartlink", "Now Playing"])):
        userid = ctx.user.id
        guildid = ctx.guild.id
        char_name = name.lower()
        filename = f'cogs/src/db/{guildid}.db'
        #USERID 0 NAME 1 COMM_CURRENT 2 COMM_MODE 3 MODULE1 4 MODULE2 5 MODULE3 6
        sql_statement = "INSERT OR REPLACE INTO Comm_Variables (userid, name, comm_current, comm_mode, module1, module2, module3) VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (userid,char_name,comm_current,comm_mode,module1,module2,module3)
        main_db(filename, sql_statement, values)
        Shadow_DB().exit_db()

        await ctx.respond(f"Your current Commlink for {char_name.title()} is {comm_current} in {comm_mode} mode with the {module1}, {module2}, and {module3} widgets loaded.")
    
    @set_.command(guild_ids=servers, description="Set your active character & currently active SIN.")
    async def sin(self, ctx,
                    name=Option(str, "Character name. May be changed later."), 
                    sinner=Option(str, "Character SIN name, nickname of Fake ID. Exact Case. May be changed later.")):
        userid = ctx.user.id
        guildid = ctx.guild.id 
        char_name = name.lower()
        filename = f'cogs/src/db/{guildid}.db'
        sql_statement = "INSERT OR REPLACE INTO User_Variables (userid, active_char, active_sin) VALUES (?, ?, ?)"
        values = (userid,char_name,sinner)
        main_db(filename, sql_statement, values)
        Shadow_DB().exit_db()

        await ctx.respond(f"Your current character is {name.title()} under the name {sinner}.")

            

#YAY COGS
def setup(bot):
    bot.add_cog(variable_setup(bot))