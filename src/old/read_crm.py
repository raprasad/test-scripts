import json
from os.path import join
from datetime import datetime

import requests
import xlsxwriter
from settings_gh_repo import *
import shared_vals as svals

def read_issues():
    """Read GitHub issues. Very basic"""

    # Figure out how many pages of issues
    issues_per_page = 100
    open_issue_count = get_open_issue_count()
    num_issue_pages = int(open_issue_count / issues_per_page)
    if open_issue_count % issues_per_page > 0:
        num_issue_pages += 1

    # Create timestamp for file naming
    today_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # For each page of issues, make an API request
    for page_num in range(1, num_issue_pages+1):
        print('retrieving page:', page_num)

        # query params, page number changes
        query_params = {'per_page': issues_per_page,
                        'page': page_num}

        # Format the read url.  e.g. https://api.github.com/opendp/crm/issues?per_page=100&page=1
        #
        read_url = (f'{svals.GH_API_URL}/repos/{GH_REPO_OWNER }/'
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
        issue_full_filename = join(svals.TEST_DATA_DIR, 'github_json', issue_filename)
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

def write_issues_to_xlsx(issue_data=None):
    """Write GitHub issues to xlsx"""
    issue_data = json.load(open(crm_issues_fname, 'r'))

    workbook = xlsxwriter.Workbook(crm_excel_fname)
    ws = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    time_fmt = '%Y-%m-%dT%H:%M:%SZ'
    time_output_fmt = '%m/%d/%Y'  # "%m/%d/%Y, %H:%M:%S"
    today = datetime.now()

    for hc in get_header_cols():
        ws.write(row, col, hc[0])
        ws.set_column(col, col, hc[1])
        col += 1

    # Iterate over the data and write it out row by row.
    for info in issue_data:
        col = 0
        row += 1
        ws.write(row, col, info['number'])
        ws.write(row, col + 1, info['state'])
        ws.write(row, col + 2, info['title'])

        ws.write(row, col + 3, get_label_info(info['labels'], 'org:'))
        ws.write(row, col + 4, get_label_info(info['labels'], 't:'))

        # How many days has the issue been open?
        create_time = datetime.strptime(info['created_at'], time_fmt)
        elapsed_time = today - create_time
        days_elapsed = elapsed_time.days
        if days_elapsed == 0: days_elapsed = 1

        ws.write(row, col + 5, days_elapsed)
        ws.write(row, col + 6, create_time.strftime(time_output_fmt))
        ws.write(row, col + 7, datetime.strptime(info['updated_at'], time_fmt).strftime(time_output_fmt))
        ws.write(row, col + 8, info['url'])

    workbook.close()
    print('file written: ', crm_excel_fname)

def get_header_cols():

    header_cols = [('Issue\nNumber', 10),
                   ('Status', 10),
                   ('Title', 50),
                   ('Organization(s)', 20),
                   ('Technology', 20),
                   ('Days Open', 20),
                   ('Created', 20),
                   ('Updated', 20),
                   ('URL', 20),]
    return header_cols

def get_label_info(labels, label_prefix):
    """Retrieve applicable labels"""
    org_labels = [x['name'].replace(label_prefix, '').strip()
                  for x in labels
                  if x['name'].startswith(label_prefix)]
    if not org_labels:
        return ''
    org_labels = ', '.join(org_labels)
    return org_labels


def list_labels():
    read_url = f'{shared_vals.GH_API_URL}/repos/{_REPO_OWNER}/{_REPO_NAME}/labels?per_page=100'
    r = requests.get(read_url, headers=shared_vals.GH_HEADERS)

    print('status code:', r.status_code)
    json_resp = r.json()
    print(json.dumps(json_resp, indent=4))
    print('num labels:', len(json_resp))


"""
curl \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/labels
"""

if __name__ == '__main__':
    read_issues()
    # write_issues_to_xlsx()
    # list_labels()d

"""
curl \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/issues
"""
