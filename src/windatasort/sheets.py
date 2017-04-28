from __future__ import print_function
import httplib2
import os
import copy

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

def gridToDict(grid):
    """takes a square nested list and converts it into a dictionary.
    The first list and the first element of each subsequent list are used as the dictionaries keys."""
    retDict={}
    x=1
    while x < len(grid):
        y=1
        #if grid[x][0]
        retDict[grid[x][0]]={}
        while (y < len(grid[x])):
            #
            retDict[grid[x][0]][grid[0][y]]=[grid[x][y]]
            y+=1
        x+=1
    return retDict
#for key in pairingGrid.keys():
#            print('key is:',key)
#            if type(pairingGrid[key])==dict:
#                for _key in pairingGrid[key].keys():
#                    print('    key is:',_key)
def recursDictKeys(dict):
    """returns a nested list the keys at each level of the dictionary
     excluding keys that have non-dictionary ancestors.
     each sub list represents the keys in a different tier"""
    for key in pairingGrid.keys():
            print('key is:',key)
            if type(pairingGrid[key])==dict:
                for _key in pairingGrid[key].keys():
                    print('    key is:',_key)
    
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
#Note: it is easier to create one template and copy it than to use format sheets at the moment
class FormatSheets:
    def __init__(self):
        pass
    #ranges format:
    #ranges:['range':{'start_row_index': 0,
    #        'end_row_index': 1,
    #        'start_column_index': 0,
    #        'end_column_index': 150
    #                    }
    #position in list corresponds to sheet id
    #]
    
    #returns an object mimicing the order of the requested ranges
    def parseSheetHeaders(self,spreadsheatId,ranges):
        "returns a list of spreadsheet data from the first row of each sheet in the given spreadsheet"
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        returnCells=[]
        range:{
        'sheet_id': 0,
        'start_row_index': 0,
        'end_row_index': 1,
        'start_column_index': 0,
        'end_column_index': 1
                       }
        x=0
        for range in ranges:
            print('range is:',range)
            range['sheet_id']=x
            #rangeForm={
            #        'range':{
            #           'sheet_id': x,
            #           'start_row_index':range['start_row_index'],
            #           'end_row_index':range['end_row_index'],
            #           'start_column_index':range['start_column_index'],
            #           
            #           'end_column_index': 150
            #                    }
            #           }
            sheetX=service.spreadsheets().get(spreadsheetId=spreadsheatId, ranges=range, includeGridData=None)
            cells={}
            #try:
            print('trying to initiate request to sheets')
            cells=sheetX.execute()
            #except:print('sheet data retrieval failed')
            returnCells.append(cells)
                
            x+=1
        print('returnCells is:',returnCells)    
        return returnCells
    
    def format(self,spreadsheetId='1bFHpt9MKE-KAoc5r6uttbj497ZdZ5kUCqYZ4x6c936E'):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        ranges=[{
            'start_row_index': 0,
            'end_row_index': 1,
            'start_column_index': 0,
            'end_column_index': 6
            }
            ]
        x=0
        while x < 4:
            range={
                'start_row_index': 0,
                'end_row_index': 1,
                'start_column_index': 0,
                'end_column_index': 150
                }
            ranges.append(range)
            x+=1
        #cells=self.parseSheetHeaders(spreadsheatId=spreadsheetId, ranges=ranges)
        #print('cells are:',cells)
        
        #winRateFormat, after adding the range information, is a dictionary that tells google sheets to format the win rates in my preffered style
        winRateFormat={
            "includeSpreadsheetInResponse": False,
               "responseIncludeGridData":False,
               "requests": [{
                        "addConditionalFormatRule":{
                                'index':0,
                                'rule':{
                                        'gradientRule':{
                                                'maxpoint':{
                                                        'color':{
                                                                'blue':0,
                                                                'alpha':1,
                                                                'green':1,
                                                                'red':0
                                                            },
                                                        'type':'Number',
                                                        'value':'1'
                                                    },
                                                'midpoint':{
                                                        'color':{
                                                                'red':1,
                                                                'blue':1,
                                                                'green':1,
                                                                'alpha':1
                                                            },
                                                            'type':'Number',
                                                            'value':'.5'                                                           
                                                    },
                                                'minpoint':{
                                                        'color':{
                                                                'red':1,
                                                                'blue':0,
                                                                'green':0,
                                                                'alpha':1
                                                            },
                                                            'type':'Number',
                                                            'value':'0'                                                            
                                                    },
                                            }
        
                                    }
                            }
                   }]
}
        pairsAndOppsForm={
            
            
            }
        
        
        pairingGridReq=service.spreadsheets().get(spreadsheetId=spreadsheetId,ranges='pairings!A1:EZ150')
        pairingGrid=pairingGridReq.execute()
        #recursDictKeys()
        #print('blank cell type is:',type(pairingGrid[0][150]),'blank cell value is',pairingGrid[0][150])
        #pairingDict=gridToDict()
        
        sheet1Format=copy.deepcopy(winRateFormat)
        sheet1Format['requests'][0]['addConditionalFormatRule']['rule'].update({
                                            'ranges':
                                            [{
                                                'sheet_id': 0,
                                                'start_row_index': 0,
                                                'end_row_index': 1000,
                                                'start_column_index': 1,
                                                'end_column_index': 3
                                            }]
                                                                                       })
        
        pairingsFormat=copy.deepcopy(winRateFormat)
        pairingsFormat['requests'][0]['addConditionalFormatRule']['rule'].update({
                                            'ranges':
                                            [{
                                                'sheet_id': 516289757,
                                                'start_row_index': 0,
                                                'end_row_index': 1000,
                                                'start_column_index': 1,
                                                'end_column_index': 1000
                                            }]
                                                                                       })
        opponentsFormat=copy.deepcopy(winRateFormat)
        opponentsFormat['requests'][0]['addConditionalFormatRule']['rule'].update({
                                            'ranges':
                                            [{
                                                'sheet_id': 204805531,
                                                'start_row_index': 0,
                                                'end_row_index': 1000,
                                                'start_column_index': 1,
                                                'end_column_index': 1000
                                            }]
                                            
                                                                                        })
        
        bodyForm={"includeSpreadsheetInResponse": False,
               "responseIncludeGridData":False,
               "requests": [{
                        "addConditionalFormatRule":{
                                'index':0,
                                'rule':{
                                        'ranges':[{
                                                'sheet_id': 0,
                                                'start_row_index': 0,
                                                'end_row_index': 1000,
                                                'start_column_index': 1,
                                                'end_column_index': 3
                                            }],
                                        'gradientRule':{
                                                'maxpoint':{
                                                        'color':{
                                                                'blue':0,
                                                                'alpha':1,
                                                                'green':1,
                                                                'red':0
                                                            },
                                                        'type':'Number',
                                                        'value':'1'
                                                    },
                                                'midpoint':{
                                                        'color':{
                                                                'red':1,
                                                                'blue':1,
                                                                'green':1,
                                                                'alpha':1
                                                            },
                                                            'type':'Number',
                                                            'value':'.5'                                                           
                                                    },
                                                'minpoint':{
                                                        'color':{
                                                                'red':1,
                                                                'blue':0,
                                                                'green':0,
                                                                'alpha':1
                                                            },
                                                            'type':'Number',
                                                            'value':'0'                                                            
                                                    },
                                            }
        
                                    }
                            }
                   }]
    }
        
        print('sheet1Format range is:',sheet1Format['requests'][0]['addConditionalFormatRule']['rule']['ranges'])
        print('pairingsFormat range is:',pairingsFormat['requests'][0]['addConditionalFormatRule']['rule']['ranges'])
        print('opponentsFormat range is:',opponentsFormat['requests'][0]['addConditionalFormatRule']['rule']['ranges'])
        resultSheet1=service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=sheet1Format)
        resultPairings=service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=pairingsFormat)
        resultOpponents=service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=opponentsFormat)
        
        #resultGet=service.spreadsheets().get(spreadsheetId=spreadsheetId, ranges='A1:A10', includeGridData=True)
        resultSheet1.execute()
        print('executed resultSheet1')
        resultPairings.execute()
        print('executed resultPairings')
        resultOpponents.execute()
        print('executed resultOpponents')
        #print('getResult is:',resultGet.execute())
        #except:print('failed to format sheet')
   
    
class PrintToSheets:
    def __init__(self,stater):
        self.stater=stater
    def sheetUpdate(self,spreadsheetId='1bFHpt9MKE-KAoc5r6uttbj497ZdZ5kUCqYZ4x6c936E'):
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
    
        
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

    def updateTable2(self,spreadsheatId="1bFHpt9MKE-KAoc5r6uttbj497ZdZ5kUCqYZ4x6c936E",subSheetName="winRates",cellRange='A1:F135',filename="redditSeige3-24_28-2017.txt"):
        
        
        request=self.service.spreadsheets().values().get(spreadsheetId=spreadsheatId, range=subSheetName.join([cellRange]), majorDimension=None, dateTimeRenderOption=None, valueRenderOption=None, x__xgafv=None)
        result=request.execute()
        print('result is:',result)
        
        
        filePath='C:\\Users\\Brian-VAIO\\Documents\\isaiAH_laptop\\computerPrograming\\LoLProject\\LoLWinRateOutput\\' + filename
        
        #unpacks the data from google sheets into the table format for reddit
        file = open(filePath,'w+')
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
        

                
         

