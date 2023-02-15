"""
Make some GitHub labels
"""
import sys
from collections import namedtuple, OrderedDict

import requests

from label_info import \
    (LabelInfo,
     ESTIMATE_LABELS,
     ASK2ME_COMPONENTS,
     PRIORITY_LABELS,
     OPENDP_LABELS_1, OPENDP_LABELS_2,
     )
from auth_token import API_TOKEN
import shared_vals

def msg(m): print(m)
def dashes(cnt=40): msg('-' * cnt)
def msgt(m): dashes(); msg(m); dashes()


GH_API_URL = 'https://api.github.com'
GH_HEADERS = OrderedDict(
                    {'Authorization': 'token %s' % API_TOKEN,
                     'Accept': 'application/vnd.github.the-key-preview+json'})

RepositoryInfo = namedtuple('RepositoryInfo', ['owner', 'repos'])


def delete_labels(repo_info, labels):
    """Delete Labels"""
    msgt(f'Delete labels for {repo_info.owner}: {repo_info.repos} ')

    # Iterate through repositories
    #
    for repo in repo_info.repos:
        msg(f'Repository: {repo}')
        # Iterate through labels
        #
        for label_info in labels:

            exists = label_info.does_exist(repo_info.owner, repo)
            #msg('Exists? %s' % exists)

            if exists:
                is_deleted = label_info.delete_label(repo_info.owner, repo)


def apply_labels(repo_info, labels_list, issue_nums):
    """Apply labels to specific issues"""
    #POST /repos/:owner/:repo/issues/:issue_number/labels

    for repo in repo_info.repos:
        msg(f'Repository: {repo}')
        # Iterate through issue numbers
        #
        for issue_number in issue_nums:
            # owner, repo, issue_number, labels_list
            LabelInfo.add_label_to_issue(\
                    repo_info.owner, repo,
                    issue_number, labels_list)

        #for label_info in labels:
        #
        #    exists = label_info.does_exist(repo_info.owner, repo)
        #
        #    if not exists:
        #        is_created = label_info.add_label(repo_info.owner, repo)



def add_labels(repo_info, labels):
    """Add labels to specific respositories"""
    msgt(f'Add labels for {repo_info.owner}: {repo_info.repos} ')

    # Iterate through repositories
    #
    for repo in repo_info.repos:
        msg(f'Repository: {repo}')
        # Iterate through labels
        #
        for label_info in labels:

            exists = label_info.does_exist(repo_info.owner, repo)

            if not exists:
                is_created = label_info.add_label(repo_info.owner, repo)

            #sys.exit(0)


if __name__ == '__main__':
    raven_info = RepositoryInfo('TwoRavens',
                                ['TwoRavens',
                                 'raven-metadata-service',
                                 'common',
                                 'two-ravens-deploy'])

    ask2me_info = RepositoryInfo('ask2me',
                                 ['ask2me-search',
                                  'ask2me-knowledge-tracking',
                                  'abstract-classifier'
                                  ])

    psi_info = RepositoryInfo('privacytoolsproject',
                                 ['PSI-Library',
                                  #'DP-Proposal',
                                  'burdock'
                                  ])


    opendp_orig = RepositoryInfo('opendifferentialprivacy',
                                 ['whitenoise-core-python',
                                  'whitenoise-core',
                                  'whitenoise-samples',
                                  'opendp-schemas',
                                  # -------------
                                  'dp-test-datasets',
                                  #'opendp-ux'
                                  #'OpenDP-Experimental'
                                  ])

    opendp_new = RepositoryInfo('opendifferentialprivacy',
                                 ['opendp-schemas',
                                  #'dp-test-datasets',
                                  'opendp-ux',
                                  'OpenDP-Experimental'
                                  ])

    opendp_new = RepositoryInfo('opendp',
                                 ['opendp',
                                  #'dp-test-datasets',
                                  'opendp-ux',
                                  'smartnoise-core-python',
                                  'smartnoise-core-samples',
                                  #'OpenDP-Experimental'
                                  ])
    # delete_labels(raven_info, ESTIMATE_LABELS)
    # add_labels(raven_info, ESTIMATE_LABELS)
    # add_labels(psi_info, ESTIMATE_LABELS)

    # add_labels(opendp_orig, OPENDP_LABELS_1)
    add_labels(opendp_new, OPENDP_LABELS_2)
    #add_labels(opendp_new, ESTIMATE_LABELS)
    #add_labels(opendp_new, PRIORITY_LABELS)

    #labels_list = ['OpenDP App']
    #apply_labels(opendp_new, labels_list, issue_nums=range(20, 39))
