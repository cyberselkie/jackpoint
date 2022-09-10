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
#CLASS FOR THE MODAL/INPUT BOX ------------
class NodeInput(discord.ui.Modal):
    def __init__(self, name, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.add_item(discord.ui.InputText(label="System", placeholder="2",required=True)) #0
        self.add_item(discord.ui.InputText(label="Response", placeholder="2",required=True)) #1
        self.add_item(discord.ui.InputText(label="Firewall", placeholder="2",required=True)) #2
        self.add_item(discord.ui.InputText(label="Signal", placeholder="2", required=True)) #3
        self.add_item(discord.ui.InputText(label="Programs", style=discord.InputTextStyle.long, placeholder="Enter each program with a comma, as so: \nAnalyze 4, Black Hammer 3", required=True)) #4


    async def callback(self, interaction: discord.Interaction):
        system = self.children[0].value
        response = self.children[1].value
        firewall = self.children[2].value
        signal = self.children[3].value
        programs = self.children[4].value
        name = self.name
        
        #SQLite Time
        userid = interaction.user.id
        guildid = interaction.guild_id
        
        #Connect 2 the DB
        connection = sqlite3.connect(f'cogs/src/db/{guildid}.db') #make or connect to database  
        cursor = connection.cursor()
        cursor.execute(f"""INSERT INTO Nodes 
                          (userid, name, system, response, firewall, signal, programs) 
                           VALUES 
                          (?, ?, ?, ?, ?, ?, ?)""",(userid, name, system, response, firewall, signal, programs))
        connection.commit()
        connection.close()
        #Embed with submitted information
        embed = discord.Embed(title=f"Node {name} saved.",
                            color=discord.Colour.green())
        embed.add_field(name="Attributes", value=f"**System:** {system} \n **Response:** {response} \n **Firewall:** {firewall} \n **Signal:** {signal}")
        embed.add_field(name="Programs", value=programs)
        await interaction.response.send_message(embed=embed)

#CLASS FOR THE MODAL/INPUT BOX AGENT EDITION------------
class AgentInput(discord.ui.Modal):
    def __init__(self, name, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.add_item(discord.ui.InputText(label="System", placeholder="4",required=True)) #0
        self.add_item(discord.ui.InputText(label="Programs", style=discord.InputTextStyle.long, placeholder="Enter each program with a comma, as so: \nAnalyze 4, Black Hammer 3", required=True)) #1


    async def callback(self, interaction: discord.Interaction):
        rating = self.children[0].value
        programs = self.children[1].value
        name = self.name

        #SQLite Time
        userid = interaction.user.id
        guildid = interaction.guild_id
        
        #Connect 2 the DB
        connection = sqlite3.connect(f'cogs/src/db/{guildid}.db') #make or connect to database  
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO Agents
                          (userid, name, rating, programs) 
                           VALUES 
                          (?, ?, ?, ?)""",(userid, name, rating, programs.lower()))
        connection.commit()
        connection.close()
        #Embed with submitted information
        embed = discord.Embed(title=f"Agent {self.name} saved.",
                            description = f"**Rating:** {rating}",
                            color=discord.Colour.green())
        embed.add_field(name="Programs", value=programs)
        await interaction.response.send_message(embed=embed)

#==========================================

class gm(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot_: discord.Bot):
        self.bot = bot_
    
    #subcommands and sub-subcommands
    gm = SlashCommandGroup("gm", "GM commands.")
    new = gm.create_subgroup("new", "GM commands related to creation.")
    npc = gm.create_subgroup("npc", "GM commands related to NPCs.")
    nodes = gm.create_subgroup("node", "GM commands related to Nodes.")

    # CREATION COMMANDS 
    #node
    @new.command(guild_ids=servers, description="Allows you to save a node to the bot.")
    async def node(self, ctx, name=Option(str,"Name of the node. Make it unique from your other nodes.", required=True)):
        modal = NodeInput(title="Create a new Node.", name=name)
        await ctx.send_modal(modal)

    #agent
    @new.command(guild_ids=servers, description="Allows you to save a agent to the bot.")
    async def agent(self, ctx, name=Option(str,"Name of the agent. Make it unique from your other agent.", required=True)):
        modal = AgentInput(title="Create a new Agent.", name=name)
        await ctx.send_modal(modal)

    #NPC
    @new.command(guild_ids=servers, name="npc", description="Allows you to save the .chum file of an NPC to the bot.")
    @option(
    "attachment",
    discord.Attachment,
    description="The .chum file of your character.",
    required=True
    )
    async def upload_npc(self, ctx, name: Option(str,'Name of the character.', required=True), attachment: discord.Attachment):
        userid = ctx.user.id
        guildid = ctx.guild.id
        chumcheck = attachment.filename[-5:]
        if chumcheck == ".chum":
            grab = FileManip()
            chumstr = grab.pull_attachment(attachment)
            name = name.lower()
            #connect to database
            filename = f'cogs/src/db/{guildid}.db'
            sql_statement = "INSERT INTO Sheets (userid, name, chum) VALUES (?,?,?) "
            values = (userid,name,chumstr);
            table = "Sheets"
            main_db(filename, sql_statement, values)
            Shadow_DB().exit_db()

            await ctx.respond(f"Character {name} uploaded!")
        else:
            await ctx.respond("Wrong file!")

    # LOOKUP COMMANDS 
    #lookup node
    @nodes.command(guild_ids=servers, description="Allows you to search the skills of the saved NPC.")
    async def search(self,ctx,name = Option(str, "Name of the NPC.", required=True)):
        userid = ctx.user.id
        guildid = ctx.guild.id
        node = find_node(userid, guildid, name)
        #SYSTEM 0 RESPONSE 1 FIREWALL 2 SIGNAL 3 PROGRAMS 4
        system = node[0]
        response = node[1]
        firewall = node[2]
        signal = node[3]
        program_dict = node[4]
        programs = program_format().organize_programs(program_dict)
        await ctx.respond(f"""Name: {name}
System: {system}
Response: {response}
Firewall: {firewall}
Signal: {signal}
Programs: {programs}""")

    #lookup agent

    #lookup npc skills
    @npc.command(guild_ids=servers, description="Allows you to search the skills of the saved NPC.")
    async def skills(self,ctx,name = Option(str, "Name of the NPC.", required=True), lookup=None):
        userid = ctx.user.id
        guildid = ctx.guild.id
        skills = find_skill(userid, guildid, name) #pull proper section from db
        txt = f"```css\n// {name} //\n"
        # RATING O TOTVALUE 1 SPEC 2 KNOWLEDGE 3 ATTRIBUTE 4
        if lookup is not None:
            skill_name = lookup.title() #all skills are capitalized
            values = skills.get(skill_name)
            if values[3] is True: #check if knowledge skill
                txt+=f"[{skill_name}].knowledge"
            else:
                txt+=f"[{skill_name}]"
            txt += f"""
Attribute: {values[4]}
Rating: {values[0]}
Total Skill: {values[1]}
"""
            if values[2] != "None": #specialization or no specialization
                txt+=f"Spec: {values[2]} \n" 
            else:
                pass
            await ctx.respond(txt)
        else:
            for x in skills:
                values = skills.get(x)
                if values[0] == '0': #check if rating is 0
                    continue #if 0, don't list
                else:
                    if values[3] is True: #check if knowledge skill
                        txt+=f"\n[{x}].knowledge"
                    else:
                        txt += f"\n[{x}]"
                    txt += f"""
Attribute: {values[4]}
Rating: {values[0]}
Total Skill: {values[1]}"""
                    if values[2] != "None": #specialization or no specialization
                        txt+=f"\nSpec: {values[2]}"
                    else:
                        pass
                    txt+="; \n"
                    if len(txt) >= 1800: #split up message if txt is too big to fit into one message
                        txt += "```"
                        await ctx.respond(txt)
                        txt = "```css" #start new message
                        continue
            txt += "\n// end attachment //\n ```"
            await ctx.send(txt)
    
    @npc.command(guild_ids=servers, description="Allows you to search the programs of the saved NPCs.")
    async def programs(self, ctx, name = Option(str, "Name of the NPC.", required=True)):
        userid = ctx.user.id
        guildid = ctx.guild.id
        programs = find_program(userid, guildid, name)
        txt = f"```css\n// {name} //\n"
        for x in programs:
            values = programs[x]
            txt+=f"\n {x} \n Rating: {values}\n"
        txt += f"```"
        await ctx.respond(txt)


#YAY COGS
def setup(bot):
    bot.add_cog(gm(bot))
