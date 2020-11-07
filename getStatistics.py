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
  
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

# to search
def getURLs(q): 
    query = q
    sites = set()
    for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
        sites.add(j)
    return sites 

#looks through all the sites makes dictionary of sources to key quotes
def lookThroughSources(sites):
    sentenceDict = dict()
    for address in sites:
        text = getPageText(address)
        if text == None:
            continue
        searchPageText(text, sentenceDict, address)

    return sentenceDict
    
def getPageText(address):
    url = address

    values = {'language': 'Python' }
    headers = {'User-Agent': "Mozilla/5.0"}

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data, headers)
    try:
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
    except:
        return
    return text


#retrieve the notable quotes
def searchPageText(text, localDict, address):
    sentences = split_into_sentences(text)
    sourceSet = set()
    keyList = ["according to", "percent", "%", "reason", "number", "because", "said", "sample", "study", "research", "researchers", "survey", "findings", "found"]
    for element in sentences:
        if len(element.split(" ")) < 6:
            continue
        else:
            for keyWord in keyList:
                if re.search(keyWord, element.lower()):
                    sourceSet.add(element)
    localDict[address] = sourceSet



sourcesSet = getURLs("tax wealthy good") 
lookThroughSources(sourcesSet)

