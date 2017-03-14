#encoding:utf-8
'''
Created on Feb 25, 2017

@author: xhu
'''


import requests, json
from localRuleEngine.analyze_query import correct_datetime_entity_resolution

luis_api = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/a1baba10-5442-44e1-9246-53a27ced4f19?subscription-key={subKey}&verbose=true&q="

def get_sentence_analysis(subscription_key, query):
    global luis_api
    url = luis_api.format(subKey=subscription_key) + query
    try:
        r = requests.get(url, None)
        if r.status_code != 200:
            print r.reason
            return None
        content = r.text
        return json.loads(content)

    except:
        return None
    return None


def get_intent(luis_result):
    ''' resolve intent & score from luis response
{
  "query": "昨天北京天气如何",
  "topScoringIntent": {
    "intent": "weather",
    "score": 0.9959259
  },
  "intents": [
    {
      "intent": "weather",
      "score": 0.9959259
    },
    {
      "intent": "None",
      "score": 0.0369909145
    },
    {
      "intent": "greeting",
      "score": 0.000822392758
    }
  ],
  "entities": [
    {
      "entity": "北京",
      "type": "location",
      "startIndex": 2,
      "endIndex": 3,
      "score": 0.902106941
    },
    {
      "entity": "天气",
      "type": "weather",
      "startIndex": 4,
      "endIndex": 5,
      "score": 0.7956967
    },
    {
      "entity": "昨天",
      "type": "builtin.datetime.date",
      "startIndex": 0,
      "endIndex": 1,
      "resolution": {
        "date": "2017-03-12"
      }
    }
  ]
}
    '''
    if luis_result and 'topScoringIntent' in luis_result:
        intent_dict = luis_result['topScoringIntent']
        if intent_dict and 'intent' in intent_dict:
            return intent_dict['intent'], intent_dict['score']

    return None, 1.00


def get_entities(luis_result):
    if 'entities' in luis_result:
        entities = luis_result['entities']
        if len(entities) > 0:
            return entities
    return None


def get_datetime_entity(entities, entity_types=set(['builtin.datetime.date', 'builtin.datetime.duration'])):
    '''return list of tuple(entity, date_range_tuple)
    date_range_tuple: start, days'''
    datetime_entity= []
    if entities is None:
        return [(None,(0,1))]

    for entity in entities:
        etype = entity['type']
        if etype in entity_types:
            if 'resolution' in entity:
                    if etype == 'builtin.datetime.date':
                         datetime_entity.append(( entity['entity'], (entity['resolution']['date'], 1)))
                    if etype == 'builtin.datetime.duration':
                        #duration: PND, n day
                        duration = entity['resolution']['duration']
                        datetime_entity.append ((entity['entity'], (0, int(duration[1:-1]))))
    if len(datetime_entity)==0:
        datetime_entity.append((None,(0,1)))
    
    #correct datetime entity with local rules:
    return correct_datetime_entity_resolution(datetime_entity)


