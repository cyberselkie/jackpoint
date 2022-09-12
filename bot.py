import os #vawiables
from dotenv import load_dotenv
load_dotenv()

import discord #discord
from discord.ext import commands

import sqlite3 #db

load_dotenv()
TOKEN = os.getenv("TOKEN")
servers = os.getenv("servers")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot=discord.Bot(intents=intents)


#========================

#Message when bot is logged into discord (appears in console)
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

async def is_owner(ctx): #MY BOT
    return ctx.author.id == 525711157030420481

@bot.slash_command(hidden=True, guild_ids=servers, description="Owner only.")
@commands.check(is_owner)
async def create_connection(ctx): #Create SQLite database for server.
    guildid = ctx.guild.id #server id
    connection = sqlite3.connect(f'cogs/src/db/{guildid}.db') #make or connect to database  
    cursor = connection.cursor()
    #GM LIST
    cursor.execute('''CREATE TABLE IF NOT EXISTS GM
              (userid INT UNIQUE, active TEXT)''')
    #NODES LIST
    cursor.execute('''CREATE TABLE IF NOT EXISTS Nodes
              (userid INT, name TEXT, system INT, response INT, firewall INT, signal INT, programs TEXT)''')
    #AGENTS LIST
    cursor.execute('''CREATE TABLE IF NOT EXISTS Agents
              (userid INT, name TEXT, rating INT, programs TEXT)''')
    #CHARACTER SHEETS & NPCS
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sheets
              (userid INT, name TEXT UNIQUE, chum TEXT)''')
    #NETWORKS
    cursor.execute('''CREATE TABLE IF NOT EXISTS Networks
              (userid INT, name TEXT, nodes TEXT)''')
    #COMM VARIABLES
    cursor.execute('''CREATE TABLE IF NOT EXISTS Comm_Variables
              (userid INT, name TEXT UNIQUE, comm_current TEXT, comm_mode TEXT, module1 TEXT, module2 TEXT, module3 TEXT)''')
    #USER VARIABLES
    cursor.execute('''CREATE TABLE IF NOT EXISTS User_Variables
              (userid INT UNIQUE, active_char TEXT, active_sin TEXT)''')

    connection.commit()
    connection.close()

    await ctx.respond(f"Database for Server ID {guildid} created.")

#=======================
cogs_list = [
    'gm',
    'roller',
    'variable_setup',
    'matrix'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

bot.run(TOKEN)