import os
from dotenv import load_dotenv
import discord
from discord import option
from discord import Option
from discord.commands import SlashCommandGroup

#import functions
from cogs.src.lookup import *
from cogs.src.db import *
from cogs.src.dice import *
from cogs.src.file_manip import *
from cogs.src.commlink import create_comm
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
        output = create_comm(userid, guildid)

        await ctx.respond(output)

#YAY COGS
def setup(bot):
    bot.add_cog(matrix(bot))
