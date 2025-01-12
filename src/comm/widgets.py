import os
from re import U #some vawiables
from dotenv import load_dotenv
load_dotenv()

from src.lookup import *
import src.commlink as c

spacer = "|█|                              |█|"

class widgets():
    def __init__(self, userid, db, name):
        self.userid = userid
        self.db = db
        self.name = name
        print(name)
        self.comm = find(userid, db, self.name).find_comm()
        self.sin = find(userid, db, self.name).find_SIN()
        self.sinner = section(userid, db, self.name).find_Active_SIN()

    # MODULE CREATION HERE ===================

    def wallet(self):
        wallet = "|█| --------  <WALLET>  -------- |█|"
        divider = "|█|              **              |█|"
        f = find(self.userid, self.db, self.name)
        #current and spent karma
        karma = f.find_TopLevel('karma')
        karma = c.number_manip(karma)
        karma_total = f.find_TopLevel('totalkarma')
        karma_spent = str(int(karma_total) - int(karma))
        karma_spent = c.number_manip(karma_spent)
        #current total nuyen
        nuyen = f.find_TopLevel('nuyen')
        nuyen = c.number_manip(nuyen)
        #streetcred. may be replaced
        streetcred = f.find_TopLevel('streetcred')
        #formatting it into the proper string
        karma_text = c.length_center("KARMA", str(karma))
        karma_spent_text = c.length_center("KARMA_SPENT", karma_spent)
        nuyen_text = c.length_center("NUYEN", nuyen)
        streetcred_text = c.length_center("STREET_CRED", streetcred)

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
                _range = values[9]
                _list = [nickname, category, ammo, mode, ap, damage, spec, _range]
                        #0         #1       #2     #3   #4   #5       #6    #7
                smartlist[x] = _list
            else:
                continue
        print(smartlist)
        if len(smartlist) == 0:
            txt = header+c.mod_error

        elif len(smartlist) == 1: #if only one gun
            name = list(smartlist)[0]
            values = smartlist[name]
            #if nickname is not None:
               # nickname = f'"{values[0]}"'
            #else: nickname = "..."
            _range = values[7]
            spec = values[6]
            category = values[1]
            ammo = values[2]
            mode = values[3]
            ap = values[4]
            damage = values[5]

            #adjust for length
            name = c.length_(name)
            nickname = c.length_(nickname)
            line3 = c.length_(f"> {category} <")
            #line4 = length_("**")
            line4 = c.length_center(f"RNG[{_range}]", f"SPEC[{spec}]")

            line5 = f"AP[{ap}] // DMG[{damage}]"
            line5 = c.length_center(line5, f"MODE{mode}")
            line6 = c.length_center(".ammo",ammo)

            txt = f"""{header}
|█|{nickname}|█|
|█|{name}|█|
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
                name = c.length_(name) #adjust for length
                line2 = f"AP[{values[4]}] // DMG[{values[5]}]"
                line2 = c.length_center(line2, f"MODE{mode}")
                line3 = c.length_center(".ammo",values[2])
                txt += f"""|█|{name}|█|
|█|{line2}|█|
|█|{line3}|█|
"""           
                txt += f"|█|{c.length_('**')}|█|\n" if counter == 1 else ""

        elif len(smartlist) == 3: #if there are 3 guns
            txt = f"{header}\n"
            counter = 0
            for x in list(smartlist):
                name = list(smartlist)[x]
                counter += 1
                values = smartlist[name]
                name = c.length_(name) #adjust for length
                #line2 = length_center(".ammo",values[2])
                line2 = c.length_center(f"AP[{values[4]}] // DMG[{values[5]}]", f"MODE{mode}")
                txt+=f"""|█|{name}|█|
|█|{line2}|█|
"""
        else: print("Didn't work!")
        print(txt)
        return(txt)

    def biometrics(self):
        header = "|█| ------  <BIOMETRICS>  ------ |█|"
