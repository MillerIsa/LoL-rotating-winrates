'''
Created on Feb 17, 2017

@author: Brian-VAIO
'''
from riot_api import RiotAPI 
from sheets import PrintToReddit
import passkey
import consts
from windatasort.win_collector import WinCollector
def main(rootSumm='mantia',gameMode='nexus_seige'):
    #PrintToReddit().updateTable2()
    api=initialize()   
    #r=api.get_summoner_by_id(62601084,49330575,20378336)
    #36179556
    #print('returned:',api.get_summoner_by_name('mantia'))
    rootSummId=api.get_summoner_by_name(rootSumm)[rootSumm]['id']
    #print('rootSummName is:',rootSumm)
    #print ('rootSummId is:',rootSummId)
    #print (r) 
    winning=WinCollector(api)
    goodRoot=winning.seedSumm(rootSummId,consts.GAME_MODES[gameMode])
    print('good root is:',goodRoot)
    winning.spider(goodRoot, consts.GAME_MODES[gameMode])
    print('times rate limit was exceeded:',api.timesLimExceeded)
    #winning.examineGameHistory(60683268,consts.GAME_MODES['poro_king'])
    #print (winning.winDict)
    #print('lists are:',winning.lists)
    
    print('Total games collected:',winning.winDict['totalGames'])
    #print ('winDict is:',winning.winDict)
    #print('GameIds',winning.lists['games'])

def initialize():
    api = RiotAPI(passkey.API_KEY)
    #CHAMPION_NAMES = api.champ_names_builder()
    #print (CHAMPION_NAMES)
    return api
#builds the list of champ ids to names

    
    
    

if __name__ == "__main__":
    main()
    