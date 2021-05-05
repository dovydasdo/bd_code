from bs4 import BeautifulSoup as soup
import time
import requests
from random import uniform

f = open("D:\\scraping\\scrape.txt", "a+", encoding="utf-8")
links = ["http://linksmas.net/pasnekesiai-f39-$OFFSET.html"]


def get_thread_comms(threads, f):
    for thread in threads:
        thread_offset = 0
        time.sleep(uniform(1, 2))
        thread_soup = soup(requests.get(thread["href"].split(".html")[0] + "-" + str(thread_offset) + ".html").text,
                           features="lxml")
        nop_soup = thread_soup.find_all("a", {"title": "Norėdami pereiti į puslapį paspauskite čia…"})
        if nop_soup:
            nop_thread = int(nop_soup[0].text.split(" ")[-1])  # Number of thread pages
            comms = thread_soup.find_all("div", {"class": "content"})
            print(thread["href"].split(".html")[0] + "-" + str(
                thread_offset) + ".html" + " COMMENTS FIRST PAGE FOUND : " + str(len(comms)))
            for comm in comms:
                f.write(" <BOS> " + comm.text + " <EOS> ")
            thread_offset += 15
            if nop_thread > 1:
                for i in range(1, nop_thread - 1):
                    time.sleep(uniform(1, 2))
                    thread_soup = soup(
                        requests.get(thread["href"].split(".html")[0] + "-" + str(thread_offset) + ".html").text,
                        features="lxml")
                    thread_offset += 15
                    comms = thread_soup.find_all("div", {"class": "content"})
                    print(thread["href"].split(".html")[0] + "-" + str(
                        thread_offset) + ".html" + " COMMENTS OTHER PAGES FOUND : " + str(len(comms)))
                    for comm in comms:
                        f.write(" <BOS> " + comm.text + " <EOS> ")
        else:
            comms = thread_soup.find_all("div", {"class": "content"})
            print(thread["href"].split(".html")[0] + "-" + str(
                thread_offset) + ".html" + " COMMENTS FOUND SINGLE PAGE : " + str(len(comms)))
            for comm in comms:
                f.write(" <BOS> " + comm.text + " <EOS> ")


for url in links:
    offset = 0
    time.sleep(uniform(1, 2))
    page_soup = soup(requests.get(url.replace("$OFFSET", str(offset))).text, features="lxml")
    num_of_pages_soup = page_soup.find_all("a", {"title": "Norėdami pereiti į puslapį paspauskite čia…"})[0]
    nop = (num_of_pages_soup.text.split(" ")[-1])  # Number of main pages

    threads = page_soup.find_all("a", {"class": "topictitle"})
    get_thread_comms(threads, f)
    offset += 40
    if int(nop) > 1:
        for i in range(1, int(nop) - 1):
            page_soup = soup(requests.get(url.replace("$OFFSET", str(offset))).text, features="lxml")
            offset += 40
            threads = page_soup.find_all("a", {"class": "topictitle"})
            get_thread_comms(threads, f)
    print(url + " DONE")
