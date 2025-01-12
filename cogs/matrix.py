import os
from dotenv import load_dotenv
import discord
from discord import option
from discord import Option
from discord.commands import SlashCommandGroup

#import functions
import src.lookup as lup
import src.db as d
import src.dice as dice
import src.file_manip as fm
import src.commlink as comm
#==========================================
load_dotenv()
servers = os.getenv("servers")
#==========================================

class matrix(discord.Cog):

    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
    
    comm = SlashCommandGroup("comm", "Commlink commands.")

    @comm.command(name="open", guild_ids=servers, description="Pull up your Commlink interface.")
    async def open_(self, ctx):
        userid = ctx.user.id 
        guildid = ctx.guild.id
        db = fm.FileManip().pull_db(guildid)
        name = lup.section(userid, db).find_Active_Character()
        output = comm.create_comm(userid, db, name)
        d.Shadow_DB().exit_db() #close DB, don't need it open anymore
        await ctx.respond(output)

#YAY COGS
def setup(bot):
    bot.add_cog(matrix(bot))
