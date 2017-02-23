'''
Created on Feb 20, 2017

@author: Brian-VAIO
'''
from riotaccess.riot_api import RiotAPI 
import consts
class WinCollector:
    'uses riot_api instance object to initialize the winDict with correct champion Ids and names. Also initializes the game statistics to zero.'
    #needs a RiotAPI object to perform data collection
    def __init__(self,riot_api):
        self.api=riot_api
        chmpNames=self.api.champ_names_builder()
        self.winDict={} #dict.fromkeys(chmpNames)
        self.gameList=[] #list of games collected ordered from lowest game Id to highest game Id
        for chmpId in chmpNames:  
            chmpName=chmpNames[chmpId]
            self.winDict[chmpId]={'chmpName':chmpName,'wins':0,'losses':0,'totalGames':0,'mirrorMatches':0}
            
    def examineGameHistory(self,keyPlayerId,mode):
        keyPlayerId=keyPlayerId
        history=self.api.get_game_history(keyPlayerId)
        games=history['games']
        for game in games:
            #executes suite only if the game is of the correct mode and not already counted
            if game['gameMode'] == mode.gameMode and game['subType'] == mode.subType and self.addGame(game['gameId']):             
            #records win stats of the key player
                chmpId=game['championId']
                chmpEntry=self.winDict[chmpId]
                print (game)#testing purposes
                if game['stats']['win'] == True:
                    chmpEntry['wins']+=1
                else:
                    chmpEntry['losses']+=1
                chmpEntry['totalGames']+=1
            
            #dictionary to test for mirror matches
                mirrorDict={}
                mirrorDict[chmpId]=1
            
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
                #incrimenting to find mirror match ups
                    try:
                        mirrorDict[chmpId]+=1
                    except KeyError:
                        mirrorDict[chmpId]=1   
                for chmpId in mirrorDict:
                    if mirrorDict[chmpId] % 2 == 0:
                        self.winDict[chmpId]['mirrorMatches']+=1
        return
            
    #@param rootPlayer is the summoner id of the player to start spidering from
    #@param string representing game mode      
    def spider(self,rootPlayer,gameMode):
        'pulls game data for statistical analysis and stores the portions of the data in winDict' 
        
        #pulls the win/loss data for an individual game
        self.examineGameHistory(rootPlayer,gameMode)
        
    #@param mode is a GameMode object used to filter examined games down to the desired game mode using mode type and subtype (not yet implimented)
    
        #api.get_game_history(keyPlayerId)['games'][0]['fellowPlayers'][0]
    #adds a game id to the list if it is not already listed, returns False if there is already a listing for that id else adds an id and returns true.
    #list is ordered from lowest to highest game id
    def addGame(self,gameId):
        x=0
        while (x < len(self.gameList) and gameId >= self.gameList[x]):   
            if self.gameList[x] == gameId:
                return False            
            x+=1
        self.gameList.insert(x, gameId)
        return True
        
    def getGamesCollected(self):
        collectedGames=0
        for chmpEntry in self.winDict:
            print(self.winDict[chmpEntry])
            collectedGames+=self.winDict[chmpEntry]['totalGames']
        return collectedGames #/ 10
            
        
        