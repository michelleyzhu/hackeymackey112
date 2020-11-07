#for finding reps and their emails
import requests
from bs4 import BeautifulSoup4
soup = BeautifulSoup(html_doc, 'html.parser')

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def find-senators(state):
    senators-url = "https://en.wikipedia.org/wiki/List_of_current_United_States_senators"
    req = requests.get(senators-url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    print(soup.prettify())
