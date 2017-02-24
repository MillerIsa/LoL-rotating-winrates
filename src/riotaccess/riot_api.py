'''
Created on Feb 17, 2017

@author: Brian-VAIO
'''
#from ratelimit import rate_limited
import requests
import consts
from riotaccess.consts import API_VERSIONS
#import ratelimit

class RiotAPI(object):
    #count of requests left in 10 seconds, count of requests left in 600 seconds,time that first request in the time window was sent for each
    class PrevReq:
        def __init__(self):
            #self.secLim={'countLeft':10,'timeSent':}
            #self.minLim{'countLeft':600,'timeSent':}        

    def __init__(self, api_key, region=consts.REGIONS['north_america']):
        self.api_key = api_key
        self.region = region
        
        self.secLim={'countLeft':10,'timeSent':0}
        self.minLim{'countLeft':600,'timeSent':0}  
        
        #base request method, assumes dynamic request unless specified
        #@return: dictionary object
    #rate limits are applied properly when request method is called through tenMinLimit()
    #@rate_limited(500,600)
    def _request(self, api_url,is_static=False, params={}):
                
        args = {'api_key':self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        if is_static:
            base=consts.URL['static_base']
        else:
            base=consts.URL['base']
        response = requests.get(           
            base.format (
                proxy=self.region,
                region=self.region,
                url=api_url
                ),
            params=args
            )
        print (response.url)
        return response.json()
    
    
    #does NOT count against rate limit
    #@return dictionary of champion info 
    def get_champion_list (self):
        api_url=consts.URL['champion_list'].format(
            version=consts.API_VERSIONS['champion']
            )
        return self._request(api_url,True)
    
    #specific request methods
    def get_summoner_by_name(self, name):
        api_url=consts.URL['summoner_by_name'].format(
            version=consts.API_VERSIONS['summoner'],
            names=name
            )
        return self._request(api_url)
    
    #@param summ IDs can be in String form or number form (I think)
    #@param list(tuple actually) of up to 40 summoner IDs to retrieve
    #@return: dictionary object containing summoner info
    def get_summoner_by_id(self,summonerID,*summonerIDs):
        summonerIDsString = str(summonerID)
        it=iter(summonerIDs)
        for ID in it:
            summonerIDsString=summonerIDsString + ',' + str(ID)
        api_url=consts.URL['summoner_by_id'].format(
            version=consts.API_VERSIONS['summoner'],
            summonerIds=summonerIDsString
            )
        return self._request(api_url)
        
    def get_game_history(self,summonerID):
        api_url=consts.URL['game_history'].format(
            version=API_VERSIONS['game'],
            summonerId=summonerID)
        return self._request(api_url)
    #@return dictionary object with data on the match    
    def get_match(self,matchID):
        api_url=consts.URL['match'].format(
            version=API_VERSIONS['match'],
            matchId=matchID
            )
        return self._request(api_url)
    
    def champ_names_builder(self):
        'returns a dictionary of champion ids mapped to champion names'
        chmpDict={}
        tempDict=self.get_champion_list()
        for name in tempDict['data']:
            chmpDict[tempDict['data'][name]['id']]=name
        return chmpDict
    
    #@rate_limited(500, 600)
    #def tenSecLim(self):
     #   return True
            
        

    
                