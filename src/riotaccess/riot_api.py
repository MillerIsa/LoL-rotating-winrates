'''
Created on Feb 17, 2017

@author: Brian-VAIO
'''
#from ratelimit import rate_limited
import requests
import consts
import time
from riotaccess.consts import API_VERSIONS
#import ratelimit

class RiotAPI(object):       

    def __init__(self, api_key, region=consts.REGIONS['north_america']):
        self.api_key = api_key
        self.region = region
        initialTime=time.process_time()
        #'timeSent' represents the time that the first request within the given time window was made
        self.secLim={'countLeft':10,'timeSent':initialTime}
        self.minLim={'countLeft':500,'timeSent':initialTime}  
        self.timesLimExceeded=0
        
    #base request method, assumes dynamic request unless specified
    #@return: dictionary object OR an integer representing the http response code in case of response failure
    #rate limits are applied properly when request method is called through tenMinLimit()
    #check http response code before attempting to use response data
    def _request(self, api_url,is_static=False, params={},retryDelay=1):
        #print('api_url_is',api_url)
        if is_static:
            args = {'api_key':self.api_key}
            for key, value in params.items():
                if key not in args:
                    args[key] = value
            base=consts.URL['static_base']
            response = self.httpRequest(base, api_url, args)
            if response.status_code == 200:return response.json()
            else:
                print('response.status_code:'.join([str(response.status_code),', ',consts.RESPONSE_CODES[response.status_code],'. Retry after:',str(retryDelay),' seconds']))
                #print('response.status_code:', + str(response.status_code) + ', ' + consts.RESPONSE_CODES[response.status_code] + '. Retry after:' + str(retryDelay) + ' seconds')
                time.sleep(retryDelay)
                if retryDelay < 600:retryDelay += 10
                return self._request(api_url, is_static,retryDelay=retryDelay)
            return response.status_code

                
                      
            
        #check to see if request is allowed by the rate limit      
        if time.process_time() - self.minLim['timeSent'] > 600:
            self.minLim['countLeft']=500
        #print(time.process_time() - self.secLim['timeSent'])
        if time.process_time() - self.secLim['timeSent'] > 10:
            self.secLim['countLeft']=10
        if self.minLim['countLeft'] > 0 and self.secLim['countLeft'] > 0:        
            args = {'api_key':self.api_key}
            for key, value in params.items():
                if key not in args:
                    args[key] = value  
            base=consts.URL['base']
            response=self.httpRequest(base, api_url, args)
            if response.status_code == 200 or response.status_code == 429:
                #record request info for rate limit management 
                newTime=time.process_time()
                #unpacks 'X-Rate-Limit-Count' response header
                x=0
                secCount=''
                minCount=''
                header=response.headers['X-Rate-Limit-Count']
                while (x < len(header)):
                    if header[x] == ':':
                        while (header[x] != ','):
                            x+=1
                        x+=1
                        while (header[x] != ':'):
                            minCount+=header[x]
                            x+=1
                        secCount = int(secCount)
                        minCount = int(minCount)
                        break
                    secCount+=header[x]
                    x+=1
                #print('secCount is:',secCount,'minCount is:',minCount)
                self.minLim['countLeft']=500 - minCount
                self.secLim['countLeft']=10 - secCount
                #reset time if this is the first request in a time window
                if self.minLim['countLeft'] == 499:
                    self.minLim['timeSent']=newTime
                if self.secLim['countLeft'] == 9:
                    self.secLim['timeSent']=newTime
            if response.status_code == 429:
                self.timesLimExceeded+=1
                if 'X-Rate-Limit-Type' in response.headers:
                    print(response.headers['X-Rate-Limit-Type'])
                    print('rate limit exceeded, retry after:',response.headers['Retry-After'])
                    time.sleep(int(response.headers['Retry-After']))
                    return self._request(api_url, is_static)
                else:print('Rate limit was enforced by the underlying service to which the request was proxied.')
                return response.status_code
            if response.status_code == 200: return response.json()
            else:
                print('response.status_code:'.join([str(response.status_code),', ',consts.RESPONSE_CODES[response.status_code],'. Retry after:',str(retryDelay),' seconds']))
                #print('response.status_code:', + str(response.status_code) + ', ' + consts.RESPONSE_CODES[response.status_code] + '. Retry after:' + str(retryDelay) + ' seconds')
                time.sleep(retryDelay)
                if retryDelay < 600:retryDelay += 10
                return self._request(api_url, is_static,retryDelay=retryDelay)
                
        else:
            if self.secLim['countLeft'] <= 0:
                retryAfter=10 - (time.process_time() - self.secLim['timeSent'])
                if retryAfter < 0.01:retryAfter=0.01
                print('retryAfter:',retryAfter)
                self.secLim['timeSent']-=retryAfter
                time.sleep(retryAfter)
                return self._request(api_url, is_static)
            if self.minLim['countLeft'] <= 0:
                retryAfter=600 - (time.process_time() - self.minLim['timeSent'])
                if retryAfter < 0.01:retryAfter=0.01
                self.minLim['timeSent']-=retryAfter
                time.sleep(retryAfter)
                return self._request(api_url, is_static)
        print('error,Rate limiting bug occurred ','self.secLim[\'countLeft\'] is:',self.secLim['countLeft'],'self.minLim[\'countLeft\'] is:',self.minLim['countLeft'])
        return 10
    def httpRequest(self,base,api_url,args,retryAfter=60):
        try:
                response = requests.get(           
                    base.format (
                        proxy=self.region,
                        region=self.region,
                        url=api_url
                        ),
                    params=args
                    )
                return response
        except:
            print('error requesting url, retry after:',str(retryAfter))
            time.sleep(retryAfter)
            return self.httpRequest(base, api_url, args, retryAfter)
        
 
    
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
        print('name to retriev is:',name)
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
        if type(tempDict) != dict:print('error retriving chmpNames:',tempDict)
        for name in tempDict['data']:
            chmpDict[tempDict['data'][name]['id']]=name
        return chmpDict
    

            
        

    
                