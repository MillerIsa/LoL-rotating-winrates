from __future__ import print_function
import httplib2
import os

from stat_calc import StatCalc

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE=os.path.join(os.path.expanduser('~'), 'Documents\Liclipse Workspace\LeagueWinRates\src\windatasort\client_secret.json')
APPLICATION_NAME = 'LoL Stat Updater'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    spef_cred_dir=os.path.join(credential_dir,'.sheets.googleapis.com-lol-stat-updater.json')
    print('os.path.exists:',os.path.exists(credential_dir))
    print('specific os.path.exists:',os.path.exists(spef_cred_dir))
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    #if not os.path.exists(spef_cred_dir):
        
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-lol-stat-updater.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

class PrintToSheets:
    def __init__(self,stater):
        self.stater=stater
    def sheetUpdate(self):
        """Shows basic usage of the Sheets API.
    
        Creates a Sheets API service object and prints the names and majors of
        students in a sample spreadsheet:
        https://docs.google.com/spreadsheets/d/1bd2aOQLF0BdYtEcoPJzzc226RD_MJcxsP9VqhowhLh8/edit
        """
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
    
        spreadsheetId = '1bd2aOQLF0BdYtEcoPJzzc226RD_MJcxsP9VqhowhLh8'
        #rangeName = 'Class Data!A2:E'
        #updates values in spreadsheet
        statDict=self.stater.calcAll()
        valueArray=[]
        x=0
        for chmpId in statDict:
            chmpEntry=statDict[chmpId]
            chmpEntry2=self.stater.rawWins['champions'][chmpId]
            valueArray.append([chmpEntry['chmpName'],chmpEntry['winRate'],chmpEntry['adjWinRate'],chmpEntry['mirrorMatches'],chmpEntry['popularity'],chmpEntry2['totalGames']])
            x+=1
        z=0
        
        print ('valueArray is:', valueArray)
        
        #make valueArray2, this array will contain correctly organized info on the champion partner pairings
        valueArray2= [None] * (len(self.stater.rawWins) - 1)
        #row 0 contains champion names
        #column 0 reserved for names also
        valueArray2[0]=['']
        chmpOrder=[]
        y=0
        for chmpId in self.stater.rawWins['champions']:
            chmpOrder.append(chmpId)
            print('for chmpId:',chmpId)
            valueArray2[0].append(self.stater.rawWins['champions'][chmpId]['chmpName'])
            y+=1
        m=1
        for chmpId in chmpOrder:
            chmpEntry=self.stater.rawWins['champions'][chmpId]
            
            valueArray2[m]=[self.stater.rawWins['champions'][chmpId]['chmpName']]
            for subChmpId in chmpOrder:
                print('for champId:',chmpId)
                print('partner dictionary is:',self.stater.rawWins['champions'][chmpId]['partners'])
                peerEntry=self.stater.rawWins['champions'][chmpId]['partners'][subChmpId]  
                print('index to attempt is:',m)
                print('valueArray2s length is:',len(valueArray2))
                valueArray2[m].append(peerEntry['winRate'])
            m+=1
            
        
        body=   {
                    "valueInputOption":'RAW',
                    "data": [
                        {
                                "range":'winRates!A2:E151',
                                "values":valueArray,
                                "majorDimension":'ROWS'
                        }
                        ]
                }
        #range is a 150*150 square
        body2=   {
                    "valueInputOption":'RAW',
                    "data": [
                        {
                                "range":'winRates!A1:EK150',
                                #"values":valueArray2,
                                "majorDimension":'ROWS'
                        }
                        ]
                }
        result=service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId,body=body)
        #executest the http request
        result.execute()
        print(result)

