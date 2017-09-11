#!flask/bin/python
import sys
import json
import requests
import datetime
from collections import defaultdict
from dota2test_model import *

def get_wl(user,timeline,day):
	under_1day = datetime.datetime.utcnow() - datetime.timedelta(1)
	search_param = {'user_id':user, 'timeline':timeline, 'timestamp': {'$gte': under_1day}}
	wl_from_db_count = count_data_mongo('players_wl', search_param)
	if wl_from_db_count > 0:
		wl_from_db = find_data_mongo('players_wl', search_param)
		wl_data = wl_from_db[0]['data']
	else:
		if timeline != 'alltime':
			url_api = 'https://api.opendota.com/api/players/%s/wl?date=%s' % (str(user), str(day))
		else:
			url_api = 'https://api.opendota.com/api/players/%s/wl' % (user)
		response = requests.get(url_api, verify=False)
		wl_data = json.loads(response.text)
		try:
			wl_data['winrate'] = float(wl_data['win'])/wl_data['lose']
		except:
			wl_data['winrate'] = 0.0
		if response.status_code == 200:
			save_mongo = {}
			save_mongo['timeline'] = timeline
			save_mongo['data'] = wl_data
			save_mongo['user_id'] = user
			save_mongo['timestamp'] = datetime.datetime.utcnow()
			insert_data_mongo('players_wl', save_mongo)
		else:
			pass
	return wl_data

def get_totals(user):
	under_1day = datetime.datetime.utcnow() - datetime.timedelta(1)
	search_param = {'user_id':user, 'timestamp': {'$gte': under_1day}}
	totals_from_db_count = count_data_mongo('players_totals', search_param)
	if totals_from_db_count > 0:
		total_from_db = find_data_mongo('players_totals', search_param)
		total_data = total_from_db[0]['data']
	else:
		url_api = 'https://api.opendota.com/api/players/%s/totals' % (str(user))
		response = requests.get(url_api, verify=False)
		total_data = json.loads(response.text)
		if response.status_code == 200:
			save_mongo = {}
			save_mongo['data'] = total_data
			save_mongo['user_id'] = user
			save_mongo['timestamp'] = datetime.datetime.utcnow()
			insert_data_mongo('players_totals', save_mongo)
		else:
			pass
	return total_data

def get_return_wl_data(users):
	days = {'week':7,'month':30,'year':365,'alltime':0}
	return_data = {}
	save_data = defaultdict(dict)
	for day in days:
	    return_temp = {}
	    for user in users:
	    	user = str(user)
	        wl_orig = get_wl(user,day,days[day])
	        return_temp[user] = wl_orig
	        save_data[user][day] = wl_orig
	    return_data[day] = return_temp
	return return_data

def get_return_total_data(users):
	totals_data = {}
	for user in users:
		user = str(user)
		totals_data[user] = get_totals(user)
	return totals_data

def get_heroes(user):
	under_1day = datetime.datetime.utcnow() - datetime.timedelta(1)
	search_param = {'user_id':user, 'timestamp': {'$gte': under_1day}}
	heroes_from_db_count = count_data_mongo('players_heroes', search_param)
	if heroes_from_db_count > 0:
		hero_from_db = find_data_mongo('players_heroes', search_param)
		hero_data = hero_from_db[0]['data']
	else:
		#only take the history heroes with win radiant and significant
		url_api = 'https://api.opendota.com/api/players/%s/heroes?is_radiant=1&significant=1' % (str(user))
		response = requests.get(url_api, verify=False)
		hero_data = json.loads(response.text)
		if response.status_code == 200:
			save_mongo = {}
			save_mongo['data'] = hero_data
			save_mongo['user_id'] = user
			save_mongo['timestamp'] = datetime.datetime.utcnow()
			insert_data_mongo('players_heroes', save_mongo)
		else:
			return False
	return hero_data

def get_final_rangking(return_data):
	final_data = {}
	for rdata in return_data:
		order_data = sorted(return_data[rdata], key=lambda k: return_data[rdata][k]['winrate'], reverse=True)
		final_data[rdata] = [{elem:return_data[rdata][elem]} for elem in order_data]
	return final_data

def get_final_comparison(return_data):
	final_data = {}
	attributes = [['sum_kills',0],['sum_deaths',1],['sum_assists',2]]
	for att in attributes:
		final_data[att[0]] = {}
		for rdata in return_data:
			try:
				final_data[att[0]][rdata] = return_data[rdata][att[1]]['sum']
			except:
				final_data[att[0]][rdata] = '-'
	return final_data

def get_best_hero(return_data):
	final_data = {}
	dict_data_all = {d["hero_id"]: d for d in return_data}
	dict_data = { k:v for k, v in dict_data_all.items() if v['games'] != 0}
	#order the heros based on number of win per number of games using the heroes
	order_data = sorted(dict_data, key=lambda k: float(dict_data[k]['win'])/dict_data[k]['games'], reverse=True)
	try:
		final_data['hero_id'] = order_data[0]
		final_data['hero_stats'] = dict_data[order_data[0]]
	except:
		final_data = False
	return final_data