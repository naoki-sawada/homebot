from homebot import *

nlp = NLP('test.json')

#ret = nlp.search('おはよう')
#ret = nlp.search('おやすみ')
ret = nlp.search('電気けして')
#ret = nlp.search('天気')

print(ret)
