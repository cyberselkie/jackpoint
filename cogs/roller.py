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

class dice_roller(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
    
    #subcommands and sub-subcommands
    roll = SlashCommandGroup("roll", "Dice roll commands.")

    @roll.command(guild_ids=servers, description="Roller test.")
    async def test(self, ctx, edge=None):
        rating = 6
        tn = 10
        rolls = roll(rating)
        result = rolls.extended_test(rating, edge, tn) #call function, get dict
        rolls_list = result["rolls"]
        hits = result["hits_list"]
        hits_total = 0
        await ctx.respond("Initializing...")
        msg = (f"// Extended Test // \nTN {tn}")
        sent = await ctx.send(msg)
        for x in rolls_list:
            index = rolls_list.index(x)
            hits_per = hits[index]
            hits_total += hits_per
            msg+=f"\n{x}\n{hits_per} hits / {hits_total} total hits"
            await asyncio.sleep(1) #rate limit
            await sent.edit(content=msg)
        if result["error"] is True:
            await ctx.send("Failure.")
        else:
            await ctx.send("Success!")
        #await ctx.respond(f"hits: {result[0]}\nresults: {result[3]}")

   # @roll.command(guild_ids=servers, description="Auto Extended Test.")
   # async def extest(self, ctx):


#YAY COGS
def setup(bot):
    bot.add_cog(dice_roller(bot))
