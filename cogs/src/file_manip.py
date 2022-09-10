import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error
import urllib.request
from urllib.request import Request, urlopen

class FileManip():
    """
    Description:
    This class encapsulates the manipulation of XML files.
    """
    #? CONSTRUCTOR
    def __init__(self) -> None:
        pass
    
    def pull_attachment(self, attachment):
        url = attachment.url # grab attachment url
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req).read()
        tree = ET.fromstring(response)
        chumstr = ET.tostring(tree, encoding='unicode', method='xml')

        return(chumstr)

    def pull_db(self, guildid, select):
        fp = f"cogs/src/db/{guildid}.db"
        db = sqlite3.connect(fp) #connect to db
        cursor = db.cursor()
        cursor.execute(select)
        txt = cursor.fetchall()

        return(txt)
