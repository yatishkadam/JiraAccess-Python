from jira import JIRA
import re
import json
import pprint
import csv

customFeildMapping = {
    'customfield_11730' : 'Team SElection',
    'customfield_11766' : 'Planned Language',
    'customfield_11767' : 'TCO reason For Change',
    'customfield_11769' : 'Platform/Systems Affected',
    'customfield_11184' : 'study team',
    'customfield_11770' : 'Associated ATS Ticket:',
    'components.name'        : 'Study name',
    'components.id'     : 'Component ID',
    'assignee.displayName' : "Assignee",
    'issuelink.issuetype'  : "Issue Type",
    'status.statusCategory.name'  : 'Status Of Issue',
    'status.name'              : 'Status'
}

class JiraReqAllIssues():

    def __init__(self, details):
        self.options = {
            'server': 'https://jira.ert.com/jira'
        }
        self.pp = pprint.PrettyPrinter(indent=4)
        self.headerForCSV = ['Jira ID', 'Issue Status', 'Last Updated', 'Resolution Date', 'Linked Issue',
                             'Team Selection', 'TCO reason For Change', 'Platform/Systems Affected',
                             'Planned Language(is it a Language TCO)', 'Associated with ATS Ticket ?', 'Assignee']
        self.defectParameters = ['Bug', 'Study Defect', 'ERT Product Defect']
        self.enhancementParameter = ['Enhancement']
        self.username = details['userName']
        self.password = details['password']
        self.issueTypesPossibleToFetch = {'TCO-RAF' : 'TCO-RAF'}
        self.jira = JIRA(basic_auth=(self.username, self.password), options=self.options)
        # self.updateAllOpenTCORAFS()
        # self.updateClosedTCORAFS()
        # self.updateTCORAFIssueWithDefect()
        # self.updateOpenTCORAFIssueWithDefect()
        # self.makeTCORAFListWithDefects()
        # self.updateTCORAFIssueWithEnhancements()
        # self.makeTCORAFTackingList()

    def checkIfTCORAF(self, issue):
        if (self.getIssueType(issue) == 'TCO-RAF'):
            return True
        else :
            return False

    def updateAllIssuesForTCORAF(self):
        self.AllIssuesForTCORAF = self.jira.search_issues('type=TCO-RAF', maxResults=50000)

    def getAllIssuesForTCORAF(self):
        try:
            issues =  self.AllIssuesForTCORAF
        except:
            self.updateAllIssuesForTCORAF()
            issues = self.AllIssuesForTCORAF
        finally:
            return issues

    def makeTCORAFListWithDefects(self):
        issues = self.TCORAFIssueWithDefect
        defectTCORAFJiraNumbers = []
        for issue in issues:
            defectTCORAFJiraNumbers.append(issue.key)
        self.defectTCORAFJiraNumbers = defectTCORAFJiraNumbers

    def getIssueFromID(self, ID):
        try:
            return self.jira.issue(ID)
        except:
            print 'something went wrong with ID ->',ID

    def getdescriptionFromIssue(self, issue):
        description = issue.fields.description
        return description

    def getdescriptionFromIssueByID(self, ID):
        issue = self.getIssueFromID(ID)
        return self.getdescriptionFromIssue(issue)

    def updateClosedTCORAFS(self):
        issues = self.getAllIssuesForTCORAF()
        self.closedTCORAFS = []
        for issue in issues:
            if str(self.getStatusCategory(issue)) == 'Done' or str(self.getStatus(issue)) == 'TCO Finished':
                # self.printIssue(issue)
                self.closedTCORAFS.append(issue)

    def getClosedTCORAFS(self):
        return self.closedTCORAFS;

    def updateAllOpenTCORAFS(self):
        issues = self.getAllIssuesForTCORAF()
        self.openTCORAFS = []
        for issue in issues:
            if str(issue.fields.status.name) == 'TCO In Progress' or str(issue.fields.status.name) == 'New' or str(issue.fields.status.name) == 'TCO Drafted':
                # self.printIssue(issue)
                self.openTCORAFS.append(issue)

    def getAllOpenTCORAFS(self):
        return self.openTCORAFS

    def getAllOtherTCORAFS(self):
        issues = self.getAllIssuesForTCORAF()
        self.otherTCORAFS = []
        for issue in issues:
            if str(issue.fields.status.name) != 'TCO In Progress' and str(issue.fields.status.name) != 'New' and str(issue.fields.status.name) != 'TCO Drafted' and str(self.getStatusCategory(issue)) != 'Done' and str(self.getStatus(issue)) != 'TCO Finished':
                self.printIssue(issue)
                self.otherTCORAFS.append(issue)

    def getAllCanceledTCORAFS(self):
        issues = self.getAllIssuesForTCORAF()
        self.canceledTCORAFS = []
        for issue in issues:
            if str(issue.fields.status.statusCategory.name) == 'Canceled':
                self.printIssue(issue)
                self.canceledTCORAFS.append(issue)

    def getNumberOfTCORAF(self):
        print 'Number of TCO-RAF ->', len(self.AllIssuesForTCORAF), '\n'
        return len(self.AllIssuesForTCORAF)

    def getNumberOfAllCanceledTCORAF(self):
        print 'Number of Canceled TCO-RAF ->',len(self.canceledTCORAFS),'\n'
        return len(self.canceledTCORAFS)

    def getNumberOfAllOnHoldTCORAF(self):
        print 'Number of OnHold TCO-RAF ->',len(self.onHoldTCORAFS),'\n'
        return len(self.onHoldTCORAFS)


    def getNumberOfAllOpenTCORAF(self):
        print 'Number of Open TCO-RAF ->',len(self.openTCORAFS),'\n'
        return len(self.openTCORAFS)


    def getNumberOfAllClosedTCORAF(self):
        print 'Number of Closed TCO-RAF ->',len(self.closedTCORAFS),'\n'
        return len(self.closedTCORAFS)

    def getNumberOfAllOtherTCORAF(self):
        print 'Number of Closed TCO-RAF ->',len(self.otherTCORAFS),'\n'
        return len(self.otherTCORAFS)


    def getNumberOfopenTCORAFIssueWithDefect(self):
        print 'Number of open TCO-RAF Issue With Defect ->',len(self.openTCORAFIssueWithDefect),'\n'
        return len(self.openTCORAFIssueWithDefect)

    def getNumberOfAllTCORAFIssueWithDefect(self):
        print 'Number of TCO-RAF Issue With Defect ->',len(self.TCORAFIssueWithDefect),'\n'
        return len(self.TCORAFIssueWithDefect)

    def printIssueUsingID(self,ID):
        issue = self.getIssueFromID(ID)
        self.printIssue(issue)

    def getCustomfield_11730(self, issue):
        # 'Team Selection'
        try:
            return issue.fields.customfield_11730
        except:
            print 'something went wrong with fetching Team selection'
    def getCustomfield_11769(self, issue):
        # 'Platform/Systems Affected'
        affected = []
        try :
            for i in issue.fields.customfield_11769:
                affected.append(str(i.value))
        except:
            pass
        return affected

    def getCustomfield_11766(self, issue):
        # 'Planned Language'
        return issue.fields.customfield_11766

    def getReasonForRAFTCO(self, issue):
        # 'TCO reason For Change'
        reason = []
        try :
            for i in issue.fields.customfield_11767:
                reason.append(str(i.value))
        except :
            pass

        return reason


    def getCustomfield_11770(self, issue):
        # 'Associated ATS Ticket:'
        return issue.fields.customfield_11770

    def getResolutiondate(self,issue):
        # 'resolutiondate'
        return str(issue.fields.resolutiondate).split('T')[0]

    def getAssignee(self, issue):
        # 'Assignee'
        return issue.fields.assignee.displayName

    def getStatusCategory(self, issue):
        # 'statusCategory Of Issue'
        return issue.fields.status.statusCategory.name

    def getStatus(self, issue):
        # 'Status Of Issue'
        return issue.fields.status.name


    def getStatusByID(self, ID):
        # 'Status Of Issue'
        issue = self.getIssueFromID(ID)
        return self.getStatus(issue)

    def getIssueKeyFromIssue(self, issue):
    #     'issue ID'
        return issue.key

    def getLinkedIssues(self, issue):
    #   gets the linked issues
        linkedIssues = []
        try :
            for linkedIssue in issue.fields.issuelinks :
                linkedIssues.append(str(linkedIssue.outwardIssue.fields.issuetype.name))
        except:
            pass
        return linkedIssues

    def getLastUpdateOnIssue(self, issue):
        return str(issue.fields.updated).split('T')[0]

    def getIssueType(self,issue):
        return str(issue.fields.issuetype)

    def getIssueTypeByID(self,ID):
        issue = self.getIssueFromID(ID)
        return str(issue.fields.issuetype)

    def updateTCORAFIssueWithDefect(self):
        issues = self.AllIssuesForTCORAF
        TCORAFIssueWithDefect = []
        for issue in issues:
            if self.checkIfDefect(issue):
                TCORAFIssueWithDefect.append(issue)

        self.TCORAFIssueWithDefect = TCORAFIssueWithDefect

    def updateTCORAFIssueWithEnhancements(self):
        issues = self.AllIssuesForTCORAF
        TCORAFIssueWithEnhancements = []
        for issue in issues:
            if self.checkIfEnhancement(issue):
                TCORAFIssueWithEnhancements.append(issue)
        self.TCORAFIssueWithEnhancements = TCORAFIssueWithEnhancements

    def checkIfDefect(self,issue):
        linkIssueList = self.getLinkedIssues(issue)
        reasonForTCO = self.getReasonForRAFTCO(issue)
        # print 'link issue list->  ',linkIssueList
        # print 'tco reason->  ', reasonForTCO
        if (self.getIssueType(issue) == 'Bug'):
            return True
        for defectParam in self.defectParameters:
            if (defectParam in linkIssueList) or (defectParam in reasonForTCO):
                return True

    def checkIfTCORAFByID(self,ID):
        issue = self.getIssueFromID(ID)
        return self.checkIfTCORAF(issue)


    def checkIfEnhancement(self,issue):
        linkIssueList = self.getLinkedIssues(issue)
        reasonForTCO = self.getReasonForRAFTCO(issue)
        if (self.getIssueType(issue) == 'Enhancement'):
            return True
        for enhancementParam in self.enhancementParameter:
            if (enhancementParam in linkIssueList) or (enhancementParam in reasonForTCO):
                for defectParam in self.defectParameters:
                    if (defectParam in linkIssueList) or (defectParam in reasonForTCO):
                        return False
                return True

    def checkIfEnhancementByID(self,ID):
        issue = self.getIssueFromID(ID)
        linkIssueList = self.getLinkedIssues(issue)
        reasonForTCO = self.getReasonForRAFTCO(issue)
        if (self.getIssueType(issue) == 'Enhancement'):
            return True
        for enhancementParam in self.enhancementParameter:
            if (enhancementParam in linkIssueList) or (enhancementParam in reasonForTCO):
                for defectParam in self.defectParameters:
                    if (defectParam in linkIssueList) or (defectParam in reasonForTCO):
                        return False
                return True

    def makeTCORAFTackingList(self):
        TCORAFIssueWithDefect = self.TCORAFIssueWithDefect
        TCORAFIssueWithEnhancements = self.TCORAFIssueWithEnhancements
        TCORAFTackingList = {}
        for issue in TCORAFIssueWithDefect:
            key = self.getIssueKeyFromIssue(issue)
            TCORAFTackingList[key] = 'Defect'
        for issue in TCORAFIssueWithEnhancements:
            key = self.getIssueKeyFromIssue(issue)
            TCORAFTackingList[key] = 'Enhancement'
        self.TCORAFTackingList = TCORAFTackingList

    def updateOpenTCORAFIssueWithDefect(self):
        issues = self.openTCORAFS
        openTCORAFIssueWithDefect = []
        for issue in issues:
            if self.checkIfDefect(issue):
                openTCORAFIssueWithDefect.append(issue)

        self.openTCORAFIssueWithDefect = openTCORAFIssueWithDefect


    def makeIssueList(self,issue):
        ls = []
        ls.append(self.getIssueKeyFromIssue(issue))
        ls.append(self.getStatus(issue))
        ls.append(self.getLastUpdateOnIssue(issue))
        ls.append(self.getResolutiondate(issue))
        ls.append(self.getLinkedIssues(issue))
        ls.append(self.getCustomfield_11730(issue))
        ls.append(self.getReasonForRAFTCO(issue))
        ls.append(self.getCustomfield_11769(issue))
        ls.append(self.getCustomfield_11766(issue))
        ls.append(self.getCustomfield_11770(issue))
        ls.append(self.getAssignee(issue))
        return ls


    def printIssue(self, issue):
        print self.getCustomfield_11730(issue)
        print self.getCustomfield_11769(issue)
        print self.getCustomfield_11766(issue)
        print self.getReasonForRAFTCO(issue)
        print self.getCustomfield_11770(issue)
        print self.getAssignee(issue)
        print self.getStatusCategory(issue)
        print 'Status ->',self.getStatus(issue)
        print 'Linked issues - >', self.getLinkedIssues(issue)
        print 'resolutiondate - >', self.getResolutiondate(issue)
        print 'Issue Key On jira - >', self.getIssueKeyFromIssue(issue)
        print 'Last updated - >', self.getLastUpdateOnIssue(issue)
        print '_____________________________________________________________'


    def errorMessage(self):
        print "Something went wrong."

    def typesOfIssuesPossibleToBeFetched(self):
        print self.issueTypesPossibleToFetch

    def writeAllOpenTCORAFSToCsvFile(self):
        issues = self.openTCORAFS
        listTowrite = []
        for issue in issues:
            listTowrite.append(self.makeIssueList(issue))
        with open('OpenTCORAF.csv', "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(self.headerForCSV)
            for line in listTowrite:
                writer.writerow(line)

    def writeAllClosedTCORAFSToCsvFile(self):
        issues = self.closedTCORAFS
        listTowrite = []
        for issue in issues:
            listTowrite.append(self.makeIssueList(issue))
        with open('ClosedTCORAF.csv', "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(self.headerForCSV)
            for line in listTowrite:
                writer.writerow(line)

    def writeAllTCORAFSToCsvFile(self):
        issues = self.AllIssuesForTCORAF
        listTowrite = []
        for issue in issues:
            listTowrite.append(self.makeIssueList(issue))
        with open('AllTCORAF.csv', "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(self.headerForCSV)
            for line in listTowrite:
                writer.writerow(line)

    def writeAllTCORAFSWithDefectsToCsvFile(self):
        issues = self.TCORAFIssueWithDefect
        listTowrite = []
        for issue in issues:
            listTowrite.append(self.makeIssueList(issue))
        with open('AllTCORAFWithDefects.csv', "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(self.headerForCSV)
            for line in listTowrite:
                writer.writerow(line)

    def writeOpenTCORAFSWithDefectsToCsvFile(self):
        issues = self.openTCORAFIssueWithDefect
        listTowrite = []
        for issue in issues:
            listTowrite.append(self.makeIssueList(issue))
        with open('AllOpenTCORAFWithDefects.csv', "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(self.headerForCSV)
            for line in listTowrite:
                writer.writerow(line)


    def writeTCORAFSWithEnhancementToCsvFile(self):
        issues = self.TCORAFIssueWithEnhancements
        listTowrite = []
        for issue in issues:
            listTowrite.append(self.makeIssueList(issue))
        with open('AllOpenTCORAFWithEnhancement.csv', "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(self.headerForCSV)
            for line in listTowrite:
                writer.writerow(line)