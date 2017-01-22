import json
 

jsonObj = json.loads(open('EkkadikiPothavuChinnavada', 'r'))

with open('EkkadikiPothavuChinnavada.json', 'r') as f:
    line = f.readline() 
    print line
    ## tweet = json.load(line) 
    ## print(json.dumps(tweet, indent=4))