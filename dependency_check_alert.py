#!/usr/bin/env python3

import requests, sys, re, json

slackWebhookUrl = sys.argv[1]
csvFile = sys.argv[2]
projectName = sys.argv[3]
htmlReportUrl = sys.argv[4]
slackAlertEnabled = sys.argv[5]
vulnerabilities = 0

def postToSlack(data):
    res = requests.post(
        slackWebhookUrl, json=data,
        headers={'Content-Type': 'application/json'}
    )

    if res.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (res.status_code, res.text)
        )

def slackData(csvFile) :
    slackData = {}
    blocks = []
    global vulnerabilities
    summary = ""

    with open(csvFile, 'r') as file:
        lines = file.readlines()
        for line in lines:
            vulnerabilities += 1
            cwe = extractCWE(line)
            severity = extractSeverity(line)
            info = extractInfo(cwe, severity, line)

            summary += f"- *{cwe}* (`{severity}`) {info}"

    blocks.append(section(f"*{projectName}* (<{htmlReportUrl}|Detailed report>)"))
    blocks.append(section(f"*Vulnerabilities:* {vulnerabilities}"))
    blocks.append(section(summary))
    slackData['blocks'] = blocks
    # return json.dumps(slackData)
    print(slackData)
    return slackData

def section(text) :
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }

def extractCWE(cweInfoSeverity) :
    return re.search('(CWE\-)\w+', cweInfoSeverity)[0]

def extractSeverity(cweInfoSeverity) :
    severity =  re.search(',(.*)', cweInfoSeverity)[0]
    return severity.replace(',', '')

def extractInfo(cwe, severity, cweInfoSeverity) :
    infoSeverity = cweInfoSeverity.replace(cwe, '')
    info = infoSeverity.replace(severity, '')
    return info.replace(',', '')

def main():
    if slackAlertEnabled == "true" :

        data = slackData(csvFile)

        if vulnerabilities > 0:
            postToSlack(data)

if __name__ == '__main__':
    print("slackWebhookUrl: " + slackWebhookUrl)
    print("csvFile: " + csvFile)
    print("projectName: " + projectName)
    print("htmlReportUrl: " + htmlReportUrl)
    print("slackAlertEnabled: " + slackAlertEnabled)

    main()
