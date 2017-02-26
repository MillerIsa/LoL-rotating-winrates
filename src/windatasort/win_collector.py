'''
Created on Feb 20, 2017

@author: Brian-VAIO
'''
from riotaccess.riot_api import RiotAPI 
import consts
from builtins import int
from windatasort import stat_calc
class WinCollector:
    'uses riot_api instance object to initialize the winDict with correct champion Ids and names. Also initializes the game statistics to zero.'
    #needs a RiotAPI object to perform data collection
    def __init__(self,riot_api):
        self.api=riot_api
        chmpNames=self.api.champ_names_builder()
        self.winDict={} 
        self.lists={'summoners':[],'games':[]}
        self.statedGames=0
        #self.summList=[]list of all summoners that game history was pulled from
        #self.gameList=[] list of games collected ordered from lowest game Id to highest game Id
        self.winDict['totalGames']=0
        self.winDict['champions']={}
        for chmpId in chmpNames:  
            chmpName=chmpNames[chmpId]
            self.winDict['champions'][chmpId]={'chmpName':chmpName,'wins':0,'losses':0,'totalGames':0,'mirrorMatches':0}
        self.stater=stat_calc.StatCalc(self)
    #returns a list of summIds        
    def examineGameHistory(self,keyPlayerId,mode):
        keyPlayerId=keyPlayerId
        summIdList=[]
        history=self.api.get_game_history(keyPlayerId)
        if type(history) == dict:
            try:
                games=history['games']
            except KeyError:
                print('No such key. Available keys are',history.keys())
                return summIdList
            for game in games:
                #executes suite only if the game is of the correct mode and not already counted
                if game['gameMode'] == mode.gameMode and game['subType'] == mode.subType and self.addId(game['gameId'],'games'): 
                    self.winDict['totalGames']+=1            
                    #records win stats of the key player
                    chmpId=game['championId']
                    chmpEntry=self.winDict['champions'][chmpId]
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
                        #log Ids of the players if not in the master list already
                        if self.addId(player['summonerId'],'summoners'):
                            summIdList.append(player['summonerId'])
                        #logs win/losses of champions
                        chmpId=player['championId']
                        chmpEntry=self.winDict['champions'][chmpId]
                        myTeamId=player['teamId']
                        if (myTeamId == keyTeamId) == (game['stats']['win']):
                            chmpEntry['wins']+=1
                        else:
                            chmpEntry['losses']+=1
                        chmpEntry['totalGames']+=1
                    #incrementing to find mirror match ups
                        try:
                            mirrorDict[chmpId]+=1
                        except KeyError:
                            mirrorDict[chmpId]=1   
                    for chmpId in mirrorDict:
                        if mirrorDict[chmpId] % 2 == 0:
                            self.winDict['champions'][chmpId]['mirrorMatches']+=1
        else: print(history)
        return summIdList
            
    #@param rootPlayer is the summoner id of the player to start spidering from
    #@param string representing game mode 
    #!!!!!!!IMPLIMENT RATE LIMITITNG BEFORE RUNNIG PROGRAM AGAIN. This method will exceed rate limit every time otherwise!!!!!!     
    def spider(self,rootPlayer,gameMode):
        'pulls game data for statistical analysis and stores the portions of the data in winDict' 
        #preforms statistic calculations when the number of games aggregated exceeds the number of recorded games by the indicated amount
        if len(self.lists['games']) - self.statedGames > 100:
            print('games collected:',self.winDict)
            print('stats are:')
            self.stater.calcAll()
            print(self.stater.statDict)
            self.statedGames=len(self.lists['games'])
        #pulls the win/loss data for an individual's game history
        summsToPull=self.examineGameHistory(rootPlayer,gameMode)
        print('summs to spider over',summsToPull)
        x=0
        for summ in summsToPull:
            x+=1
        print('summsFound:',x)
        for summId in summsToPull:
            self.spider(summId,gameMode)
        
    #@param mode is a GameMode object used to filter examined games down to the desired game mode using mode type and subtype (not yet implimented)
    
        #api.get_game_history(keyPlayerId)['games'][0]['fellowPlayers'][0]
    #adds a game id to the list if it is not already listed, returns False if there is already a listing for that id else adds an id and returns true.
    #list is ordered from lowest to highest game id
    def addId(self,newId,listKey):
        x=0
        while (x < len(self.lists[listKey]) and newId >= self.lists[listKey][x]):   
            if self.lists[listKey][x] == newId:
                #print('!!id in list!!')
                return False            
            x+=1
        #print('%%%%%id not in list{[[[[[',self.lists[listKey])
        self.lists[listKey].insert(x, newId)
        return True
    #deprecated - use self.totalGames instead
    def getGamesCollected(self):
        collectedGames=0
        for chmpEntry in self.winDic['champions']:
            print(self.winDict['champions'][chmpEntry])
            collectedGames+=self.winDict['champions'][chmpEntry]['totalGames']
        return collectedGames #/ 10
            
        
        