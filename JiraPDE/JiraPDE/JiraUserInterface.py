import JiraReqBaseClass

userName = ''
password = ''


details = {
    'userName' : userName,
    'password' : password
}


jiraUserInterface = JiraReqBaseClass.JiraReqAllIssues(details)

# jiraUserInterface.printIssueUsingID('ONEECOA-88150')
# issue = jiraUserInterface.getIssueFromID('ONEECOA-88150')
# print jiraUserInterface.getAllIssuesOfType('TCO-F')

# jiraUserInterface.getClosedTCORAFS()
# jiraUserInterface.getAllOpenTCORAFS()
# jiraUserInterface.getAllCanceledTCORAFS()
# jiraUserInterface.getAllOnHoldTCORAFS()
#
# jiraUserInterface.getAllOtherTCORAFS()
#
#
# jiraUserInterface.getNumberOfTCORAF()
# jiraUserInterface.getNumberOfAllOnHoldTCORAF()
# jiraUserInterface.getNumberOfAllCanceledTCORAF()
# jiraUserInterface.getNumberOfAllClosedTCORAF()
# jiraUserInterface.getNumberOfAllOpenTCORAF()
# jiraUserInterface.getNumberOfAllOtherTCORAF()
# jiraUserInterface.getNumberOfopenTCORAFIssueWithDefect()
# jiraUserInterface.getNumberOfAllTCORAFIssueWithDefect()

# jiraUserInterface.writeAllOpenTCORAFSToCsvFile()
# jiraUserInterface.writeAllClosedTCORAFSToCsvFile()
# jiraUserInterface.writeAllTCORAFSToCsvFile()
# jiraUserInterface.writeOpenTCORAFSWithDefectsToCsvFile()
# jiraUserInterface.writeAllTCORAFSWithDefectsToCsvFile()

jiraUserInterface.writeTCORAFSWithEnhancementToCsvFile()