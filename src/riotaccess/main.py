'''
Created on Feb 17, 2017

@author: Brian-VAIO
'''
from riot_api import RiotAPI 
from sheets import PrintToReddit
from sheets import FormatSheets
import passkey
import consts
from windatasort.win_collector import WinCollector
def main(rootSumm='mantia',gameMode='arsr'):
    #PrintToReddit().updateTable2()
    #FormatSheets().format()
    api=initialize()   
    #r=api.get_summoner_by_id(62601084,49330575,20378336)
    #36179556
    #print('returned:',api.get_summoner_by_name('mantia'))
    rootSummId=api.get_summoner_by_name(rootSumm)[rootSumm]['id']
    winning=WinCollector(api)
    goodRoot=winning.seedSumm(rootSummId,consts.GAME_MODES[gameMode])
    #print('good root is:',goodRoot)
    winning.spider(goodRoot, consts.GAME_MODES[gameMode])
    #winning.spiderAll(60683268)
    #print('times rate limit was exceeded:',api.timesLimExceeded)
    #winning.examineGameHistory(60683268,consts.GAME_MODES['poro_king'])
    #findParticularHist(api)
    
    #print('Total games collected:',winning.winDict['totalGames'])
    #print ('winDict is:',winning.winDict)
    #print('GameIds',winning.lists['games'])
def findParticularHist(api):
    history=api.get_game_history(59892834)
    games=history['games']
    for game in games:
        print('game mode is:',game['gameMode'],'game subType is:',game['subType'],"mapId is:",game['mapId'])
        print('championId is:',game['championId'])
        champNames=api.champ_names_builder()
        print('champ name is:',champNames[game['championId']])
def initialize():
    api = RiotAPI(passkey.API_KEY)
    #CHAMPION_NAMES = api.champ_names_builder()
    #print (CHAMPION_NAMES)
    return api
#builds the list of champ ids to names

    
    
    

if __name__ == "__main__":
    main()
    