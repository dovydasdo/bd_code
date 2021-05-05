from os import listdir
from os.path import isfile, join
import json

mypath = "D:\\DELFI_COMMENTS"
comms = []
for file in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
    f = open(mypath + "\\" + file, "r", encoding="utf-8")

    data = json.load(f)
    f.close()
    for comm in data["data"]["getCommentsByArticleId"]["comments"]:
        if comm:
            if comm["content"]:
                comms.append("<BOS> " + comm["content"] + " <EOS> ")
    f.close()

f = open("D:\\BD_Scripts\\DELFI_NEW_COMMS.txt", "w", encoding="utf-8")
print(len(comms))
for com in comms:
    f.write(com)

f.close()
