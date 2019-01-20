
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import JiraReqBaseClass
import inspect
from jira import JIRA
import re
import time
import pickle

userName = ''
password = ''
options = {
            'server': ''
        }

details = {
    'userName' : userName,
    'password' : password
}

# name of the sheet
goodgleSheetName = 'Post Release Status'

sheetName = 'All TCOs'
DESCRIPTION_COLUMN_ID_LETTER = 'Q'
JIRA_ID_COLUMN_NAME = 'RAF JIRA #'
JIRA_ID_COLUMN_LETTER = 'P'
OTHER_JIRA_IDS_COLUMN_NAME = 'Other Jira #s'
STATUS_COLUMN_ID_LETTER = 'K'
STATUS_COLUMN_NAME = 'Status'
HANDLED_BY_COLUMN_NAME = 'Who Will Handle?'
OTHER_JIRA_NUMBER_ID_LETTER = 'R'
TRACKING_COLUMN_NAME = 'Tracking Bucket'
TRACKING_COLUMN_LETTER_ID = 'J'


PERMITED_HANDLERS_LIST = ['PR-Kevin', 'PR-Deepthi']


# object which holds the mapping to the status feild.
mappedStatus = {
    'New'               : 'Needs Assignment',
    'Canceled'          : 'Canceled',
    'TCO Drafted'       : 'Pending RAF',
    'TCO In Progress'   : 'Ongoing Dev',
    'TCO Finished'      :  'Released',
    'Closed'            :  'Released',
    'Resolved'          :  'Released',
    'In Progress'       :  'Ongoing Dev'
}



# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
allWorksheets = client.open(goodgleSheetName)
sheet = allWorksheets.worksheet(sheetName)


# Extract and print all of the values
list_of_hashes = sheet.get_all_records()

# initialising jira interface
jiraUserInterface = JiraReqBaseClass.JiraReqAllIssues(details)


# function to get the mapped status from the mappedStatus object
# status- string - the current status of the issue.
def getMappedStatus(status):
    return mappedStatus[status]


IDSNotFetched =[]
def updateDefectOrEnhancement(rowValue, jiraId, OjiraId):
    try:
        issue = jiraUserInterface.getIssueFromID(jiraId)
        if jiraUserInterface.checkIfDefect(issue):
            # print 'issue is a defect -> ',jiraId
            row = sheet.find(OjiraId)
            if row :
                rowNum = row.row
                toUpdate = TRACKING_COLUMN_LETTER_ID + str(rowNum)
                previousVal = rowValue[TRACKING_COLUMN_NAME]
                sheet.update_acell(toUpdate, 'Defect')
                # print 'updated issue - >',rowNum
                print 'jira ID - >',jiraId,'        previous value - >',previousVal,'             Update value -> Defect'
        if jiraUserInterface.checkIfEnhancement(issue):
            # print 'issue is a enhancement-> ', jiraId
            row = sheet.find(OjiraId)
            if row:
                rowNum = row.row
                toUpdate = TRACKING_COLUMN_LETTER_ID + str(rowNum)
                previousVal = rowValue[TRACKING_COLUMN_NAME]
                sheet.update_acell(toUpdate, 'Enhancement')
                # print 'updated issue - >', rowNum
                print 'jira ID - >',jiraId,'        previous value - >',previousVal, '             Update value -> Enhancement'
    except:
        print IDSNotFetched.append(jiraId)



# this function update the description feild in the row.
# jiraId - string - the jira ID
# OjiraID - string - the ID which was orignally entered in the cell of the google sheet. used to search for the feild.

descriptUpdatedFailed = []
def updateDescriptionInSheet(jiraId, OjiraId):
    time.sleep(0.2)
    try:
        issue = jiraUserInterface.getIssueFromID(jiraId)
        if jiraUserInterface.checkIfTCORAF(issue):
            description = jiraUserInterface.getdescriptionFromIssueByID(jiraId).encode('utf8')
            s = description.replace('\r', '')
            description = re.sub(r'\n\s*\n', '', s)
            description = ' '.join(description.split('\n'))
            row = sheet.find(OjiraId)
            if row:
                rowNum = row.row
                cellToUpdate = DESCRIPTION_COLUMN_ID_LETTER + str(rowNum)
                sheet.update_acell(cellToUpdate, description)
                print 'Updated for JIRAID ->           ', jiraId
    except:
        descriptUpdatedFailed.append(jiraId)


# this function update the description feild in the row.
# rowValue - obj class - hold the whole row from the worksheet.
# jiraId - string - the jira ID
# OjiraID - string - the ID which was orignally entered in the cell of the google sheet. used to search for the feild.

statusUpdateFaildForID = []
def updateStatusOFIssueInSheet(rowValue, jiraId, OjiraId):
    try:
        status = str(jiraUserInterface.getStatusByID(jiraId))
        row = sheet.find(OjiraId)
        handledBy = rowValue[HANDLED_BY_COLUMN_NAME]
        # print handledBy
        if handledBy in PERMITED_HANDLERS_LIST:
            pass
        else :
            issue = jiraUserInterface.getIssueFromID(jiraId)
            if jiraUserInterface.checkIfTCORAF(issue):
                if row:
                    rowNum = row.row
                    previousVal = rowValue[STATUS_COLUMN_NAME]
                    cellToUpdate = STATUS_COLUMN_ID_LETTER + str(rowNum)
                    mapStatus = getMappedStatus(status)
                    sheet.update_acell(cellToUpdate, mapStatus)
                    print 'Updated for JIRAID ->           ',jiraId, '                   previous value, new value ->',previousVal,'   ',mapStatus
            else :
                print 'JiraID -> NOT a TCO , status not updated             -> ',jiraId
    except:
        statusUpdateFaildForID.append(jiraId)


# this function update the description feild in the row.
# rowValue - obj class - hold the whole row from the worksheet.
# jiraId - string - the jira ID
# OjiraID - string - the ID which was orignally entered in the cell of the google sheet. used to search for the feild.

def updateTCONumberFeild(rowValue ,OjiraId, jiraDefectmap):
    row = sheet.find(OjiraId)
    if row:
        jiraIDs = ''
        otherIDs = rowValue[OTHER_JIRA_IDS_COLUMN_NAME]
        rowNum = row.row
        jiraCellToUpdate = JIRA_ID_COLUMN_LETTER + str(rowNum)
        time.sleep(0.2)
        otherIDCellToUpdate = OTHER_JIRA_NUMBER_ID_LETTER + str(rowNum)
        for i, v in jiraDefectmap.iteritems():
            if v:
                jiraIDs =i+ '\n'+ jiraIDs
            else :
                otherIDs = otherIDs + '\n' + i
        jiraIDs = '\n'.join(jiraIDs).strip('\n')
        sheet.update_acell(jiraCellToUpdate, jiraIDs)
        time.sleep(0.2)
        otherIDs = '\n'.join(otherIDs).strip('\n')
        sheet.update_acell(otherIDCellToUpdate, otherIDs)


TCOIDSNotMoved = []
def updateFeildsOnSheet():
    cannotFetchId = []
    for rowValue in list_of_hashes:
        jiraDefectmap ={}
        OjiraId = rowValue[JIRA_ID_COLUMN_NAME]
        if (OjiraId != '' or OjiraId):
            time.sleep(.5)
            dID =OjiraId
            dID = ' '.join(dID.splitlines())
            listOfJiraID = re.split(', |\n| | \n|; |,\n |;\n',dID)
            for i in listOfJiraID:
                # making the issue id
                jiraId = i
                jiraId = jiraId.strip()
                jiraId = jiraId.replace(" ", "")
                try :
                    if (i != ''):
                        jiraDefectmap[i] = jiraUserInterface.checkIfTCORAFByID(jiraId)
                        updateDefectOrEnhancement(rowValue, jiraId, OjiraId)
                        updateStatusOFIssueInSheet(rowValue, jiraId, OjiraId)
                        updateDescriptionInSheet(jiraId, OjiraId)
                        print 'udpate done for ID - >              ',jiraId
                except:
                    cannotFetchId.append(str(jiraId))
                    print 'cannot fetch for jiraID - >             ', jiraId
            try:
                if (jiraDefectmap):
                    updateTCONumberFeild(rowValue, OjiraId, jiraDefectmap)
                    print jiraDefectmap
            except:
                TCOIDSNotMoved.append(OjiraId)


def writeToFile():
    with open('ErrorNames.txt', "w+") as file:
        file.write('\nTCO which were not moved\n')
        for i in TCOIDSNotMoved:
            file.write(i)
            file.write('\n')
        file.write('\n\n\nStatus not updated\n')
        for i in statusUpdateFaildForID:
            file.write(i)
            file.write('\n')

        file.write('\n\n\ndescription not updated\n')
        for i in descriptUpdatedFailed:
            file.write(i)
            file.write('\n')


updateFeildsOnSheet()
writeToFile()
