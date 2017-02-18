'''
Created on Feb 17, 2017

@author: Brian-VAIO
'''
from riot_api import RiotAPI 
import passkey
def main():
    api=initialize()   
    r=api.get_summoner_by_id(62601084,49330575,20378336)    
    print (r)

def initialize():
    api = RiotAPI(passkey.API_KEY)
    CHAMPION_NAMES = api.champ_names_builder()
    print (CHAMPION_NAMES)
    return api
#builds the list of champ ids to names

    
    
    

if __name__ == "__main__":
    main()
    