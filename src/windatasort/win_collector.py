'''
Created on Feb 20, 2017

@author: Brian-VAIO
'''
from riotaccess.riot_api import RiotAPI 
from riotaccess import consts
from builtins import int
from windatasort import stat_calc
from windatasort import sheets

import time
import copy

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
            #the win rate of a particular pair is equal to the sum of the two pair entries. Ex: win rate of ahri,annie + annie,ahri = win rate of the annie ahri pairing
            #entries where chmpId and subChmpId are the same will have double the values
            self.winDict['champions'][chmpId]={'chmpName':chmpName,'wins':0,'losses':0,'totalGames':0,'mirrorMatches':0,'winRate':-1,'adjWinRate':-1,'popularity':0,'partners':{},'opponents':{}}
        self.pairDict={}
        for chmpId in self.winDict['champions']:
            for subChmpId in self.winDict['champions']:
                subChmpName=chmpNames[subChmpId]
                #mirror matches are not yet implemented for pairings
                self.winDict['champions'][chmpId]['partners'][subChmpId]={'partnerName':subChmpName,'wins':0,'losses':0,'totalGames':0,'mirrorMatches':0,'winRate':-1}
                self.winDict['champions'][chmpId]['opponents'][subChmpId]={'opponentName':subChmpName,'wins':0,'losses':0,'totalGames':0,'mirrorMatches':0,'winRate':-1}
        self.stater=stat_calc.StatCalc(self)
        self.printer=sheets.PrintToSheets(self.stater)
    #returns a list of summIds        
    def examineGameHistory(self,keyPlayerId,mode):
        keyPlayerId=keyPlayerId
        summIdList=[]
        #print('player to retrieve history on:',keyPlayerId)
        history=self.api.get_game_history(keyPlayerId)
        if type(history) == dict:
            try:
                games=history['games']
            except KeyError:
                print('No such key. Available keys are',history.keys())
                return summIdList
            for game in games:
                #executes suite only if the game is of the correct mode and not already counted
                #print('game found:',game)
                if game['gameMode'] == mode.gameMode and game['subType'] == mode.subType and self.addId2(game['gameId'],'games'): 
                    keyTeamId=game['teamId'] 
                    self.winDict['totalGames']+=1            
                    #records win stats of the key player
                    mChmpId=game['championId']
                    chmpEntry=self.winDict['champions'][mChmpId]
                    if game['stats']['win'] == True:
                        chmpEntry['wins']+=1
                    else:
                        chmpEntry['losses']+=1
                    chmpEntry['totalGames']+=1
                    #records pairing data. logs data with the higher Id on the encapsulating level
                    #game represents the key champion in the list of partners
                    partners=copy.copy(game['fellowPlayers'])
                    partners.append(game)
                    #print('champions in game:',partners)
                    self.partner(partners, game)
                    
                #dictionary to test for mirror matches
                    mirrorDict={}
                    mirrorDict[mChmpId]=1
                
                        
                    for player in game['fellowPlayers']:
                        #log Ids of the players if not in the master list already
                        if self.addId2(player['summonerId'],'summoners'):
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
                        #logs chmp pairing data
                        
                        
                            
                    for chmpId in mirrorDict:
                        if mirrorDict[chmpId] % 2 == 0:
                            self.winDict['champions'][chmpId]['mirrorMatches']+=1
        else: 
            print('history is:',history)
        return summIdList
    #logs all pair win/losses in the given list of partners for the game given
    #@ param "partners" each partner must be a dictionary with the following keys: 'teamId','championId'
    #at all times win losses for a champion pair are stored in the High Id, Low Id dictionary entry. But all mirror pairings are double counted, win rate calculation should be unaffected by this.
    # for opponent pairings it is accurately stored in both pairs
    def partner(self,partners,game):
        keyTeamId=game['teamId']
        for player in partners:
            myTeamId=player['teamId']
            chmpId=player['championId']
            for pairPlayer in partners:
                pairId=pairPlayer['championId']
                if chmpId >= pairId:
                    allyOrNot=self.winDict['champions'][chmpId]['opponents'][pairId]
                    #if true, then they are on the same team
                    if (pairPlayer['teamId'] == myTeamId):
                        allyOrNot=self.winDict['champions'][chmpId]['partners'][pairId]
                    if (pairPlayer['teamId'] == keyTeamId) == game['stats']['win']:
                        allyOrNot['wins']+=1
                    else:
                        allyOrNot['losses']+=1
                    allyOrNot['totalGames']+=1    
                    
                                
    #@param rootPlayer is the summoner id of the player to start spidering from
    #@param string representing game mode    
    def spider(self,rootPlayer,gameMode):
        'pulls game data for statistical analysis and stores the portions of the data in winDict' 
      
        summsToPull=[rootPlayer]
        #pulls the win/loss data for an individual's game history
        for summ in self.examineGameHistory(rootPlayer,gameMode):
            summsToPull.append(summ)
        x=0
        for summ in summsToPull:
            x+=1
            #print('summ in list:',summ)
        #print('summsFound:',x)
        i=0
        while (i < len(summsToPull)):
            summ=summsToPull[i]
            newSumms=self.examineGameHistory(summ,gameMode)
            i+=1
            s=0
            while (s < len(newSumms)):
                summsToPull.append(newSumms[s])
                s+=1
                #time.sleep(.001)
                #print('summsToPull is:',summsToPull)
            #performs statistic calculations when the number of games aggregated exceeds the number of recorded games by the indicated amount
            if len(self.lists['games']) - self.statedGames > 500:
                print('total games collected:',self.winDict['totalGames'])
                self.stater.calcAll()
                self.printer.sheetUpdate()
                #self.stater.printCalcs()
                self.statedGames=len(self.lists['games'])
        #for summId in summsToPull:
            #self.spider(summId,gameMode)
            
        
    #@param mode is a GameMode object used to filter examined games down to the desired game mode using mode type and subtype (not yet implimented)
    #@param mode is the desired mode to pull games on
    #@return game Id of the new game to spider from
    def seedSumm(self,rootSumm,mode):
        summsToCheck=[rootSumm]
        y=0
        while y < len(summsToCheck):
            history=self.api.get_game_history(summsToCheck[y])
            for game in history['games']:
                print('game is:',game)
                if game['gameMode'] == mode.gameMode and game['subType'] == mode.subType and self.addId2(game['gameId'], 'games', insertOrNot=False):
                    return summsToCheck[y]
                else:
                    if 'fellowPlayers' in game.keys(): 
                        for player in game['fellowPlayers']:
                            summsToCheck.append(player['summonerId'])
            y+=1
        
            
        
        
        
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
    #add an entry to the list if it is not already in there. Split the list in half until the correct index is located
    def addId2(self,newId,listKey,insertOrNot=True):
        reList=self.lists[listKey]
       
        leftInd=-1
        rightInd=len(reList)
        #never test the right or left indexes. They are guaranteed to not be the target value
        #while sublist length is at least 2
        y=0
        while(rightInd - leftInd > 2):
            y+=1
            testInd=(rightInd + leftInd + 1) // 2 
            #print('test index is:',testInd)
            if reList[testInd - 1] < newId < reList[testInd]:
                if insertOrNot:reList.insert(testInd,newId)
                #print('number of index checks:',y)
                #print('for list length of:',len(reList))
                return True
            if reList[testInd] == newId:
                #print('number of index checks:',y)
                #print('for list length of:',len(reList))
                return False
            if newId < reList[testInd]:
                rightInd=testInd# - 1
            else:
                leftInd=testInd# + 1
        x=leftInd + 1
        while (x < rightInd and newId >= reList[x]):
            y+=1
            if reList[x] == newId:
                #print('number of index checks:',y)
                #print('for list length of:',len(reList))
                return False
            x+=1
        if insertOrNot:reList.insert(x,newId)
        return True
    #finds a game to start spidering from   
   
            
            
    #deprecated - use "self.winDic['totalGames']" instead
    def getGamesCollected(self):
        collectedGames=0
        for chmpEntry in self.winDict['champions']:
            print('do not call getGamesCollected()',self.winDict['champions'][chmpEntry])
            collectedGames+=self.winDict['champions'][chmpEntry]['totalGames']
        return collectedGames #/ 10
            
        
        