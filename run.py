#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import json
import urllib2

import StringIO

#=== Configuration ===
gitaccount = "ACCOUNT"
username = "USERNAME"
password = "PASSWORD"
sourceRepository = "SOURCE_REPO"
destinationRepository = "DEST_REPO"
#=== End of configuration ===

server = "api.github.com"
sourceUrl = "https://%s/repos/%s" % (server, sourceRepository)
destinationUrl = "https://%s/repos/%s" % (server, destinationRepository)

leadingSpace = ""

def incrementOutput():
    global leadingSpace

    leadingSpace = leadingSpace+"   "

def decrementOutput():
    global leadingSpace

    leadingSpace = leadingSpace[3:]

def output(string = ""):
    print "%s%s" % (leadingSpace, string)

def openUrl(method, url, data = None):
    request = urllib2.Request(url, data)

    request.add_header("Authorization", "Basic " + base64.urlsafe_b64encode("%s:%s" % (username, password)))
    request.add_header("Content-Type", "application/json")
    if (method == "PATCH"):
        request.add_header("Accept", "application/vnd.github.loki-preview+json")
    else:
        request.add_header("Accept", "application/json")

    request.get_method = lambda: method
    # pprint (vars(request))

    response = urllib2.urlopen(request)
    data = response.read()

    if data:
        result = json.load(StringIO.StringIO(data))
    else:
        result = []

    return result

def getInformation(url):
    information = []
    maximumPerPage = 100

    if "?" in url:
        realUrl = url+"&page=%s&per_page=%s"
    else:
        realUrl = url+"?page=%s&per_page=%s"

    mustGetInformation = True
    page = 1

    while mustGetInformation:
        pageInformation = openUrl("GET", realUrl % (page, maximumPerPage))

        information.extend(pageInformation)

        if len(pageInformation) == maximumPerPage:
            page += 1
        else:
            mustGetInformation = False

    return information

def setInformation(method, url, data = None):
    openUrl(method, url, data)

def getMilestones(url):
    openMilestones = getInformation("%s/milestones?direction=asc" % url)
    closedMilestones = getInformation("%s/milestones?direction=asc&state=closed" % url)

    return openMilestones+closedMilestones

def cleanUpMilestones(url):
    milestones = getMilestones(url)

    if milestones:
        output(" - Removing existing milestone(s):")

        incrementOutput()

        for milestone in milestones:
            setInformation("DELETE", "%s/milestones/%s" % (url, milestone["number"]))

            output(" - %s" % milestone["title"])

        decrementOutput()
    else:
        output(" - No milestones")

def importMilestones(fromUrl, toUrl):
    milestones = getMilestones(fromUrl)

    if milestones:
        output(" - Importing milestone(s):")

        incrementOutput()

        for milestone in milestones:
            data = json.dumps({
                "title": milestone["title"],
                "state": milestone["state"],
                "description": milestone["description"],
                "due_on": milestone["due_on"]
            })

            setInformation("POST", "%s/milestones" % toUrl, data)

            output(" - %s" % milestone["title"])

        decrementOutput()

def protectBranches(url):

    data = json.dumps({
        "protection": {
            "enabled": True,
            "required_status_checks": {
                "enforcement_level": "off",
                "contexts": []
            }
        }
    })

    output(" - Protecting develop Branch")
    setInformation("PATCH", "%s/branches/develop" % url, data)

    output(" - Protecting master Branch")
    setInformation("PATCH", "%s/branches/master" % url, data)

def updateDefaultBranch(url):

    output(" - Updating default branch to develop")
    repo = openUrl("GET", url)

    data = json.dumps({
        "name": repo['name'],
        "default_branch": "develop"
    })

    setInformation("PATCH", "%s" % url, data)

def main():
    # output("Cleaning up %s:" % destinationRepository)
    # cleanUpMilestones(destinationUrl)

    output()
    output("Importing milestones of %s to %s:" % (sourceRepository, destinationRepository))
    importMilestones(sourceUrl, destinationUrl)

    output()
    output("Protecting branches on %s:" % destinationRepository)
    protectBranches(destinationUrl)

    output()
    output("Update default branch to develop: ")
    updateDefaultBranch(destinationUrl)

if __name__ == '__main__':
    main()
