import subprocess, sys
import time
from random import randrange, uniform
import json

f = open("D:\\BD_Scripts\\delfi_archive_AIDs.txt", 'r')
aids = f.read().split('\n')
f.close()
counter_a = 0
counter_r = 0
for aid in aids:
    #Can only get 100 comms per request + responses
    g_aid = aid.split(" ")[0]
    offset = 0
    while(True):
        raz_path = "D:\\DELFI_COMMENTS\\" + str(counter_a) + "_anon.json"
        counter_a += 1
        time.sleep(uniform(10, 20))
        ################################################################### AID | MODE_TYPE | ORDER_BY | LIMIT | OFFSET | LIMIT_REPLIES | OUT_FILE_NAME
        p = subprocess.Popen(["powershell.exe", 
        "D:\\Bakalauro_darbas\\Scraping\\Delfi\\gql_api\\request.ps1 {} {} {} {} {} {} {}".format(
            g_aid, 
            "ANONYMOUS_MAIN", 
            "DATE_DESC",
            "20",
            offset,
            "20",
            raz_path
            )],
        stdout=sys.stdout)
        p.communicate()
        offset+= 20

        f = open(raz_path, "r", encoding="utf-8")

        data = json.load(f)
        f.close()
        if len(data["data"]["getCommentsByArticleId"]["comments"]) < 20:
            break;
    
    print(aid + " ARTICLE ANON DONE")
    offset = 0
    while(True):
        raz_path = "D:\\DELFI_COMMENTS\\" + str(counter_r) + "_registerd.json"
        counter_r += 1
        time.sleep(uniform(10, 20))
        ################################################################### AID | MODE_TYPE | ORDER_BY | LIMIT | OFFSET | LIMIT_REPLIES | OUT_FILE_NAME
        p = subprocess.Popen(["powershell.exe", 
        "D:\\Bakalauro_darbas\\Scraping\\Delfi\\gql_api\\request.ps1 {} {} {} {} {} {} {}".format(
            g_aid, 
            "REGISTERED_MAIN", 
            "DATE_DESC",
            "20",
            offset,
            "20",
            raz_path
            )],
        stdout=sys.stdout)
        p.communicate()
        offset+= 20

        f = open(raz_path, "r", encoding="utf-8")

        data = json.load(f)
        f.close()
        if len(data["data"]["getCommentsByArticleId"]["comments"]) < 20:
            break;
    print(aid + " ARTICLE REGISTERD DONE")