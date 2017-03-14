#coding:utf-8
'''
main module
@author: xhu
'''
import sys, locale
import render
from localRuleEngine.analyze_query import extract_location
from luisEngine.client import get_sentence_analysis, get_intent, get_datetime_entity, get_entities
from thinkpageApiClient.client import query_weather


def utf8_input(prompt):

    return raw_input(prompt).decode(sys.stdin.encoding or locale.getpreferredencoding(True))

def understand_query(luis_subscription_key, query):
    #find locations using local rule engine
    location = extract_location(query) or '北京'
    print "location: %s" % location
    #analyze query, get the intent and entities
    luis_result = get_sentence_analysis(luis_subscription_key, query)
    intent, score = get_intent(luis_result)
    print "Intent =  '" , intent, "'  with score = ", score
        
    return location, intent, luis_result

def perform_and_render(time_entity_list, location, thinkpage_api_key):
    for time_entity, date_range in time_entity_list:
        if time_entity:
            print "time request is ",time_entity 
        else:
            date_range = (0, 1)  #(start, days)
            print "time request is 今天"

        #form a query for thinkpage api
        thinkpage_result = query_weather(location, date_range, thinkpage_api_key)
        #render the answer template
        if thinkpage_result:
            template = render.render_response(thinkpage_result, location, date_range)
            print "Weather : \n", template
        else:
            print "Can't get query results from thinkpage api"
                
if __name__ == '__main__':

    thinkpage_api_key = "u6hurepwh5jpbnoo"
    luis_subscription_key = 'ea3553224519428c833af1242ea2fad9'

    query = utf8_input('Input your weather query, input # to exit:')
    query = query.strip()

    while query != "#":
        #extract location, intent
        location, intent, luis_result = understand_query(luis_subscription_key, query)

        if intent != "weather":
            print "Not support the intent for now"
            query = raw_input("Input your weather query, input # to exit:")
            query = query.strip()
            continue

        #extract time entity from the query via luis
        time_entity_list = get_datetime_entity(get_entities(luis_result))
        
        #query weather and render
        perform_and_render(time_entity_list, location, thinkpage_api_key)

        query = utf8_input("Input your weather query, input # to exit:")
        query = query.strip()

    print "exit"


