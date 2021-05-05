from bs4 import BeautifulSoup as soup
import requests

page_soup = soup(requests.get("https://www.delfi.lt/").text)

out_filename = "G:\\BD_Scripts\\delfi_AIDs.txt"
f = open(out_filename, "w+", encoding="utf-8")

items = page_soup.find_all("h3",{"class":"headline-title"})
aids_old = f.read().split('\n')
aids = []
for item in items:
    ancers = item.find_all("a")
    url = ancers[0]["href"]
    if(".d?id=" in url):
        aid = url.split(".d?id=")[-1]
        if (aid in aids or aid in aids_old):
            continue
        aids.append(aid)
        f.write(aid + "\n")
f.close()
