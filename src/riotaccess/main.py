'''
Created on Feb 17, 2017

@author: Brian-VAIO
'''
from riot_api import RiotAPI 
from sheets import PrintToReddit
import passkey
import consts
from windatasort.win_collector import WinCollector
def main(rootSumm='Direwolf23',gameMode='normals'):
    PrintToReddit().updateTable()
    api=initialize()   
    #r=api.get_summoner_by_id(62601084,49330575,20378336)
    #36179556
    rootSummId=api.get_summoner_by_name(rootSumm)['names']['id']
    print ('rootSummId is:',rootSummId)
    #print (r) 
    winning=WinCollector(api)
    winning.spider(rootSummId, consts.GAME_MODES[gameMode])
    
    #winning.examineGameHistory(60683268,consts.GAME_MODES['poro_king'])
    #print (winning.winDict)
    #print('lists are:',winning.lists)
    
    print('Total games collected:',winning.getGamesCollected())
    #print('GameIds',winning.lists['games'])

def initialize():
    api = RiotAPI(passkey.API_KEY)
    #CHAMPION_NAMES = api.champ_names_builder()
    #print (CHAMPION_NAMES)
    return api
#builds the list of champ ids to names

    
    
    

if __name__ == "__main__":
    main()
    