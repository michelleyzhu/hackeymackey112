#get the information for the blanks

#put the information in the blank
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re


try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 
  
# to search
def getURLs(q): 
    query = q
    sites = set()
    for j in search(query, tld="co.in", num=3, stop=3, pause=2): 
        sites.add(j)
    return sites 


def lookThroughSources(sites):
    sentenceSet = set()
    for address in sites:
        text = getPageText(address)
        searchPageText(text, sentenceSet)

def getPageText(address):
    url = address
    #html = urlopen(url).read()
    #soup = BeautifulSoup(html, features="html.parser")

    values = {'language': 'Python' }
    headers = {'User-Agent': "Mozilla/5.0"}

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def searchPageText(text, set):
    sentences = text.split("\n") 
    #according to

    #percent

    #results in

    #query [1......n]
sourcesSet = getURLs("gun control bad") 
lookThroughSources(sourcesSet)


'''
Hello my name is ____. I live in ______. 

I noticed on this_____ you voted this______. This matters to me a lot, and I believe ______.



I am emailing you about ______. Here is why this issue is important:
Generate 6 statistics
They pick 3 that speak to them'''