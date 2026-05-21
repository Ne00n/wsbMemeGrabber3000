from Class.base import Base
from random import randint
from time import sleep
import os
tools = Base()

path = os.path.dirname(os.path.realpath(__file__))
success, comments = tools.readFile(f"{path}/data/comments.json")
success, pictures = tools.readFile(f"{path}/data/pictures.json")
origin = "https://old.reddit.com/r/wallstreetbets/"
nextPages = []

while True:
    success, req = tools.fetch(origin)
    if not success: exit(f"Failed to fetch {origin}")

    urls = tools.getUrls(req.text)
    filteredUrls = tools.filterUrls(urls,"reddit.com/r/wallstreetbets/comments/")
    print(f"Fetched {len(filteredUrls)} comment urls")
    for url in filteredUrls: 
        if url not in comments: comments.append(url)
    tools.saveFile(f"{path}/data/comments.json",comments)
    nextPage = filteredUrls = tools.filterUrls(urls,"r/wallstreetbets/?count=")
    if not nextPage: break
    if len(nextPage) == 1:
        origin = nextPage[0]
    else:
        origin = nextPage[1]
    if origin in nextPages: break
    nextPages.append(origin)

for url in comments:
    if not url in pictures: 
        pictures[url] = []
        success, req = tools.fetch(url)
        if not success: exit(f"Failed to fetch {url}")
        urls = tools.getUrls(req.text)
        filteredUrls = tools.grabPictures(req.text)
        for picture in filteredUrls: 
            if picture not in pictures[url]: pictures[url].append(picture)
        tools.saveFile(f"{path}/data/pictures.json",pictures)
        sleep(randint(5,10))