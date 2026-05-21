from Class.base import Base
import os
tools = Base()

path = os.path.dirname(os.path.realpath(__file__))
origin = "https://old.reddit.com/r/wallstreetbets/"
success, comments = tools.readFile(f"{path}/data/comments.json")

success, req = tools.fetch(origin)
if not success: exit(f"Failed to fetch {origin}")

urls = tools.getUrls(req.text)
filteredUrls = tools.filterUrls(urls,"reddit.com/r/wallstreetbets/comments/")
for url in filteredUrls: 
    if url not in comments: comments.append(url)
tools.saveFile(f"{path}/data/comments.json",filteredUrls)