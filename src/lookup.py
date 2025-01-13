import xml.etree.ElementTree as ET
import pandas as pd

import src.db as db
import src.file_manip as fm

class section():
    def __init__(self, userid, db, name=None):
        self.file = fm.FileManip()
        self.userid = userid
        self.db = db
        if name is not None:
            self.name = name

    def sheet(self): #find thing from sheets
        name = f'\'{self.name.lower()}\'' #names are stored lowercase & with quotes
        select = f"SELECT chum FROM Sheets WHERE name={name} GROUP BY userid={self.userid}"
        row = fm.FileManip().cursor_db(self, self.db, select)
        text = row[0][0] # grab just the sheet
        tree = ET.fromstring(text) #turn it back into xml
        return(tree)

    def _node(self):
        name = f'\'{self.name.lower()}\'' #names are stored lowercase & with quotes
        print(name)
        #select = """SELECT name FROM sqlite_master  
                #WHERE type='table';"""
        select = f"SELECT * FROM Nodes WHERE name={name} GROUP BY userid={self.userid}"
        row = fm.FileManip().cursor_db(self, self.db, select)
        print(row)
        text = row[0] #grab the whole node
        return(text)
    
    def _comm(self):
        name = f'\'{self.name.lower()}\''
        select = f"SELECT * FROM Comm_Variables WHERE name={name} GROUP BY userid={self.userid}"
        row = fm.FileManip().cursor_db(self, self.db, select)
        text = row[0]
        return(text)

    def find_Active_Character(self):
        select = f"SELECT active_char FROM User_Variables WHERE userid={self.userid}"
        row = fm.FileManip().cursor_db(self, self.db, select)
        print(row)
        text = row[0][0]
        return(text)

    def find_Active_SIN(self):
        select = f"SELECT active_sin FROM User_Variables WHERE userid={self.userid}"
        row = fm.FileManip().cursor_db(self, self.db, select)
        print(row)
        text = row[0][0]
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

class find():
    def __init__(self, userid, db, name):
        self.userid = userid
        self.db = db
        self.name = name

    # Find the relevant Skill or Skills of the Sheet --------------------------
    def find_skill(self):
        tree = section(self.userid, self.db, self.name).sheet()
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
    def find_program(self):
        tree = section(self.userid, self.db, self.name).sheet()
        programs = {}
        for x in tree.findall('gears/gear'): #Look through gear for Matrix Programs
            if x.find('category').text == "Matrix Programs":
                name = x.find('name').text
                rating = x.find('rating').text
                programs[name] = rating #record rating with name of program
            else: continue
        return programs

    # Lookup Stored Node
    def find_node(self):
        node = section(self.userid, self.db, self.name)._node()
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
    def find_comm(self):
        comm = section(self.userid, self.db, self.name)._comm()
        #USERID 0 CHAR_NAME 1 COMM_CURRENT 2 COMM_MODE 3 MODULE1 4 MODULE2 5 MODULE3 6
        commlink = {}
        comm_current = comm[2].title()
        commlink["comm_name"] = comm_current
        commlink["comm_mode"] = comm[3]
        commlink["module1"] = comm[4]
        commlink["module2"] = comm[5]
        commlink["module3"] = comm[6]

        tree = section(self.userid, self.db, self.name).sheet()
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

    #Lookup SINs from .chum
    def find_SIN(self):
        tree = section(self.userid, self.db, self.name).sheet()
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

    #Lookup first items in sheet
    def find_TopLevel(self, term):
        tree = section(self.userid, self.db, self.name).sheet()
        result = tree.find(term).text
        return (result)

    #Lookup all weapons, separated into melee or ranged when called
    def find_Weapons(self, term):
        tree = section(self.userid, self.db, self.name).sheet()
        weapons = {}
        mod_list = []
        for x in tree.findall('weapons/weapon'):
            if x.find('type').text == term: #loop through ranged or melee weapons
                name = x.find('name').text
                category = x.find('category').text
                spec = x.find('spec').text
                spec2 = x.find('spec2').text
                reach = x.find('reach').text
                damage = x.find('damage').text
                ap = x.find('ap').text
                mode = x.find('mode').text
                ammo = x.find('ammo').text
                conceal = x.find('conceal').text
                _range = x.find('range').text
                range_multiply = x.find('rangemultiply').text
                fullburst = x.find("fullburst").text
                suppressive = x.find("suppressive").text
                nickname = x.find('weaponname').text

                #loop through weapon mods for each weapon
                for mod in x.findall('weaponmods/weaponmod'):
                    m_name = mod.find('name').text
                    mod_list.append(m_name)
            else: continue
            _list = [category, spec, spec2, reach, damage,  # 0 1 2 3 4
                    ap, mode, ammo, conceal, _range,        # 5 6 7 8 9
                    range_multiply, fullburst, suppressive, nickname, mod_list]
            weapons[name] = _list                           # 10 11 12 13 14
        
        return(weapons)

    #Lookup attributes
    def find_Attributes(self):
        tree = section(self.userid, self.db, self.name).sheet()
        attrib = {}
        for x in tree.findall('attributes/attribute'):
            name = x.find('name').text
            value = x.find('value').text
            augmodifier = x.find('augmodifier').text
            totalvalue = x.find('totalvalue').text

            _list = [value, augmodifier, totalvalue]

            attrib[name] = _list

        return(attrib)

    #lookup cyberware
    def find_Cyberware(self):
        tree = section(self.userid, self.db, self.name).sheet()
        cyberware = {}
        for x in tree.findall('cyberwares/cyberware'):
            name = x.find('name').text
            category = x.find('category').text
            limbslot = x.find('limbslot').text
            ess = x.find('ess').text
            grade = x.find('grade').text

            _list = [category, limbslot, ess, grade]
                        #0          #1     #2   #3
            cyberware[name] = _list
            
            return(cyberware)
