#!/usr/bin/python3
response = {}
page = 1

#{
#    "nameSurname": "Andrea",
#    "dob": "1980-06-26",
#    "prediction": "love",
#    "partnerNameSurname": "Lorenzani",
#    "partnerDob": "2022-12-12"
#}

def extractData():
	import sys, json
	myjson = json.load(sys.stdin)
	#myjson = json.loads('''{
    #"nameSurname": "Andrea Lorenzani",
    #"dob": "1980-06-26",
    #"prediction": "love",
    #"partnerNameSurname": "Marilena Bruffa",
    #"partnerDob": "1980-06-15"
#}''')
	return myjson

def sendResponse(status=200):
	print("x-header-received: yes")
	print('Status: {}'.format(status))
	print('Content-Type: application/json\n')
	import json 
	print(json.dumps(response))
	print('\n\n')

def addData(value, index='value'):
	global page, response
	import json
	newIdx = json.loads('{"%s":"%s"}' % (index, value))
	response[page] = newIdx
	page = page +1

def  physical_bio(numDays):
    return bio(numDays, 23)
    
def  emotional_bio(numDays):
    return bio(numDays, 28)
    
def  intellectual_bio(numDays):
    return bio(numDays, 33)
    
def bio(num_days, range_days):
    days_in_range = num_days % range_days
    ratio = (days_in_range*2)/range_days
    import math
    return math.sin(ratio * math.pi)

def compare(your_days, its_days, bio_fun):
    res = { 'max_value': -3, 'max_days': -1, 'min_value': 3, 'min_days': -1}
    for x in range(33):
        value = bio_fun(your_days+x) + bio_fun(its_days+x) 
        if value > res['max_value']:
            res['max_value'] = value
            res['max_days'] = x
        if value < res['min_value']:
            res['min_value'] = value
            res['min_days'] = x
    return (res['max_days'], res['min_days'], biorythm_tssize(res['max_value'], 2))

from operator import le, ge    
def max_bio(num_days, bio_fun, math_fun = ge):
    res = { 'value': None, 'days': -1}
    for x in range(33):
        if not res['value'] or math_fun(bio_fun(num_days+x), res['value']):
            res['value'] = bio_fun(num_days+x)
            res['days'] = x
    return res['days']

def biorythm_tssize(value, multiplier=1):
    if value <= -0.25 * multiplier:
        return "very low"
    elif value <= 0.1 * multiplier:
        return "low"
    elif value <= 0.5 * multiplier:
        return "below average"
    elif value <= 0.7 * multiplier:
        return "average"
    elif value <= 0.85 * multiplier:
        return "very good"
    elif value > 0.85:
        return "perfect"

def getDateFromJson(value):
	from dateutil.parser import parse
	return parse(value)

def checkAffinity(value):
	value = value.lower();
	res = (value.count('a')*10000 + value.count('m')*1000 + value.count('o')*100 + value.count('r')*10 + value.count('e'))
	while res > 110:
		res = reduceForLove(res)
	return res

def reduceForLove(value):
	maxVal = 10**(len(str(value))-1)
	minVal = 10**(len(str(value))-2)
	res = int(( (value / maxVal) + (value/minVal)%10 ) *minVal)
	return int(res)


try:
	data = extractData()
except:
	data = {}
import os
if (not os.getenv("QUERY_STRING") or os.getenv("QUERY_STRING") == '') and (not data or data == {}):
	sendResponse()
	exit()

if not data['dob']:
	addData("I cannot do any prediction without you date of birth, bitch!")
	sendResponse()
	exit()

import datetime
date_of_birth = getDateFromJson(data['dob'])
your_dob = datetime.datetime.now() - date_of_birth

if data['prediction'] == "business":
	in_byo = "Your most stimulating day will be in %s days, the apathetic one will be in %s days" % (max_bio(your_dob.days, intellectual_bio), max_bio(your_dob.days, intellectual_bio, le))
	addData(in_byo)

if data['prediction'] == "love":
	em_byo = "Your best emotional day will be in %s days, the worst will be in %s days" % (max_bio(your_dob.days, emotional_bio), max_bio(your_dob.days, emotional_bio, le))
	addData(em_byo)
	if data['partnerNameSurname'] and data['nameSurname']:
		affinity = "The affinity among you two is %s%%" % checkAffinity("%s%s" % (data['nameSurname'], data['partnerNameSurname']))
		addData(affinity)

if data['prediction'] == "health":
	ph_byo = "The day in which you will feel in your best shape will be in %s days, the one in which you will be at your minimum is in %s days" % (max_bio(your_dob.days, physical_bio), max_bio(your_dob.days, physical_bio, le))
	addData(ph_byo)

if data['prediction'] == "general":
	general_byo = "Tomorrow your physical mood will be %s, your emotional mood will be %s and your intellectual mood will be %s" % (biorythm_tssize(physical_bio(your_dob.days+1)), biorythm_tssize(emotional_bio(your_dob.days+1)), biorythm_tssize(intellectual_bio(your_dob.days+1)))
	addData(general_byo)

if data.get('partnerDob'):
	its_dob = datetime.datetime.now() - getDateFromJson(data['partnerDob'])
	phy_diff = compare(your_dob.days, its_dob.days, physical_bio)
	emo_diff = compare(your_dob.days, its_dob.days, emotional_bio)
	int_diff = compare(your_dob.days, its_dob.days, intellectual_bio)

	ph_byo = "The best day to have physical activities (included THOSE activities) with him will be in %s days, the worst is in %s days (%s)" % phy_diff
	em_byo = "The best day for romance, speaking about sentiments or for a date will be in %s days, the worst will be in %s days (%s)" % emo_diff
	in_byo = "The best day for museum, theater, a concert or an exposition will be in %s days, the worst will be in %s days (%s)" % int_diff
	addData("%s. %s. %s" % (ph_byo, em_byo, in_byo))

sendResponse()
exit()
