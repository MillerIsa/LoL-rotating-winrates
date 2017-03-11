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
    #print (r) 
    winning=WinCollector(api)
    winning.spider(36179556, consts.GAME_MODES['ascension'])
    winning.stater.calcAll()
    winning.stater.printCalcs()
    
    #winning.examineGameHistory(60683268,consts.GAME_MODES['poro_king'])
    print (winning.winDict)
    print('lists are:',winning.lists)
    
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
    