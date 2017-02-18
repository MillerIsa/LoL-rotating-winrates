'''
Created on Feb 17, 2017

@author: Brian-VAIO
'''
URL = {
    'base':'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
    'summoner_by_name':'v{version}/summoner/by-name/names',
    'summoner_by_id':'v{version}/summoner/{summonerIds}',
    'game_history':'v{version}/game/by-summoner/{summonerId}/recent',
    'match':'v{version}/match/{matchId}',
    'static_base':'https://{proxy}.api.pvp.net/api/lol/static-data/{region}/{url}',
    'champion_list':'v{version}/champion'
    
    }
API_VERSIONS = {
    'summoner':'1.4',
    'game':'1.3',
    'match':'2.2',
    'champion':'1.2'
    }
REGIONS = {
    'north_america':'na',
    'europe_nordic_and_east':'eune',
    'europe_west':'euw'
    }
