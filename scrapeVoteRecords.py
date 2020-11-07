#for finding reps and their emails
import module_manager
module_manager.review()
import requests
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def capitalizeFirstLetters(word):
    word = word.capitalize()
    if ' ' in word:
        space = word.find(' ')
        word.replace(' ', '-')
        word = word[:space + 1] + word[space + 1].upper() + word[space + 2:]
    return word

#topic and chamber MUST have first letter capitalized
def findIntroducedBills(topic, chamber, specificInterest, userBelief):
    topic = capitalizeFirstLetters(topic)
    chamber = capitalizeFirstLetters(chamber)
    url = "https://www.congress.gov/search?searchResultViewType=expanded&q=%7B%22source%22%3A%22legislation%22%2C%22search%22%3A%22" + specificInterest + "%22%2C%22congress%22%3A%5B%22116%22%5D%2C%22chamber%22%3A%22" + chamber + "%22%2C%22subject%22%3A%22" + topic + "%22%2C%22bill-status%22%3A%22introduced%22%7D"
    print(url)
    req = requests.get(url, headings)
    soup = BeautifulSoup(req.content, 'html.parser')
    #print(req.content)
    #billNums = soup.find_all(class_="result-heading")
    billNums = soup.select("span[class=result-heading]")
    print(billNums)
    #billNums = soup.find_all("span")

    billTitles = soup.find_all("span", class_="result-title")
    billUrls = soup.find_all("span", class_="result-items")
    #link to cosponsor list, has random other stuff though
    billParties = ["R"] * len(billNums)
    for i in range(len(billNums)):
        billNums[i] = billNums[i].find("a").get_text()
        billTitles[i] = billTitles[i].get_text()
        cosponsorLink = billUrls[i].find()
        billParties[i] = billIdeology(cosponsorLink)
    result = []
    userAgreement = [False] * len(billNums)
    for i in range(10):
        #try:
        print(billNums[i])
        print(str(billNums[i]) + " : " + str(billTitles[i]) + " : " + str(billParties[i]))
            #result.append((billNums[i], billTitles[i], userAgreement[i]))
        #except:
            #pass
    return result
        


def billIdeology(url):
    req = requests.get(url, headers)
    #print(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    partyCounts = soup.find_all("span", class_="count")
    republicanCount, democratCount, independentCount = (0,0,0)
    for element in partyCounts[0:2]:
        number = element.get_text()[1:len(element.get_text())]
        number = int(number[0:-1])
        #print(element.get_text())
        if element.get("id") == "facetItempartyRepublicancount":
            republicanCount = number
        elif element.get("id") == "facetItempartyDemocraticcount":
            democratCount = number
        else:
            independentCount = number
    if democratCount == 0:
        return "R"
    score = republicanCount / democratCount
    print(republicanCount, democratCount, independentCount, score)
    if score > 2.333: #at least 70% of cosponsors are republican
        return "R"
    elif score < .428: #at least 70% of cosponsors are democrat
        return "D"
    return "Bipartisan"
    

print(findIntroducedBills("international relations", "House", "abortion", "D"))

#print(billIdeology("https://www.congress.gov/bill/116th-congress/house-bill/20/cosponsors?q={%22search%22:[%22abortion%22]}&s=2&r=1&overview=closed&searchResultViewType=expanded"))