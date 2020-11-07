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

def findSenators(state):
    senatorsUrl = "https://en.wikipedia.org/wiki/List_of_United_States_senators_from_" + state
    req = requests.get(senatorsUrl, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    currentSenators = soup.select("div[class='thumbcaption text-align-center']")
    value = set()
    for senator in currentSenators:
        person = senator.find("a").get_text()
        value.add(person)
    return value

def findHouseRep(zipCode):
    houseUrl = "https://ziplook.house.gov/htbin/findrep_house?ZIP=" + str(zipCode)
    req = requests.get(houseUrl, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    currentRep = soup.find("div", id="PossibleReps").find("a").get_text()
    return currentRep




findHouseRep(15213)
