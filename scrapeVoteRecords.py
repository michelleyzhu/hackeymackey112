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
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    billNums = soup.find_all("span", class_="result-heading")[::2]
    billTitles = soup.find_all("span", class_="result-title")[::2]
    billCosponsors = soup.find_all("span", class_="result-item")[::8]
    billUrls = []
    for i in range(10):
        try:
            links = billCosponsors[i].find_all("a")
            billCosponsors[i] = "https://www.congress.gov/" + links[1].get("href")
            billUrls.append(billNums[i].find("a").get("href"))
        except:
            pass
    billParties = ["R"] * len(billNums)
    for i in range(10):
        try:
            billNums[i] = billNums[i].find("a").get_text()
            billTitles[i] = billTitles[i].get_text()
            links = billUrls[i].find_all("a")
            cosponsorLink = "https://www.congress.gov/" + links[1].get("href")
            billParties[i] = billIdeology(cosponsorLink)
            print(i)
        except:
            pass
    result = []
    userAgreement = [False] * len(billNums)
    for i in range(10):
        try:
            userAgreement[i] = (billParties[i] == "I" or billParties[i] == userBelief)
            print(billParties[i])
            result.append((billNums[i], billTitles[i], userAgreement[i], billUrls[i]))
        except:
            pass
    return result
        

def billIdeology(url):
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    partyCounts = soup.find_all("span", class_="count")
    republicanCount, democratCount, independentCount = (0,0,0)
    for element in partyCounts[0:2]:
        number = element.get_text()[1:len(element.get_text())]
        number = int(number[0:-1])
        if element.get("id") == "facetItempartyRepublicancount":
            republicanCount = number
        elif element.get("id") == "facetItempartyDemocraticcount":
            democratCount = number
        else:
            independentCount = number
    if democratCount == 0 and republicanCount !=0:
        return "R"
    elif democratCount == 0:
        return "Bipartisan"
    score = republicanCount / democratCount
    if score > 2.333: #at least 70% of cosponsors are republican
        return "R"
    elif score < .428: #at least 70% of cosponsors are democrats
        return "D"
    return "Bipartisan"
    

#print(findIntroducedBills("Health", "House", "abortion", "D"))

print(billIdeology("https://www.congress.gov/bill/116th-congress/house-bill/1692/cosponsors?q={%22search%22:[%22abortion%22]}&r=3&s=2&searchResultViewType=expanded"))