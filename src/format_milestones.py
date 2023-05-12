"""
Create a tabular summary of milestones and issues
"""
import json
import sys
from datetime import datetime
from os.path import isfile, join

import pandas as pd

import shared_vals as svals


class MilestoneFormatter:

    def __init__(self, input_json_fname):
        assert isfile(input_json_fname), "File not found: {input_json_fname}"

        self.milestone_title_prefix_filter = '202'
        self.json_filename = input_json_fname
        self.milestone_input_data = json.load(open(self.json_filename, 'r'))
        self.milestone_output_data = []

        self.today_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.create_milestone_basic_report()
        self.init_data()
        self.create_milestone_issue_report()

    def init_data(self):
        self.milestone_output_data = []

    def create_milestone_basic_report(self):
        """
        Iterate through milestone data
        """
        basic_milestone_data = [self.get_headers_basic_report()]
        milestone_data_list = sorted(self.milestone_input_data['repository']['milestones']['nodes'],
                                     key=lambda d: d['title'])
        for ms in milestone_data_list:
            if ms['title'].startswith(self.milestone_title_prefix_filter):
                ms_data_row = self.process_milestone_basic_report(ms)
                basic_milestone_data.append(ms_data_row)

        self.milestone_output_data = basic_milestone_data

        json_output_filename = join(svals.GITHUB_JSON_DATA_DIR, (f'milestone_basics_{self.today_str}.json'))
        json.dump(self.milestone_output_data, open(json_output_filename, 'w'), indent=2)
        print('file written: ', json_output_filename)

        df = pd.DataFrame(data=self.milestone_output_data[1:],
                          columns=self.milestone_output_data[0])

        csv_filename = join(svals.GITHUB_JSON_DATA_DIR, (f'milestone_basics_{self.today_str}.csv'))
        df.to_csv(csv_filename, index=False)
        print(f'CSV file written: {csv_filename}')

    def process_milestone_basic_report(self, ms):
        """Process a single milestone and its related issues, return a row of dat"""
        num_open_issues = len([i for i in ms['issues']['nodes'] if i['state'] == 'OPEN'])
        num_closed_issues = len([i for i in ms['issues']['nodes'] if i['state'] == 'CLOSED'])

        ms_data_row = [
            ms['id'],
            ms['title'],
            ms['description'],
            ms['url'],
            ms['issues']['totalCount'],
            num_open_issues,
            num_closed_issues,
            ms['progressPercentage'],
            ms['dueOn'],
            ms['createdAt'],
            ms['updatedAt'],
        ]
        return ms_data_row

    def get_headers_basic_report(self):
        """Return a list of column headers"""
        return ['Milestone ID',
                'Milestone Title',
                'Milestone Description',
                'Milestone URL',
                'Issue Count',
                'Open',
                'Closed',
                '% Complete',
                'Due Date',
                'Created Date',
                'Updated Date']

    def create_milestone_issue_report(self):
        """
        Iterate through milestone data
        """
        issues_data = [self.get_headers_issue_report()]
        milestone_data_list = sorted(self.milestone_input_data['repository']['milestones']['nodes'],
                                     key=lambda d: d['title'])
        for ms in milestone_data_list:
            if ms['title'].startswith(self.milestone_title_prefix_filter):
                issue_data_rows = self.process_milestone_issue_report(ms)
                for info in issue_data_rows:
                    issues_data.append(info)

        self.milestone_output_data = issues_data

        df = pd.DataFrame(data=self.milestone_output_data[1:],
                          columns=self.milestone_output_data[0])

        csv_filename = join(svals.GITHUB_JSON_DATA_DIR, (f'milestone_issues_{self.today_str}.csv'))
        df.to_csv(csv_filename, index=False)
        print(f'CSV file written: {csv_filename}')
        #print(df.head())
        sys.exit(0)

        json_output_filename = join(svals.GITHUB_JSON_DATA_DIR, (f'milestone_issues_{self.today_str}.json'))
        json.dump(self.milestone_output_data, open(json_output_filename, 'w'), indent=2)
        print('file written: ', json_output_filename)



    def process_milestone_issue_report(self, ms):
        """Process a single milestone and its related issues, return a row of dat"""
        ms_data_row_start = [
            ms['id'],
            ms['title'],
            ms['url'],
        ]
        issue_data_list = sorted(ms['issues']['nodes'],
                                 key=lambda d: f"{d['state']}-{d['number']}")

        issue_data_rows = []
        for issue_info in issue_data_list:
            # Format effort label
            effort_label = self.retrieve_by_prefix(issue_info['labels']['nodes'], 'Effort')
            priority_label = self.retrieve_by_prefix(issue_info['labels']['nodes'], 'Priority')

            single_issue_data_row = ms_data_row_start + [
                issue_info['id'],
                issue_info['number'],
                issue_info['title'],
                issue_info['bodyText'],
                issue_info['state'],
                effort_label,
                priority_label,
                issue_info['createdAt'],
                issue_info['updatedAt'],
                issue_info['url'], ]
            issue_data_rows.append(single_issue_data_row)

        return issue_data_rows

    def retrieve_by_prefix(self, label_data, label_prefix):
        """Iterate through labels and pull out the one that starts with the prefix"""
        chosen_label = [l['name'] for l in label_data if l['name'].startswith(label_prefix)]
        if chosen_label:
            chosen_label = chosen_label[0]
        else:
            chosen_label = None

        return chosen_label

    def get_headers_issue_report(self):
        """Return a list of column headers"""
        return ['Milestone ID',
                'Milestone Title',
                'Milestone Url',
                'Issue ID',
                'Issue Number',
                'Issue Title',
                'Issue Description',
                'Issue State',
                'Effort',
                'Priority',
                'Issue Created Date',
                'Issue Updated Date',
                'Issue URL',
                ]


if __name__ == '__main__':
    input_json = join(svals.GRAPHQL_RESULTS, 'milestone_summary_2023-05-12_12-58-57.json')
    mf = MilestoneFormatter(input_json)
