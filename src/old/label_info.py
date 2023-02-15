"""Labels for adding to GitHub"""
import json
from collections import namedtuple, OrderedDict

import requests

from auth_token import API_TOKEN
import shared_vals

def msg(m): print(m)
def dashes(cnt=40): msg('-' * cnt)
def msgt(m): dashes(); msg(m); dashes()


GH_API_URL = 'https://api.github.com'
GH_HEADERS = OrderedDict(
                    {'Authorization': 'token %s' % API_TOKEN,
                     'Accept': 'application/vnd.github.the-key-preview+json'})


class LabelInfo:
    """Label information!"""
    def __init__(self, name, **kwargs):
        assert name and isinstance(name, str), \
            '"name" must be a non-empty string!'

        self.name = name
        self.description = kwargs.get('desc')
        self.color = kwargs.get('color')

        #self.name_short = self.name.split()[0]

    def as_dict(self, as_string=False):
        """For POST to GitHub"""
        info = dict(name=self.name)

        if self.description: info['description'] = self.description
        if self.color: info['color'] = self.color

        if as_string:
            return json.dumps(info)

        return info


    def does_exist(self, owner, repo):
        """Does this label exist already?"""
        check_url = (f'{shared_vals.GH_API_URL}/repos/'
                     f'{owner}/{repo}/labels/{self.name}')
        msgt('Exists? %s' % check_url)

        resp = requests.get(check_url, headers=GH_HEADERS)
        if resp.status_code == 200:
            msg('label exists')
            return True

        if resp.status_code == 404:
            msg('Nope!')
            return False

        msg(resp.text)
        return False


    def delete_label(self, owner, repo):
        """Delete label!"""
        delete_url = (f'{shared_vals.GH_API_URL}/repos/'
                      f'{owner}/{repo}/labels/{self.name}')

        msgt(f'Delete: {delete_url}')

        resp = requests.delete(delete_url,
                               headers=GH_HEADERS)

        if resp.status_code == 204:
            msg('label deleted!')
            return True

        msg('DELETE FAILED!')
        msg(resp.text)
        msg(resp.status_code)
        return False

    @staticmethod
    def add_label_to_issue(owner, repo, issue_number, labels_list):
        """Add label!"""
        add_url = (f'{shared_vals.GH_API_URL}/repos/'
                   f'{owner}/{repo}/issues/{issue_number}/labels')

        label_data = json.dumps(dict(labels=labels_list))

        resp = requests.post(add_url,
                             headers=GH_HEADERS,
                             data=label_data)

        if resp.status_code == 200:
            msg('label added to issue!')
            return True

        msg('label add failed')
        msg(resp.text)
        msg(resp.status_code)
        return False


    def add_label(self, owner, repo):
        """Add label!"""
        create_url = (f'{shared_vals.GH_API_URL}/repos/'
                      f'{owner}/{repo}/labels')

        print(self.as_dict(as_string=True))

        resp = requests.post(create_url,
                             headers=GH_HEADERS,
                             data=self.as_dict(as_string=True))

        if resp.status_code == 201:
            msg('label created!')
            return True

        msg('created failed')
        msg(resp.text)
        msg(resp.status_code)
        return False


PRIORITY_LABELS = [LabelInfo('Priority 1 - Small :zap:',
                             desc='Used for estimation',
                             color='FFAC33'),
                   LabelInfo('Priority 2 - Medium :partly_sunny:',
                             desc='Used for estimation',
                             color='FFEF33'),
                   LabelInfo('Priority 3 - Low :sunflower:',
                             desc='Used for estimation',
                             color='33FFF2'),]

ESTIMATE_LABELS = [LabelInfo('Effort 1 - Small :coffee:',
                             desc='Used for estimation',
                             color='42c5f5'),
                   LabelInfo('Effort 2 - Medium :cookie:',
                             desc='Used for estimation',
                             color='9cf542'),
                   LabelInfo('Effort 3 - Large :cake:',
                             desc='Used for estimation',
                             color='ebc034'),
                   LabelInfo('Effort 4 - Too Large :oncoming_bus:',
                             desc='Used for estimation',
                             color='eb7134'),]

ASK2ME_COMPONENTS = [LabelInfo('Feature: R Packages',
                               desc='',
                               color='cbddf5'),
                     LabelInfo('Feature: NLP Classification',
                               desc='',
                               color='cbddf5'),
                     LabelInfo('Feature: Annotation',
                               desc='',
                               color='cbddf5'),
                     LabelInfo('Feature: Calculator',
                               desc='',
                               color='cbddf5'),]

OPENDP_LABELS_1 = [LabelInfo('OrigSmartNoise',
                             desc='',
                             color='fbca04'),
                   LabelInfo('Blocked',
                             desc='',
                             color='5319e7')]

OPENDP_LABELS_2 = [LabelInfo('DP Component',
                             desc='',
                             color='76D7C4'),
                   LabelInfo('OpenDP Core',
                             desc='',
                             color='b9e27f'),
                   LabelInfo('CSL',
                             desc='',
                             color='AD8244'),
                   LabelInfo('OpenDP Schema',
                             desc='',
                             color='FFC300'),
                   LabelInfo('OpenDP App',
                             desc='',
                             color='d87093'),
                   LabelInfo('v0.1',
                              desc='',
                              color='1DD314'),
                   LabelInfo('Dependencies',
                              desc='',
                              color='0366d6'),
                   LabelInfo('Documentation',
                              desc='',
                              color='0075ca'),
                   LabelInfo('Security',
                              desc='',
                              color='FBCA04'),
                   LabelInfo('Dataverse',
                             desc='',
                             color='ff7619'),
                   LabelInfo('Blocked',
                             desc='',
                             color='5319e7'),]
