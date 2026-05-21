from Class.base import Base
import os
tools = Base()

path = os.path.dirname(os.path.realpath(__file__))
success, comments = tools.readFile(f"{path}/data/comments.json")
origin = "https://old.reddit.com/r/wallstreetbets/"

while True:
    print(f"Fetching {origin}")
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