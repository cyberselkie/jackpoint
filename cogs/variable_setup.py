import os
from dotenv import load_dotenv
import discord
from discord import Option
from discord.ext import commands
from discord.commands import SlashCommandGroup
import asyncio

#import functions
import src.lookup as lup
import src.db as db
import src.dice as dice
import src.file_manip as fm
import src.conditions as con
#==========================================
load_dotenv()
servers = os.getenv("servers")
#==========================================
class variable_setup(discord.Cog):

    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    _set = SlashCommandGroup("set", "Set specific variables for later use.")

    @_set.command(guild_ids=servers, description="Set your active Commlink.")
    async def commlink(self, ctx, 
                        name=Option(str, "Character name.",required=True), 
                        comm_current = Option(str, "Name of the Commlink model you primarily use. Use exact name.",required=True),
                        comm_mode = Option(str, "AR, Hot-Sim VR, or Cold-Sim VR. May be changed later.", choices=["Hot-Sim VR", "AR", "Cold-Sim VR"],required=True),
                        module1 = Option(str, "The first of three modules loaded on your Commlink home screen. May be changed later.", choices=["Biometrics", "Wallet", "Smartlink", "Music"], required=True),
                        module2 = Option(str, "The second of three modules loaded on your Commlink home screen. May be changed later.", choices=["Biometrics", "Wallet", "Smartlink", "Music"],required=True),
                        module3 = Option(str, "The third of three modules loaded on your Commlink home screen. May be changed later.", choices=["Biometrics", "Wallet", "Smartlink", "Music"], required=True)):
        userid = ctx.user.id
        guildid = ctx.guild.id
        char_name = name.lower()
        filename = f'src/db/{guildid}.db'
        #USERID 0 NAME 1 COMM_CURRENT 2 COMM_MODE 3 MODULE1 4 MODULE2 5 MODULE3 6
        sql_statement = "INSERT OR REPLACE INTO Comm_Variables (userid, name, comm_current, comm_mode, module1, module2, module3) VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (userid,char_name,comm_current,comm_mode,module1,module2,module3)
        print(sql_statement)
        db.main_db(filename, sql_statement, values)
        db.Shadow_DB().exit_db()

        await ctx.respond(f"Your current Commlink for {char_name.title()} is {comm_current} in {comm_mode} mode with the {module1}, {module2}, and {module3} widgets loaded.")
    
    @_set.command(guild_ids=servers, description="Set your active character & currently active SIN.")
    async def sin(self, ctx,
                    name=Option(str, "Character name. May be changed later.",required=True), 
                    sinner=Option(str, "Character SIN name, nickname of Fake ID. Exact Case. May be changed later.",required=True)):
        userid = ctx.user.id
        guildid = ctx.guild.id 
        char_name = name.lower()
        filename = f'src/db/{guildid}.db'
        sql_statement = "INSERT OR REPLACE INTO User_Variables (userid, active_char, active_sin) VALUES (?, ?, ?)"
        values = (userid,char_name,sinner)
        db.main_db(filename, sql_statement, values)
        db.Shadow_DB().exit_db()

        await ctx.respond(f"Your current character is {name.title()} under the name {sinner}.")

    #@_set.command(guild_ids=servers, description="Initiate your max condition boxes.")

    # CONDITION BOX MODIFIERS
    @_set.command(guild_ids=servers, description="Modify your Physical Condition Boxes.")
    async def phys(self, ctx):
        userid = ctx.user.id
        guildid = ctx.guild.id 
        d = fm.FileManip().pull_db(guildid)
        name = lup.section(userid, d).find_Active_Character()
        await ctx.respond("Mark your damage.", view=(con.Phys_Condition_View(userid, d, name)))
        await asyncio.sleep(12)
        db.Shadow_DB().exit_db() #close DB, don't need it open anymore


#YAY COGS
def setup(bot):
    bot.add_cog(variable_setup(bot))