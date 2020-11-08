from getStatistics import *
import random

def generateQuoteAndSource(query):
    sourcesSet = getURLs(query) 
    sourceQuoteDict = lookThroughSources(sourcesSet)
    source1, quotes = random.choice(list(sourceQuoteDict.items()))
    randSourceEntry = random.choice(list(quotes))
    source2, quotes2 = random.choice(list(sourceQuoteDict.items()))
    randSourceEntry2 = random.choice(list(quotes2))
    print("separate")
    print(source1, randSourceEntry, source2, randSourceEntry2)
    return (source1, randSourceEntry, source2, randSourceEntry2)

generateQuoteAndSource("immigration good")

#i need
statusAbout = 7
stance = 8
#source1, content1 = generateQuoteAndSource("abortion")
#source2, content2 = generateQuoteAndSource("abortion")

"""
emailText = f'''Dear Congress Person {senator}:
My name is {name} and I reside at [Insert Your Address] in [Insert Your City], South Carolina.  I am {statusAbout}.  
I am writing you about {issue}, and asking that you stand {stance} it. 
This issue is important to me because:
According to {source1}, \" {content1}\"
And according to {source2}, \" {content2}\"
I appreciate your help and ask that you please send me a response letting me know if you are able to pass a Bill that would improve lives of American citizens like me.
Thank you for your time and considering my request.
Sincerely,
{name}
'''
"""