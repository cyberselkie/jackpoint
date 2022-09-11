import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3

from cogs.src.file_manip import *

class section():
    def __init__(self) -> None:
        pass

    def sheet(self, userid, guildid, name): #find thing from sheets
        file = FileManip()
        name = f'\'{name.lower()}\'' #names are stored lowercase & with quotes
        select = f"SELECT chum FROM Sheets WHERE name={name} GROUP BY userid={userid}"
        print(select)
        row = file.pull_db(guildid, select)
        text = row[0][0] # grab just the sheet
        tree = ET.fromstring(text) #turn it back into xml
        return(tree)

    def _node(self, userid, guildid, name):
        file = FileManip()
        name = f'\'{name.lower()}\'' #names are stored lowercase & with quotes
        #select = """SELECT name FROM sqlite_master  
                #WHERE type='table';"""
        select = f"SELECT * FROM Nodes WHERE name={name} GROUP BY userid={userid}"
        row = file.pull_db(guildid, select)
        text = row[0] #grab the whole node
        return(text)
    
    def _comm(self, userid, guildid, name):
        file = FileManip()
        name = f'\'{name.lower()}\''
        select = f"SELECT * FROM Comm_Variables WHERE name={name} GROUP BY userid={userid}"
        row = file.pull_db(guildid, select)
        text = row[0]
        return(text)

    def find_Active_Character(self, userid, guildid):
        file = FileManip()
        select = f"SELECT active_char FROM User_Variables WHERE userid={userid}"
        active = file.pull_db(guildid, select)
        print(active)
        text = active[0][0]
        return(text)

    def find_Active_SIN(self, userid, guildid):
        file = FileManip()
        select = f"SELECT active_sin FROM User_Variables WHERE userid={userid}"
        active = file.pull_db(guildid, select)
        print(active)
        text = active[0][0]
        return(text)
    

class program_format():
        #Split Programs
    def programs_split(self, programs):
        programs_list = programs.split(",") # might need to do ", "
        programs_dict = {}
        for x in range(len(programs_list)):
            program = programs_list[x]
            program_split = program.split(" ")
            program_rating = int(program_split[-1]) # gets the last element in a list and casts it to int --- THIS ASSUMES A RATING WAS PASSED!!!
            program_name_split = program_split[0:-1] # gets every element EXCEPT the last element
            program_name = " ".join(program_name_split) # this is for programs with multiple words in their name like Black Hammer
            programs_dict[program_name] = program_rating
        print(programs_dict)
        return(programs_dict)
        
    #Find Program
    def find_node_programs(self, programs, prog):
        self.programs_split(programs)

    #Organize Programs List
    def organize_programs(self, programs_dict):
        programs = ""
        for i in programs_dict:
            value = programs_dict[i]
            programs += f"\n *{i} {value}*\n"
        return(programs)

# Find the relevant Skill or Skills of the Sheet --------------------------
def find_skill(userid, guildid, name):
    tree = section().sheet(userid, guildid, name)
    skills = {}
    for x in tree.findall('skills/skill'): #ElementTree is confusing so we have to search through all the skills first
        name = x.find('name').text
        rating = x.find('rating').text
        totvalue = x.find('totalvalue').text
        attribute = x.find('attribute').text
        if x.find('spec').text is not None: #record if specialization
            spec = x.find('spec').text
        else:
            spec = "None"
        if x.find('knowledge').text == "True": #record if knowledge skill
            knowledge = True
        else:
            knowledge = False
        values = (rating, totvalue, spec, knowledge, attribute) #values tuple
        skills[name] = values #record tuple inside name
    return skills

# List Programs of the Sheet
def find_program(userid, guildid, name):
    tree = section().sheet(userid, guildid, name)
    programs = {}
    for x in tree.findall('gears/gear'): #Look through gear for Matrix Programs
        if x.find('category').text == "Matrix Programs":
            name = x.find('name').text
            rating = x.find('rating').text
            programs[name] = rating #record rating with name of program
        else: continue
    return programs

# Lookup Stored Node
def find_node(userid, guildid, name):
    node = section()._node(userid, guildid, name)
    #USERID 0 NAME 1 SYSTEM 2 RESPONSE 3 FIREWALL 4 SIGNAL 5 PROGRAMS 6
    system = node[2]
    response = node[3]
    firewall = node[4]
    signal = node[5]
    program_data = node[6]
    programs = program_format().programs_split(program_data)
    programs_list = [system, response, firewall, signal, programs]
    return(programs_list)

# Lookup Comm Info
def find_comm(userid, guildid, name):
    tree = section().sheet(userid, guildid, name)
    comm = section()._comm(userid, guildid, name)
    #USERID 0 CHAR_NAME 1 COMM_CURRENT 2 COMM_MODE 3 MODULE1 4 MODULE2 5 MODULE3 6
    commlink = {}
    comm_current = comm[2].title()
    commlink["comm_name"] = comm_current
    commlink["comm_mode"] = comm[3]
    commlink["module1"] = comm[4]
    commlink["module2"] = comm[5]
    commlink["module3"] = comm[6]

    for x in tree.findall('gears/gear'): #look through gear for commlinks
        if x.find('category').text == "Commlink" and x.find('name').text == comm_current:
            commlink["response"] = x.find('response').text
            commlink["signal"] = x.find('signal').text
            for child in x.find('children'):
                if child.find('category').text == "Commlink Operating System":
                    commlink["os_name"] = child.find('name').text
                    commlink["firewall"] = child.find('firewall').text
                    commlink["system"] = child.find('system').text
                else: pass
                if child.find('category').text == "Commlink Operating System Upgrade":
                    if child.find('firewall').text != 0:
                        commlink["firewall"] = child.find('firewall').text
                    else: pass
                    if child.find('system').text != 0:
                        commlink["system"] = child.find('system').text
                    else: pass
        else:
            continue
    print(commlink)
    return(commlink)

def find_SIN(userid, guildid, name):
    tree = section().sheet(userid, guildid, name)
    sinner = {}
    #if x in tree:findall()
    for x in tree.findall('gears/gear'):
        if x.find('name').text == "Fake SIN":
            rating = x.find('rating').text
            name = x.find('extra').text
            sinner[name] = rating
        else: continue
    print(sinner)
    return(sinner)