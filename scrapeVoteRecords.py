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

#topic and chamber MUST have first letter capitalized
def findIntroducedBills(topic, chamber, specificInterest, userBelief):
    topic.replace(" ", "+")
    url = "https://www.congress.gov/search?searchResultViewType=expanded&q=%7B%22source%22%3A%22legislation%22%2C%22search%22%3A%22" + specificInterest + "%22%2C%22congress%22%3A%5B%22116%22%5D%2C%22chamber%22%3A%22" + chamber + "%22%2C%22subject%22%3A%22" + topic + "%22%2C%22bill-status%22%3A%22introduced%22%7D"
    req = requests.get(url, headers)
    print(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    billNums = soup.find_all("span", class_="result-heading")
    billTitles = soup.find_all("span", class_="result-title")
    billParties = soup.find_all("span", class_="result-item")
    for i in range(len(billNums)):
        billNums[i] = billNums[i].find("a").get_text()
        billTitles[i] = billTitles[i].get_text()
        if "[R" in billParties[i].get_text():
            billParties[i] = "R"
        elif "[D" in billParties[i].get_text():
            billParties[i] = "D"
        else:
            billParties[i] = "I"
    result = []
    userAgreement = [False] * len(billNums)
    for i in (0,10):
        try:
            print(str(billNums[i]) + " : " + str(billTitles[i]) + " : " + str(billParties[i]))
            result.append((billNums[i], billTitles[i], userAgreement[i]))
        except:
            pass


def billIdeology(url):
    req = requests.get(url, headers)
    #print(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    partyCounts = soup.find_all("span", class_="count")
    republicanCount, democratCount, independentCount = (0,0,0)
    for element in partyCounts[0:2]:
        number = element.get_text()[1:len(element.get_text())]
        number = number[0:len(number) - 1]
        print(type(number))
        #print(element.get_text())
        if element.get("id") == "facetItempartyRepublicancount":
            republicanCount = int(element.get_text()[1:len(element.get_text() - 1)])
        elif element.get("id") == "facetItempartyDemocraticcount":
            democratCount = int(element.get_text()[1:len(element.get_text() - 1)])
        else:
            independentCount = int(element.get_text()[1:len(element.get_text() - 1)])
    if democratCount == 0:
        return "R"
    score = republicanCount / democratCount
    print(republicanCount, democratCount, independentCount, score)
    if score > 2.333: #represents at least 70% of cosponsors are republican
        return "R"
    elif score < .428: #at least 70% of cosponsors are democrat
        return "D"
    return "Bipartisan"
    

findIntroducedBills("Health", "House", "abortion", "D")

#print(billIdeology("https://www.congress.gov/bill/116th-congress/house-bill/20/cosponsors?q={%22search%22:[%22abortion%22]}&s=2&r=1&overview=closed&searchResultViewType=expanded"))