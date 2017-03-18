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
    
        spreadsheetId = '13xtXU-4gAEzlMb0uvmfzMENsmbmtLRA9kXeeZnPSl4I'
        #rangeName = 'Class Data!A2:E'
        #updates values in spreadsheet
        rawWins=self.stater.calcAll()
        valueArray=[]
        x=0
        for chmpId in rawWins['champions']:
            chmpEntry=rawWins['champions'][chmpId]
            chmpEntry2=self.stater.rawWins['champions'][chmpId]
            valueArray.append([chmpEntry['chmpName'],chmpEntry['winRate'],chmpEntry['adjWinRate'],chmpEntry['mirrorMatches'],chmpEntry['popularity'],chmpEntry2['totalGames']])
            x+=1
        z=0
        
        print ('valueArray is:', valueArray)
        
        #make valueArray2, this array will contain correctly organized info on the champion partner pairings
        numChamps=len(self.stater.rawWins['champions']) + 2
        valueArray2= [None] * (numChamps)
        opponentArray= [None] * (numChamps)
        partNumGamesArr= [None] * (numChamps)
        oppNumGamesArr= [None] * (numChamps)
        print('len(valueArray2 is):',len(valueArray2))
        #row 0 contains champion names
        #column 0 reserved for names also
        valueArray2[0]=['champion']
        opponentArray[0]=['champion']
        partNumGamesArr[0]=['champion']
        oppNumGamesArr[0]=['champion']
        chmpOrder=[]
        y=0
        for chmpId in self.stater.rawWins['champions']:
            chmpOrder.append(chmpId)
            #print('for chmpId:',chmpId)
            chmpName=self.stater.rawWins['champions'][chmpId]['chmpName']
            valueArray2[0].append(chmpName)
            opponentArray[0].append(chmpName)
            partNumGamesArr[0].append(chmpName)
            oppNumGamesArr[0].append(chmpName)
            y+=1
        m=1
        for chmpId in chmpOrder:
            chmpEntry=self.stater.rawWins['champions'][chmpId]
            subChmpName=self.stater.rawWins['champions'][chmpId]['chmpName']
            
            valueArray2[m]=[subChmpName]
            opponentArray[m]=[subChmpName]
            partNumGamesArr[m]=[subChmpName]
            oppNumGamesArr[m]=[subChmpName]
            
            for subChmpId in chmpOrder:
                #print('for champId:',chmpId)
                oppEntry= self.stater.rawWins['champions'][chmpId]['opponents'][subChmpId] 
                oppWinRate=oppEntry['winRate']
                if chmpId >= subChmpId:      
                    allyEntry=self.stater.rawWins['champions'][chmpId]['partners'][subChmpId]  
                else:
                    #swap chmpId and subChmp Id so as to match Hi - low pairing format
                    allyEntry=self.stater.rawWins['champions'][subChmpId]['partners'][chmpId]
                    #following two lines convert data entry to accurately represent opp win rates when (chmpId < subChmpId)
                    oppEntry= self.stater.rawWins['champions'][subChmpId]['opponents'][chmpId]
                    oppWinRate= 1 - oppEntry['winRate']
                    if oppWinRate == 2:oppWinRate=-1
                valueArray2[m].append(allyEntry['winRate'])
                partNumGamesArr[m].append(allyEntry['totalGames'])
                opponentArray[m].append(oppWinRate)
                oppNumGamesArr[m].append(oppEntry['totalGames'])
                
            m+=1
        
        #returns a two dimensional list of number of games for printing    
        #def aggrPartGames():
            
        body=   {
                    "valueInputOption":'RAW',
                    "data": [
                        {
                                "range":'winRates!A2:F151',
                                "values":valueArray,
                                "majorDimension":'ROWS'
                        }
                        ]
                }
        #range is a 150*150 square
        partnerBody=   {
                    "valueInputOption":'RAW',
                    "data": [
                        {
                                "range":'pairings!A1:EK150',
                                "values":valueArray2,
                                "majorDimension":'ROWS'
                        }
                        ]
                }
        partNumGames=   {
                    "valueInputOption":'RAW',
                    "data": [
                        {
                                "range":'pairings sample size!A1:EK150',
                                "values":partNumGamesArr,
                                "majorDimension":'ROWS'
                        }
                        ]
                }
        opponentBody=   {
                    "valueInputOption":'RAW',
                    "data": [
                        {
                                "range":'opponents!A1:EK150',
                                "values":opponentArray,
                                "majorDimension":'ROWS'
                        }
                        ]
                }
        oppNumGames=   {
                    "valueInputOption":'RAW',
                    "data": [
                        {
                                "range":'opponents sample size!A1:EK150',
                                "values":oppNumGamesArr,
                                "majorDimension":'ROWS'
                        }
                        ]
                }
        #test to see if data is valid
        #print('opponentArray is:',opponentArray)
        #print('oppNumGamesArr is:',oppNumGamesArr)
        
            
        print('oppNumGamesArr is:',oppNumGamesArr)
        print('partNumGamesArr is',partNumGamesArr)
        result=service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId,body=body)
        result2=service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId,body=partnerBody)
        result3=service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId,body=opponentBody)
        result4=service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId,body=partNumGames)
        result5=service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId,body=oppNumGames)
        #executest the http requests
        try:
            result.execute()
            result2.execute()
            result3.execute()
            result4.execute()
            result5.execute()
        except:pass
    
#prints from sheets to reddit compatible text mark-up file
class PrintToReddit:
    def __init__(self):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

    def updateTable2(self):
        spreadsheatId="1Sr_xuN1Kv3xexn8uU3hjm3goMZ7GbnDuzUgVWFrDNzA"
        subSheetName="Ascension-3/15/2017"
        cellRange='A1:F135'
        
        request=self.service.spreadsheets().values().get(spreadsheetId=spreadsheatId, range=subSheetName.join([cellRange]), majorDimension=None, dateTimeRenderOption=None, valueRenderOption=None, x__xgafv=None)
        result=request.execute()
        print('result is:',result)
        
        
        filePath='C:\\Users\\Brian-VAIO\\Documents\\isaiAH_laptop\\computerPrograming\\LoLProject\\LoLWinRateOutput\\redditAscension3-14-2017.txt'
        
        #unpacks the data from google sheets into the table format for reddit
        file = open(filePath,'w')
        file.write('|'.join(result['values'][0]))
        z=1
        alignmentStr=':--'
        while z < len(result['values'][0]):
            z+=1
            alignmentStr='|'.join([alignmentStr,':--'])
        file.write(alignmentStr.join(['\n','\n']))
        y=1
        while y < len(result['values']):
            rowEntry=result['values'][y]
            file.write('|'.join(rowEntry) + '\n')
            y+=1
        file.close()
        

                
         

