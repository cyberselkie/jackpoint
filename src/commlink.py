import os
from re import U #some vawiables
from dotenv import load_dotenv
load_dotenv()
import math

from src.lookup import *
import src.comm.widgets as widg
#====================================
#Constant Variables
comm_header = """```css

/ -------------------------------- \\
"""
comm_base = """\█\\"____________________________"/█/
 \███████████████████████████████/
```"""
spacer = "|█|                              |█|"

mod_error ="""
|█|                              |█|
|█|                              |█|
|█|           [ERROR]            |█|
|█|         *NONE FOUND*         |█|
|█|                              |█|
|█|                              |█|
"""
mod_error_header = "|█| ------  ------------  ------ |█|"


# ADDING SPACES FOR FORMATTING 
def length_(text):
    max_len = 30
    if len(text) <= max_len:
        space = max_len - len(text)
        front_space = " "*(math.floor(space/2))
        end_space = " "*(math.ceil(space/2))
        text = f"{front_space}{text}{end_space}"
    else:
        text = text[:28]+".."
    try:
        if len(text) == max_len:
            print("Spacing is right!")
            print(text)
    except:
        print("Spacing is wrong!")
    return(text)

def length_center(text1, text2):
    max_len = 28
    print(len(text1+text2))
    if len(text1 + text2) <= max_len:
        space = max_len - len(text1 + text2)
        middle_space = " "*space
        text = f" {text1}{middle_space}{text2} "
    try:
        if len(text) == max_len:
            print("Spacing is right!")
            print(text)
    except:
        print("Spacing is wrong!")
    return(text)

def number_manip(numbers):
    result = " ".join([numbers[::-1][i:i+3] for i in range(0, len(numbers), 3)])[::-1]
    return (result)

class commlink():
    def __init__(self, userid, db, name):
        self.userid = userid
        self.db = db
        self.name = name
        print(name)
        self.comm = find(userid, db, self.name).find_comm()
        self.sin = find(userid, db, self.name).find_SIN()
        self.sinner = section(userid, db, self.name).find_Active_SIN()

    #setup Commlink top section
    def comm_top(self):
        model = f"* {self.comm['comm_name'].upper()} *"
        print(model)
        text = length_(model)
        top_data = f"""|▒░{text}░▒|
|█|\____________________________/|█|
"""
        return(top_data)
    
    def comm_home_welcome(self):
        welcome = f"hello, {self.sinner.upper()}"
        print(welcome)
        text = length_(welcome)
        print(text)
        welcome_data = f"""|█|{text}|█|
{spacer}
"""
        return(welcome_data)
    
    def comm_notifs(self):
        notif_num = "[14]"
        art_num = "[02]"
        notifs = length_(f"{notif_num}  unread.Notifications")
        articles = length_(f"{art_num}  new.Articles        ")
        text = f"""|█|{notifs}|█|
|█|{articles}|█|
{spacer}
"""
        return(text)

    def comm_module(self, module_number):
        #Check the settings in the DB
        module = self.comm[module_number] 
        #wallet module
        if module == "Wallet":
            widget = widg.widgets(self.userid, self.db, self.name).wallet()
        #smartlink module
        elif module == "Smartlink":
            widget = widg.widgets(self.userid, self.db, self.name).smartlink()
        #biometrics module
        #elif module == "Biometrics":
        #music module
        #elif module == "Music":
        else:
            widget = mod_error_header+mod_error
        return(widget)
    
    def comm_bottom(self):
        mode = self.comm["comm_mode"]
        mode_text = f"user.Mode: {mode}"
        mode_text_text = length_(mode_text)
        text = f"""|█| ------ ============== ------ |█|
|█|{mode_text_text}|█|
"""

        print(text)
        return(text)
    
#PUTTING IT ALL TOGETHER
def create_comm(userid, db, name):
    comms = commlink(userid, db, name)
    comm = comm_header
    comm += comms.comm_top()
    comm += comms.comm_home_welcome()
    comm += comms.comm_notifs()
    comm += comms.comm_module("module1")
    comm += comms.comm_module("module2")
    comm += comms.comm_module("module3")
    comm += comms.comm_bottom()
    comm += comm_base
    return(comm)
        
