'''
Created on Feb 20, 2017

@author: Brian-VAIO
'''
from riotaccess.riot_api import RiotAPI 
class WinCollector:
    'uses riot_api instance object to initialize the winDict with correct champion Ids and names. Also initializes the game statistics to zero.'
    #needs a RiotAPI object to perform data collection
    def __init__(self,riot_api):
        self.api=riot_api
        chmpNames=self.api.champ_names_builder()
        self.winDict=dict.fromkeys(chmpNames)
        for chmpId in chmpNames:  
            chmpName=chmpNames[chmpId]
            self.winDict[chmpId]={'chmpName':chmpName,'wins':0,'losses':0,'totalGames':0,'mirrorMatches':0}
            
    def spider(self):
        'pulls game data for statistical analysis and stores the portions of the data in winDict'
        #write game data pull in riot_api since I don't understand the data structure of RecentGamesDto very well
        #pulls the win/loss data for an individual game
        examineGameHistory(00000000)
        #does not include PlayerDto of KEY player
        
    def examineGameHistory(self,keyPlayerId):
        keyPlayerId=keyPlayerId
        history=self.api.get_game_history(keyPlayerId)
        games=history['games']
        for game in games:
            #records win stats of the key player
            chmpId=game['championId']
            chmpEntry=self.winDict[chmpId]
            print (game)#testing purposes
            if game['stats']['win'] == True:
                chmpEntry['wins']+=1
            else:
                chmpEntry['losses']+=1
            chmpEntry['totalGames']+=1
            
            keyTeamId=game['teamId']     
            for player in game['fellowPlayers']:
                chmpId=player['championId']
                chmpEntry=self.winDict[chmpId]
                myTeamId=player['teamId']
                if (myTeamId == keyTeamId) == (game['stats']['win']):
                    chmpEntry['wins']+=1
                else:
                    chmpEntry['losses']+=1
                chmpEntry['totalGames']+=1   
                
        #api.get_game_history(keyPlayerId)['games'][0]['fellowPlayers'][0]
    def getGamesCollected(self):
        collectedGames=0
        for chmpEntry in self.winDict:
            print(self.winDict[chmpEntry])
            collectedGames+=self.winDict[chmpEntry]['totalGames']
        return collectedGames #/ 10
            
        
        