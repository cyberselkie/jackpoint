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
