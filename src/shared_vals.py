"""
- Updated 2/9/23
GitHub API url and headers
"""

from collections import OrderedDict
from os.path import dirname, join

from auth_token import API_TOKEN

GH_API_URL = 'https://api.github.com'
GH_HEADERS = OrderedDict({'Accept': 'application/vnd.github+json',
                          'Authorization': 'Bearer %s' % API_TOKEN,
                          'X-GitHub-Api-Version': '2022-11-28'})

TEST_DATA_DIR = join(dirname(dirname(__file__)), 'test_data')
GITHUB_JSON_DATA_DIR = join(TEST_DATA_DIR, 'github_json')
EXCEL_OUTPUT_DIR = join(TEST_DATA_DIR, 'output')