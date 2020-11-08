from getStatistics import *
import random

def generateQuoteAndSource(query):
    sourcesSet = getURLs(query) 
    sourceQuoteDict = lookThroughSources(sourcesSet)
    source1, quotes = random.choice(list(sourceQuoteDict.items()))
    randSourceEntry = random.choice(list(quotes))
    source2, quotes2 = random.choice(list(sourceQuoteDict.items()))
    randSourceEntry2 = random.choice(list(quotes2))
    return ((source1, randSourceEntry, source2, randSourceEntry2))

