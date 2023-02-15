import json
from datetime import datetime
from os.path import join

import requests
import xlsxwriter

import shared_vals

crm_issues_fname = join(shared_vals.TEST_DATA_DIR, 'crm_issues.json')
crm_excel_fname = join(shared_vals.TEST_DATA_DIR, 'crm_issues.xlsx')

print('okay')


def runit():
    """Read GitHub issues"""
    print('read issues')
    #session = requests.Session()

    read_url = (f'{shared_vals.GH_API_URL}/repos/{shared_vals.GH_REPO_NAME}'
                f'/{shared_vals.GH_REPO_OWNER}/issues')
    query_params = {"per_page": 100}

    print('read_url', read_url)

    first_page = session.get(read_url, params=query_params, headers=shared_vals.GH_HEADERS)
    yield first_page
    print('first_page:', first_page)

    next_page = first_page
    while get_next_page(next_page) is not None:
        try:
            next_page_url = next_page.links['next']['url']
            next_page = session.get(next_page_url, params=query_params,
                                    headers=shared_vals.GITHUB_AUTH_HEADER)
            yield next_page

        except KeyError:
            print("No more Github pages")
            break

"""
r = requests.get(read_url, headers=shared_vals.GH_HEADERS)

print('status code:', r.status_code)
json_resp = r.json()
json_info_str = json.dumps(json_resp, indent=4)

open(crm_issues_fname, 'w').write(json_info_str)
print('file written:', crm_issues_fname)
"""


def get_next_page(page):
    return page if page.headers.get('link') != None else None


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
                   ('URL', 20), ]
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


if __name__ == '__main__':
    print('huh')
    runit()
    # write_issues_to_xlsx()
    # list_labels()d
