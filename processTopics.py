from dataclasses import make_dataclass

# interest is yes, no or "unanswered"
topic = make_dataclass('Topic', 
    ['name','interest', 'options', 'opinion','opinionSaved'])

#issues = make_dataclass('Issues', ['topics', 'currTopicIndex'])
'''
topicDict = {
    'legalized abortion' : ['pro-life', 'pro-choice']
    'gun rights' : ['favor gun control', 'oppose gun control']
    'tax the ultra-wealthy' : ['oppose wealth tax', 'favor wealth tax']
    'undocumented immigration' : ['support deportation', 'favor assimilation']
}

listOfTopics = list()
for topic in topicDict:
    listOfTopics.append(interest = "unanswered", name = topic, 
        options = topicDict[topic], 'opinionSaved' = False)

currTopic = 0
'''
# when we start iterating through, everytime "unanswered" is unchecked
# currTopic increases
