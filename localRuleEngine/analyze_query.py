#encoding:utf-8
'''
Created on 2017年2月25日

@author: xhu
'''
import codecs,re


ChineseCities = {}  # place:label, label could be Province/Location/Station
with codecs.open('../res/ChineseCities.txt','r','utf-8') as f:
    for line in f.readlines():
        if line.strip():
            arr = line.split(',')
            if len(arr) < 2:
                continue
            place, label = arr[0], arr[1]
            ChineseCities[place] = label

timeMapping = {}  # datetime entity:(start, days)
with codecs.open('../res/TimeMapping.txt','r','utf-8') as f:
    for line in f.readlines():
        if line.strip() and not line.startswith("#"):
            arr = line.split(',')
            if len(arr) < 3:
                continue
            dt, start, days = arr[0], arr[1], arr[2]
            timeMapping[dt] = (start, days)


def extract_location(query):
    '''find the location by matching the local Chinese cities dict'''
    global ChineseCities
    for place in ChineseCities:
        if query.find(place) >= 0:
            return place
    return None

def correct_datetime_entity_resolution(datetime_entity_list):
    '''find the location by matching the local Chinese cities dict'''
    final_entities = {}
    global timeMapping
    for en, drange in datetime_entity_list:
        if en in final_entities:
            #means more than two times in the result for the same datetime entity
            #check whether it could be corrected with local rule
            reduced_en = en.replace(u'与','').replace(u'和','').replace(u'、','').replace(u' ','')
            if reduced_en in timeMapping:
                final_entities[en] = timeMapping[reduced_en]
        else:
            final_entities[en] = drange
    return final_entities.items()

if __name__=="__main__":
    entity = u'今天与明天'
    print correct_datetime_entity_resolution(entity, -1 ,1)
    
    query = u'今天明天上海天气'
    print extract_location(query)
