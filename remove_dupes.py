import random
from main_config import options

f = open(options["cleaned_data_path"], 'r', encoding="utf-8")
comms = f.read().split(' <EOS> ')
f.close()
before = len(comms)
comms = list(dict.fromkeys(comms))
random.shuffle(comms)

f = open(options["cleaned_data_path_no_dupes"], 'w', encoding="utf-8")
count = 0
for com in comms:
    f.write("<BOS>" + com.split("<BOS>")[-1] + " <EOS> ")

    count += 1

f.close()
print("NUM OF COMENTS: " + str(count) + " NUM OF COMMS BEFORE: " + str(before))
