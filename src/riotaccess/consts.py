'''
Created on Feb 17, 2017

@author: Brian-VAIO
'''

URL = {
    'base':'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
    'summoner_by_name':'v{version}/summoner/by-name/{names}',
    'summoner_by_id':'v{version}/summoner/{summonerIds}',
    'game_history':'v{version}/game/by-summoner/{summonerId}/recent',
    'match':'v{version}/match/{matchId}',
    'static_base':'https://{proxy}.api.pvp.net/api/lol/static-data/{region}/{url}',
    'champion_list':'v{version}/champion'
    
    }
API_VERSIONS = {
    'summoner':'1.4',
    'game':'1.3',
    'match':'2.2',
    'champion':'1.2'
    }
REGIONS = {
    'north_america':'na',
    'europe_nordic_and_east':'eune',
    'europe_west':'euw'
    }
#CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO, SIEGE
#    Game sub-type. (Legal values: NONE, NORMAL, BOT, RANKED_SOLO_5x5, RANKED_PREMADE_3x3, RANKED_PREMADE_5x5, ODIN_UNRANKED, RANKED_TEAM_3x3, RANKED_TEAM_5x5, NORMAL_3x3, BOT_3x3, CAP_5x5, ARAM_UNRANKED_5x5, ONEFORALL_5x5, FIRSTBLOOD_1x1, FIRSTBLOOD_2x2, SR_6x6, URF, URF_BOT, NIGHTMARE_BOT, ASCENSION, HEXAKILL, KING_PORO, COUNTER_PICK, BILGEWATER, SIEGE, RANKED_FLEX_SR, RANKED_FLEX_TT)
#first value is game type, second is the subtype
class GameMode:
    #@param strings representing the gameMode and subType as outlined by the riot API
    def __init__(self,gameMode,subType):
        self.gameMode=gameMode
        self.subType=subType

GAME_MODES = {
    'aram':GameMode('ARAM','ARAM_UNRANKED_5x5'),
    'ranked5v5':GameMode('CLASSIC','RANKED_SOLO_5x5'),
    'normals':GameMode('CLASSIC','NORMAL'),
    'ascension':GameMode('ASCENSION','ASCENSION'),
    'one_for_all':GameMode('ONEFORALL','ONEFORALL_5x5'),
    'poro_king':GameMode('KINGPORO','KING_PORO'),
    'blood_moon':GameMode('ASSASSINATE','ASSASSINATE'),
    'urf':GameMode('URF','URF'),
    'nexus_seige':GameMode('SIEGE','SIEGE'),
    'definitely_not_dominion':GameMode('ODIN','ODIN_UNRANKED'),
    'snowdown_showdown':GameMode('FIRSTBLOOD','FIRSTBLOOD_1x1'),
    'arsr':GameMode('ARSR','ARSR'),
    #null mode should be used when no mode should be examined
    'null_mode':GameMode('NULL','NULL'),
    'doom_bots':GameMode('DOOMBOTSTEEMO','NIGHTMARE_BOT')   
    }

MAPS = {
    12:'Howling_Abyss',
    11:'Summoners_Rift',
    10:'Twisted_Treeline',
    8:'Ascension_Map'
    }
RESPONSE_CODES = {
    400:'Bad request',
    401:'Unauthorized',
    403:'Forbidden',
    404:'Game data not found',
    429:'Rate limit exceeded',
    500:'Internal server error',
    503:'Service unavailable'
    }

