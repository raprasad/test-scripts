"""
Make some GitHub labels
"""
import sys
from collections import namedtuple, OrderedDict
import json
import requests
from msg_util import msgt, msg
from label_info import \
    (ESTIMATE_LABELS,
     ASK2ME_COMPONENTS)
from auth_token import API_TOKEN
import shared_vals


def create_issue(title, **kwargs):
    """create issue content"""
    owner = 'opendp'
    repo = 'opendp-ux'

    default_body = """
- [ ] Implement function
- [ ] Include comments
- [ ] Write tests
        """

    body = kwargs.get('body', default_body)
    subtitle = kwargs.get('subtitle')
    issue_num = kwargs.get('issue_num')

    if subtitle:
        title = f'{title} ({subtitle})'

    create_url = (f'{shared_vals.GH_API_URL}/repos/'
                f'{owner}/{repo}/issues')
    if issue_num:
        create_url = f'{create_url}/{issue_num}'

    params = dict(title=title,
                  body=body,
                  labels=['OpenDP App', 'v0.1'],
                  #milestone=1,
                  #labels=['MVP', 'PSI Core Library'],
                  #milestone=1
                  )

    print('create_url', create_url)

    if issue_num:
        resp = requests.patch(create_url,
                         data=json.dumps(params),
                         headers=shared_vals.GH_HEADERS)
    else:
        resp = requests.post(create_url,
                         data=json.dumps(params),
                         headers=shared_vals.GH_HEADERS)
    msg(resp.status_code)

    if resp.status_code == 200:
        msg('label exists')
        return True

    if resp.status_code == 404:
        msg('Nope!')
        return False

    msg(resp.text)
    return False

def format_description(content):

    pieces = content.split('|')

    desc = []
    if pieces[0]:
        desc.append(f'**Input**: {pieces[0]}')
    if pieces[1]:
        desc.append(f'**Output**: {pieces[1]}')
    if pieces[2]:
        desc.append(f'**Notes**\n{pieces[2]}')
    if pieces[3]:
        desc.append(f'**Logging**\n{pieces[3]}')

    desc.append('**Reference**: https://docs.google.com/spreadsheets/d/1FcxCMqP6z0PUN-5cIEcpxbqlNamuL9oq_73D32ON9E8/edit#gid=0')
    return '\n\n'.join(desc)

if __name__ == '__main__':
    titles = [
        ('Is this a registered Dataverse?', 104),
        ('List Registered Dataverses', 105),
        ('Create Accounrt', 106),
        ('Login', 107),
        ('Update DataverseUser', 108),
        ('Get Terms Of Use', 109),
        ('Set Terms Of Use ', 110),
        ('Get DV Info ', 111),
        ('Start DV Dataset Downloading/Profiling Process', 112),
        ]

    body_info = [\
    'siteUrl|{"isRegisteredDataverse" : true/false}|Check if a RegisteredDataverse object exists for a given siteUrl|Except or tokens, record DV params of non-registered Dataverse connection attempts.',

    '(none)|list of dv objects (url, name, image,etc)|List of allowed dataverses for this OpenDP installation|',

    'firstname, lastname, password, email|OpenDPUser object|This is part of the rest-auth API library|Create/upate already recorded in the database',

    'username, password |OpenDPUser object|This is part of the rest-auth API library|Create/upate already recorded in the database. Do we want failed attempts recorded? Perhaps if the username does not match anything else in the system? Should native logins require 2-factor?',

    'OpenDPUserID, siteUrl, apiGeneralToken|DataverseUser object|Will be called after logging in to OpenDP. Get dv-user info from Dataverse, and either create DataverseUser or update existing DataverseUser|If categorizing logging, this could be part of "Dataverse API calls"',

    'OpenDPUserID|Terms of Use text and ID, if required for this user|The app can call this method to determine whether terms of use are required. If the user has already agreed, the method will return null, or some other indicator to specify that. If the user needs to agree to terms, then the method will return the text of the agreement, and an id of the agreement (so we can keep track of which terms were agreed to, if terms expire and new terms need to be accepted).|',

    'OpenDPUserID, TermsOfUseID|no output accept for success message|Do we need to specify that user accepts or rejects? Or is rejecting the same as not recording an acceptance? Change TOS based on the installation|For audit trail, record a rejection.',

    """dataverseInstallation, datasetPID, generalAPIToken|DataverseFileInfo object, including its uuid. Also includes dataset name, citation info, etc|- Retrieve DV JSON-LD/citation information
- Create DataverseFileInfo object
- Note: this may already exist. If so, also return something about its state. e.g. state of: DepositorInfo, AnalysisPlan|""",

    """(if UI initiates this, DataverseFileInfo uuid)|Profile information: variable names and types|- Not called if file already downloaded + profiled
- Download DV dataset + Run profiler|""",
    ]

    #to_implement.reverse()
    cnt = 1
    for idx in range(0, len(titles)):
        title, issue_num = titles[idx]
        desc = format_description(body_info[idx])
        #desc = desc.strip()
        print(issue_num, title)
        print(desc)
        print('-' * 40)
        #continue
        create_issue(f'{title} (API endpoint #{cnt})',
                     **dict(body=desc,
                            issue_num=issue_num))
        cnt+=1
        #break
