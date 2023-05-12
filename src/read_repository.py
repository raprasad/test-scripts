"""
Basic script to read GitHub issues and write them to JSON files
(1) Read the instructions in "auth_token_template.py"
(2) Update your repository in "settings_gh_repo.py"
(3) Run this script: python read_repository.py
(4) Output will be in: ../test_data/github_json
"""
import json
from datetime import datetime
from os.path import join

import requests

import shared_vals as svals
from settings_gh_repo import *

_ISSUES_PER_PAGE = 100


def read_issues():
    """Read GitHub issues. Very basic"""

    # Figure out how many pages of issues
    issues_per_page = _ISSUES_PER_PAGE
    open_issue_count = get_open_issue_count()
    num_issue_pages = int(open_issue_count / issues_per_page)
    if open_issue_count % issues_per_page > 0:
        num_issue_pages += 1

    # Create timestamp for file naming
    today_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # For each page of issues, make an API request
    for page_num in range(1, num_issue_pages + 1):
        print('retrieving page:', page_num)

        # query params, page number changes
        query_params = {'per_page': issues_per_page,
                        'page': page_num}

        # Format the read url.  e.g. https://api.github.com/opendp/crm/issues?per_page=100&page=1
        #
        read_url = (f'{svals.GH_API_URL}/repos/{GH_REPO_OWNER}/'
                    f'{GH_REPO_NAME}/issues')

        # Retrieve the data and format it into a JSON string
        #
        r = requests.get(read_url, params=query_params, headers=svals.GH_HEADERS)

        print('status code:', r.status_code)
        json_resp = r.json()
        json_info_str = json.dumps(json_resp, indent=4)

        # Write the output to a file
        #
        if num_issue_pages == 1:
            page_num_str = 'all'
        else:
            page_num_str = str(page_num).zfill(3)

        #  example: issues_opendp_crm_2023_0215_001.json
        #
        issue_filename = (f'issues_{GH_REPO_OWNER}_{GH_REPO_NAME}'
                          f'_{today_str}_{page_num_str}.json')

        # example: ../test_data/github_json/issues_opendp_crm_2023_0215_001.json
        #
        issue_full_filename = join(svals.GITHUB_JSON_DATA_DIR, issue_filename)
        open(issue_full_filename, 'w').write(json_info_str)
        print('file written:', issue_full_filename)


def get_open_issue_count():
    """Read GitHub repo and pull 'open_issues_count'"""
    read_url = f'{svals.GH_API_URL}/repos/{GH_REPO_OWNER}/{GH_REPO_NAME}'
    r = requests.get(read_url, headers=svals.GH_HEADERS)

    print('status code:', r.status_code)
    json_resp = r.json()

    json_info_str = json.dumps(json_resp, indent=4)
    print(json_info_str)
    return json_resp['open_issues_count']


def list_labels():
    read_url = (f'{svals.GH_API_URL}/repos/{GH_REPO_OWNER}/{GH_REPO_NAME}'
                f'/labels?per_page=100')

    r = requests.get(read_url, headers=svals.GH_HEADERS)

    print('status code:', r.status_code)
    json_resp = r.json()
    print(json.dumps(json_resp, indent=4))
    print('num labels:', len(json_resp))


if __name__ == '__main__':
    read_issues()
