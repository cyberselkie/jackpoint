import os
from re import U #some vawiables
from dotenv import load_dotenv
load_dotenv()
import math

from cogs.src.lookup import *
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
        module = self.comm[module_number]
        if module == "Wallet":
            widget = self.wallet()
        elif module == "Smartlink":
            widget = self.smartlink()
        #elif module == "Biometrics":
        #elif module == "Now Playing":
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
    
    # MODULE CREATION HERE ===================

    def wallet(self):
        wallet = "|█| --------  <WALLET>  -------- |█|"
        divider = "|█|              **              |█|"
        f = find(self.userid, self.db, self.name)
        #current and spent karma
        karma = f.find_TopLevel('karma')
        karma = number_manip(karma)
        karma_total = f.find_TopLevel('totalkarma')
        karma_spent = str(int(karma_total) - int(karma))
        karma_spent = number_manip(karma_spent)
        #current total nuyen
        nuyen = f.find_TopLevel('nuyen')
        nuyen = number_manip(nuyen)
        #streetcred. may be replaced
        streetcred = f.find_TopLevel('streetcred')
        #formatting it into the proper string
        karma_text = length_center("KARMA", str(karma))
        karma_spent_text = length_center("KARMA_SPENT", karma_spent)
        nuyen_text = length_center("NUYEN", nuyen)
        streetcred_text = length_center("STREET_CRED", streetcred)

        module_text = f"""{wallet}
|█|{karma_text}|█|
|█|{nuyen_text}|█|
{divider}
|█|{karma_spent_text}|█|
|█|{streetcred_text}|█|
{spacer}
"""
        return(module_text)

    def smartlink(self):
        header = "|█| ------  <SMART_LINK>  ------ |█|"
        f = find(self.userid, self.db, self.name)
        weapons_list = f.find_Weapons("Ranged")
        counter = 0
        smartlist = {}
        for x in weapons_list:
            if counter >= 3:
                break
            else: pass
            values = weapons_list.get(x)
            if "Smartgun System" in values[14]:
                counter += 1
                category = values[0]
                spec = values[1]
                damage = values[4]
                ap = values[5]
                mode = values[6]
                ammo = values[7]
                nickname = values[13]
                _list = [nickname, category, ammo, mode, ap, damage, spec]
                        #0         #1       #2     #3   #4   #5       #6
                smartlist[x] = _list
            else:
                continue
        print(smartlist)
        if len(smartlist) == 0:
            txt = header+mod_error

        elif len(smartlist) == 1: #if only one gun
            name = list(smartlist)[0]
            values = smartlist[name]
            if nickname is not None:
                nickname = f'"{values[0]}"'
            else: nickname = "..."
            category = values[1]
            ammo = values[2]
            mode = values[3]
            ap = values[4]
            damage = values[5]

            #adjust for length
            name = length_(name)
            nickname = length_(nickname)
            line3 = length_(category)
            line4 = length_("**")

            line5 = f"AP[{ap}] // DMG[{damage}]"
            line5 = length_center(line5, f"[{mode}]")
            line6 = length_center(".ammo",ammo)

            txt = f"""{header}
|█|{name}|█|
|█|{nickname}|█|
|█|{line3}|█|
|█|{line4}|█|
|█|{line5}|█|
|█|{line6}|█|
"""
        elif len(smartlist) == 2: #if there are 2 guns
            txt = f"{header}\n"
            counter = 0
            
            for x in list(smartlist):
                name = list(smartlist)[counter]
                counter += 1
                values = smartlist[name]
                name = length_(name) #adjust for length
                line2 = f"AP[{values[4]}] // DMG[{values[5]}]"
                line2 = length_center(line2, f"[{mode}]")
                line3 = length_center(".ammo",values[2])
                txt += f"""|█|{name}|█|
|█|{line2}|█|
|█|{line3}|█|
"""           
                txt += f"| |{length_('**')}| |\n" if counter == 1 else ""

        elif len(smartlist) == 3: #if there are 3 guns
            txt = f"{header}\n"
            counter = 0
            for x in list(smartlist):
                name = list(smartlist)[x]
                counter += 1
                values = smartlist[name]
                name = length_(name) #adjust for length
                line2 = length_center(".ammo",values[2])
                txt+=f"""|█|{name}|█|
|█|{line2}|█|
"""
        else: print("Didn't work!")
        print(txt)
        return(txt)

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
        
