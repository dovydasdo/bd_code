from bs4 import BeautifulSoup as soup
import time
import requests
from random import uniform

def getPageNums(info):
    arr = info.split(" ")
    n = arr[0]
    return int(n[1:])

f = open("D:\\BD_Scripts\\uzdarbis_postURLS.txt", 'r')
urls = f.read().split('\n')
f.close()
out_filename = "D:\\BD_Scripts\\uzdarbis_comms_raw_verslas-technologijos_domenai.txt"
f = open(out_filename, "a+", encoding="utf-8")

for url in urls:
    time.sleep(uniform(1, 2))
    page_soup = soup(requests.get(url + "/page__st__0").text)
    pages = page_soup.find_all("li", {"class":"total"})
    if pages:
        num_of_pages = getPageNums(pages[0].text)
        print(str(num_of_pages)  + " pages found")
        for i in range(0, num_of_pages - 1):
            time.sleep(uniform(1, 2))
            page_soup = soup(requests.get(url + "/page__st__" + str(20 * i)).text)
            print(url + "/page__st__" + str(20 * i) + " PAGE READ")
            conten = page_soup.find_all("div", {"class":"post entry-content"})
            if conten:
                for node in conten:
                    for trash in node.find_all():
                        trash.decompose()
                    string = ''.join(node.findAll(text=True))
                    string = string.split("+0000")[-1]
                    f.write("<BOS>" + string + "<EOS>")
            else:
                print("NO CONTENT")
    else:
        time.sleep(uniform(1, 2))
        page_soup = soup(requests.get(url + "/page__st__0").text)
        conten = page_soup.find_all("div", {"class":"post entry-content"})
        if conten:
            for node in conten:
                for trash in node.find_all():
                    trash.decompose()
                string = ''.join(node.findAll(text=True))
                string = string.split("+0000")[-1]
                f.write("<BOS>" + string + "<EOS>")
    print(url + " DONE")