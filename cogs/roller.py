import os
from dotenv import load_dotenv
import discord
from discord.commands import SlashCommandGroup
import asyncio

#import functions
import src.lookup as lup
import src.db as db
import src.dice as dice
import src.file_manip as fm
#==========================================
load_dotenv()
servers = os.getenv("servers")
#==========================================

class roller(discord.Cog): # create a class for our cog that inherits from commands.Cog
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
    @roll.command(guild_ids=servers)
    async def length_test(self, ctx):
        string = "                                   "
        length = string.count(" ")
        print(length)


#YAY COGS
def setup(bot):
    bot.add_cog(roller(bot))
