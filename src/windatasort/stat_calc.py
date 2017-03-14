'''
Created on Feb 25, 2017

@author: Brian-VAIO
'''
#takes aggregated data from win_collector and generates statistics from it
#from windatasort.win_collector import WinCollector
class StatCalc:
    def __init__(self,winCollector):
        self.winCollector=winCollector
        self.rawWins=self.winCollector.winDict
        self.statDict={}#contains dictionary of champion names mapped to dictionaries of various statistics for each champion
        #for chmpId in self.rawWins['champions']:
        #    self.statDict[chmpId]={'winRate':-1,'adjWinRate':-1,'mirrorMatches':0,'popularity':0,'chmpName':self.rawWins['champions'][chmpId]['chmpName'],'partners':{},'opponents':{}}
    #adds winRate data to rawWins['champions']
    def winRate(self):       
        for chmpId in self.rawWins['champions']:
            if self.rawWins['champions'][chmpId]['totalGames'] > 0:
                self.rawWins['champions'][chmpId]['winRate'] = self.rawWins['champions'][chmpId]['wins'] / self.rawWins['champions'][chmpId]['totalGames']
            else:
                self.rawWins['champions'][chmpId]['winRate'] = -1
            #calculates win rates of champion pairings
            for peerId in self.rawWins['champions'][chmpId]['partners']:
                peer=self.rawWins['champions'][chmpId]['partners'][peerId]
                try:peer['winRate']=peer['wins'] / peer['totalGames']
                except ZeroDivisionError:peer['winRate']=-1
            for oppId in self.rawWins['champions'][chmpId]['opponents']:
                peer=self.rawWins['champions'][chmpId]['opponents'][oppId]
                try:peer['winRate']=peer['wins'] / peer['totalGames']
                except ZeroDivisionError:peer['winRate']=-1
    #adds adjusted winRate to rawWins['champions']
    def adjWinRate(self):
        for chmpId in self.rawWins['champions']:
            try: 
                divisor=(self.rawWins['champions'][chmpId]['totalGames'] - 2 * self.rawWins['champions'][chmpId]['mirrorMatches'])
                self.rawWins['champions'][chmpId]['adjWinRate'] = (self.rawWins['champions'][chmpId]['wins'] - self.rawWins['champions'][chmpId]['mirrorMatches']) / (divisor)
            except ZeroDivisionError:self.rawWins['champions'][chmpId]['adjWinRate']=-1
    def popularity(self):
        for chmpId in self.rawWins['champions']:
            if self.rawWins['totalGames'] == 0:
                self.rawWins['champions'][chmpId]['popularity']=-1
            else:
                self.rawWins['champions'][chmpId]['popularity']= self.rawWins['champions'][chmpId]['totalGames'] / self.rawWins['totalGames']
    def calcAll(self):
        self.winRate()
        self.adjWinRate()
        self.popularity()
        return self.rawWins
    def printCalcs(self):
        for chmpId in self.rawWins['champions']:
            print(self.rawWins['champions'][chmpId])
            #for subId in self.rawWins['champions']:
            #    print(self.rawWins['champions'][chmpId]['partners'][subId])
            #    print(self.rawWins['champions'][chmpId]['opponents'][subId])
        
        
    