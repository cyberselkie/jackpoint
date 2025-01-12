from itertools import count
import math
import xml.etree.ElementTree as ET
import pandas as pd
import discord

import src.lookup as lup
import src.file_manip as fm
import src.db as d

"""
Tracking & recording variables that are
user input and managed.

"""

class Condition_Boxes():
    def __init__(self, userid, db, name=None):
        self.file = fm.FileManip()
        self.userid = userid
        self.db = db
        if name is not None:
            self.name = name

    def phys_max(self):
        attributes = lup.find(self.userid, self.db, self.name).find_Attributes()
        bod = attributes['BOD']
        value = bod[2]

        cyberware = lup.find(self.userid, self.db, self.name).find_Cyberware()
        print(cyberware)
        counter = 0
        for x in cyberware:
            info = cyberware.get(x)
            if info[1] is not None:
                counter += 1

        phys_box_count = (math.ceil(int(value)/2)+8+counter)
        return(phys_box_count)

    def stun_max(self):
        attributes = lup.find(self.userid, self.db, self.name).find_Attributes()
        wil = attributes['Wil']
        totalvalue = wil[2]
        stun_box_count = (math.ceil(int(totalvalue)/2)+8)
        return(stun_box_count)


class Phys_Condition_Buttons(discord.ui.Button): #Physical Condition Boxes
    def __init__(self, phys_max, x:str = None, y: int = None, z:str = None): #x: int
        # A label is required, but we don't need one so a zero-width space is used.
        super().__init__(style=discord.ButtonStyle.green, label=x, row=y, custom_id=z)
        self.x = x
        self.y = y
        self.z = z
        self.phys_max = phys_max

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Phys_Condition_View = self.view

        c = 0
        for child in view.children:
            n = view.children.index(child)
            print(f"this is n {n}")
            if n <= int(self.z) and child.style is discord.ButtonStyle.green: #if the button is green
                child.style = discord.ButtonStyle.red                         #mark all buttons before it red

            elif child.style is discord.ButtonStyle.red: #If the button is already red
                for _ in range(int(self.z)+1):             # mark all buttons after it green
                    if n >= (int(self.z)):
                        child.style = discord.ButtonStyle.green
            else: break
            if child.style is discord.ButtonStyle.red:
                c+=1

        phys = self.phys_max - c
        content = f"{phys} / {self.phys_max}"
        await interaction.response.edit_message(content=content, view=view)

class Phys_Condition_View(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons.
    # This is not required.
    def __init__(self, userid, db, name):
        super().__init__(timeout=10)
        self.userid = userid
        self.db = db
        self.name = name
        self.phys_max = Condition_Boxes(userid, db, name).phys_max()
        print(f"{self.phys_max} max phys")
        y = 0
        xcount = 1
        
        for z in range(self.phys_max):
            x = "\u200b"
            if z%3 == 0:
                y += 1
            elif z%3 == 2:
                x = f"-{xcount}"
                xcount+=1
            else: pass
            z = str(z)
            self.add_item(Phys_Condition_Buttons(self.phys_max, x, y, z))
        
    async def on_timeout(self):
        print(self.children)
        c = 0
        for child in self.children:
            if child.style is discord.ButtonStyle.red:
                c+=1
            child.disabled = True
        phys = self.phys_max - c
        char_name = self.name.lower()
        #USERID 0 NAME 1 COMM_CURRENT 2 COMM_MODE 3 MODULE1 4 MODULE2 5 MODULE3 6
        sql_statement = "INSERT OR REPLACE INTO Comm_Variables (userid, name, comm_current, comm_mode, module1, module2, module3) VALUES (?, ?, ?, ?, ?, ?, ?)"

        content = f"```Total: {phys} / {self.phys_max} Physical damage boxes left.```"
        await self.message.edit(content=content, view=self)

