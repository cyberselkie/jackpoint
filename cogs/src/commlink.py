import os #some vawiables
from dotenv import load_dotenv
load_dotenv()
import math

from cogs.src.lookup import *
#====================================
#Constant Variables
comm_header = """```css

/ -------------------------------- \\
"""
comm_base = """\ \\"____________________________"/ /
 \________________________________/
```"""
spacer = "| |                              | |"

# ADDING SPACES FOR FORMATTING 
def length_(text):
    max_len = 30
    if len(text) <= max_len:
        space = max_len - len(text)
        front_space = " "*(math.ceil(space/2))
        end_space = " "*(math.floor(space/2))
        text = f"{front_space}{text}{end_space}"
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

class modules():
    def wallet(self, userid, guildid):
        wallet = "| | --------  <WALLET>  -------- | |"
        divider = "| |              **              | |"
        karma = "13"
        karma_spent = "021"
        nuyen = "104 902"
        nuyen_spent = "8 374"

        karma_text = length_center("KARMA", karma)
        print(karma_text)
        karma_spent_text = length_center("KARMA_SPENT", karma_spent)
        nuyen_text = length_center("NUYEN", nuyen)
        nuyen_spent_text = length_center("NUYEN_SPENT", nuyen_spent)
        module_text = f"""{wallet}
| |{karma_text}| |
| |{nuyen_text}| |
{divider}
| |{karma_spent_text}| |
| |{nuyen_spent_text}| |
{spacer}
"""
        return(module_text)

class commlink():
    #setup Commlink top section
    def comm_top(self,userid, guildid):
        name = section().find_Active_Character(userid, guildid)
        comm = find_comm(userid, guildid, name)
        model = "* "
        for l in comm["comm_name"]:
            model += f"{l.title()} "
        model += " *"
        print(model)
        text = length_(model)
        top_data = f"""| .{text}. |
| |\____________________________/| |
"""
        return(top_data)
    
    def comm_home_welcome(self, userid, guildid):
        name = section().find_Active_Character(userid, guildid)
        sin = find_SIN(userid, guildid, name)
        sinner = section().find_Active_SIN(userid, guildid)
        print(sin)
        welcome = f"hello, {sinner}"
        print(welcome)
        text = length_(welcome)
        print(text)
        welcome_data = f"""| |{text}| |
{spacer}
"""
        return(welcome_data)
    
    def comm_notifs(self):
        notif_num = "4"
        art_num = "2"
        notifs = length_(f"[{notif_num}] Unread.notifications")
        articles = length_(f"[{art_num}] New Articles")
        text = f"""| |{notifs}| |
| |{articles}| |
{spacer}
"""
        return(text)

    def comm_module(self, userid, guildid, module_number):
        name = section().find_Active_Character(userid, guildid)
        comm = find_comm(userid, guildid, name)
        module = comm[module_number]
        if module == "Wallet":
            widget = modules().wallet(userid, guildid)
        else:
            widget = modules().wallet(userid, guildid)
        print(widget)
        return(widget)
    
    def comm_bottom(self, userid, guildid):
        name = section().find_Active_Character(userid, guildid)
        comm = find_comm(userid, guildid, name)
        mode = comm["comm_mode"]
        mode_text = f"user.Mode: {mode}"
        mode_text_text = length_(mode_text)
        text = f"""| | ------ ============== ------ | |
| |{mode_text_text}| |
"""

        print(text)
        return(text)


#PUTTING IT ALL TOGETHER
def create_comm(userid, guildid):
    comm = comm_header
    comm += commlink().comm_top(userid, guildid)
    comm += commlink().comm_home_welcome(userid, guildid)
    comm += commlink().comm_notifs()
    comm += commlink().comm_module(userid, guildid, "module1")
    comm += commlink().comm_module(userid, guildid, "module2")
    comm += commlink().comm_module(userid, guildid, "module3")
    comm += commlink().comm_bottom(userid, guildid)
    comm += comm_base
    return(comm)
        
