from bs4 import BeautifulSoup as soup
import time
import requests
from random import uniform

f = open("D:\\BD_Scripts\\uzdarbis_forumURLS.txt", 'r')
urls = f.read().split('\n')
f.close()
last_urls = []
out_filename = "D:\\BD_Scripts\\uzdarbis_postURLS.txt"
f = open(out_filename, "a+", encoding="utf-8")

for url in urls:
    offset = 0
    f.write("###" + url + "###\n")
    while True:
        time.sleep(uniform(1, 2))
        page_soup = soup(requests.get(
            url + "page__prune_day__100__sort_by__Z-A__sort_key__last_post__topicfilter__all__st__" + str(offset)).text)
        last = page_soup.find_all("a", {"class": "topic_title"})
        if last:
            for l in last:
                f.write(l["href"] + "\n")
            print(url + " DONE " + str(offset))
            offset += 30
        else:
            break

f.close()
