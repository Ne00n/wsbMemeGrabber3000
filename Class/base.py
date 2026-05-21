from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests, json, copy, html, time, os, re

class Base:
    def __init__(self):
        ua = UserAgent()
        self.userAgent = ua.chrome

    def fetch(self,url,method="GET",payload={},max=5):
        headers = {'User-Agent': self.userAgent}
        crashed = False
        for run in range(1,max):
            try:
                if method == "POST":
                    req = requests.post(url, headers=headers, json=payload, timeout=(5,5))
                elif method == "GET":
                    req = requests.get(url, headers=headers, timeout=(5,5))
                else:
                    req = requests.patch(url, headers=headers, json=payload, timeout=(5,5))
                if req.status_code == 200: 
                    return True,req
                else:
                    return False,req
            except Exception as ex:
                crashed = True
                pass
            if run == 4 and not crashed:
                return False,req
            elif run == 4:
                return False,None
            time.sleep(2)

    def getUrls(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        for link in soup.find_all('a'): urls.append(link.get('href'))
        return urls

    def filterUrls(self,urls,keyword):
        tmpUrls = copy.deepcopy(urls)
        for url in list(tmpUrls):
            if url is None:
                tmpUrls.remove(url)
                continue 
            if not keyword in url:
                tmpUrls.remove(url)
        return tmpUrls

    def fully_unescape(self,s):
        while True:
            new_s = html.unescape(s)
            if new_s == s:
                return s
            s = new_s

    def grabPictures(self,src):
        pictures =  re.findall(r'https://[^\s"\']*preview[^\s"\']*', src)
        urls = []
        for url in pictures:
            url = self.fully_unescape(url)
            url = url.rstrip('"\'')
            urls.append(url)
        return urls

    def readFile(self,path):
        if os.path.isfile(path):
            try:
                with open(path) as handle: return True,json.loads(handle.read())
            except Exception as e:
                return False,{}
        else:
            return False,{}

    def saveFile(self,path,data):
        try:
            with open(path, 'w') as f: json.dump(data, f, indent=4)
        except Exception as e:
            return False
        return True
