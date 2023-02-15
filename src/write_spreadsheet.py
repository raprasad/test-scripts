import json
import os
import sys
from datetime import datetime
from os.path import join

import xlsxwriter

import shared_vals as svals


def get_github_json_files(json_file_prefix):
    """Return the full filepaths of any matching JSON files"""
    data_files = []
    for fname in os.listdir(svals.GITHUB_JSON_DATA_DIR):
        if fname.startswith(json_file_prefix) and fname.lower().endswith('.json'):
            data_files.append(join(svals.GITHUB_JSON_DATA_DIR, fname))

    if not data_files:
        print((f'No JSON data files found for prefix "{json_file_prefix}"'
               f' in directory "{svals.GITHUB_JSON_DATA_DIR}"'))

    return data_files


def write_issues_to_xlsx(json_file_prefix):
    """Write GitHub issues to xlsx"""
    excel_fname = join(svals.EXCEL_OUTPUT_DIR, f'{json_file_prefix}.xlsx')
    workbook = xlsxwriter.Workbook(excel_fname)
    ws = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    col = 0
    row = 0
    time_fmt = '%Y-%m-%dT%H:%M:%SZ'
    time_output_fmt = '%m/%d/%Y'  # "%m/%d/%Y, %H:%M:%S"
    today = datetime.now()

    for hc in get_header_cols():
        ws.write(row, col, hc[0])
        ws.set_column(col, col, hc[1])
        col += 1

    # Get the name of the JSON input files
    json_data_files = get_github_json_files(json_file_prefix)
    if not json_data_files:
        print('No data for Excel file')
        return

    # Iterate through the file data, writing to an XLSX spreadsheet
    file_cnt = 0
    for data_file in json_data_files:
        file_cnt += 1
        print(f'({file_cnt}) Processing file: {data_file}')

        issue_data = json.load(open(data_file, 'r'))

        for info in issue_data:
            col = 0
            row += 1
            ws.write(row, col, info['number'])  # issue number
            ws.write(row, col + 1, info['state'])  # is it open or closed
            ws.write(row, col + 2, info['title'])  # issue title

            # any labels beginning with "org:"
            ws.write(row, col + 3, get_label_info(info['labels'], 'org:'))

            # any labels beginning with "t:"
            ws.write(row, col + 4, get_label_info(info['labels'], 't:'))

            # How many days has the issue been open?
            create_time = datetime.strptime(info['created_at'], time_fmt)
            elapsed_time = today - create_time
            days_elapsed = elapsed_time.days
            if days_elapsed == 0: days_elapsed = 1

            ws.write(row, col + 5, days_elapsed)  # days issue has been open
            ws.write(row, col + 6, create_time.strftime(time_output_fmt))  # create date
            ws.write(row, col + 7, datetime.strptime(info['updated_at'], time_fmt).strftime(time_output_fmt))  # updated date
            ws.write(row, col + 8, info['url'])  # url to issue

    workbook.close()
    print(f'\n\n>> file written: {excel_fname}\n')


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
    """Retrieve applicable labels from issue data"""
    org_labels = [x['name'].replace(label_prefix, '').strip()
                  for x in labels
                  if x['name'].startswith(label_prefix)]
    if not org_labels:
        return ''
    org_labels = ', '.join(org_labels)
    return org_labels


if __name__ == '__main__':
    if len(sys.argv) == 2:
        write_issues_to_xlsx(sys.argv[1])
    else:
        print(('\n\nUsage: python write_spreadsheet.py [file_prefix]'
               '\n\n - file_prefix is the beginning of the name of the JSON data files in'
               ' "../test_data/github_json"'
               ' \n\n - example: "python write_spreadsheet.py issues_opendp_crm_2023-02-15_15-52-25"\n\n'))
        # write_issues_to_xlsx('issues_opendp_crm_2023-02-15_16-04-53')
