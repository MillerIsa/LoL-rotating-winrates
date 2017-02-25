'''
Created on Feb 17, 2017

@author: Brian-VAIO
'''
from riot_api import RiotAPI 
import passkey
import consts
from windatasort.win_collector import WinCollector
def main():
    api=initialize()   
    #r=api.get_summoner_by_id(62601084,49330575,20378336) 
    winning=WinCollector(api)
    winning.spider(60683268, consts.GAME_MODES['poro_king'])
    winning.examineGameHistory(60683268,consts.GAME_MODES['poro_king'])
    print (winning.winDict)
    r=api.get_game_history(60683268)['games'][0]['fellowPlayers'][0]
    print (r)
    print('Total games collected:',winning.getGamesCollected())
    print('GameIds',winning.lists['games'])

def initialize():
    api = RiotAPI(passkey.API_KEY)
    #CHAMPION_NAMES = api.champ_names_builder()
    #print (CHAMPION_NAMES)
    return api
#builds the list of champ ids to names

    
    
    

if __name__ == "__main__":
    main()
    