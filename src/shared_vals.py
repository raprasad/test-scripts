"""
- Updated 2/9/23
GitHub API url and headers
"""

from collections import OrderedDict
from os import makedirs
from os.path import abspath, dirname, isdir, join

from auth_token import API_TOKEN, GQL_API_TOKEN

CURRENT_DIR = dirname(abspath(__file__))
GRAPHQL_QUERY_DIR = join(CURRENT_DIR, 'graphql_queries')
GRAPHQL_RESULTS = join(dirname(CURRENT_DIR), 'test_data', 'graphql_results')
if not isdir(GRAPHQL_RESULTS):
    makedirs(GRAPHQL_RESULTS)


# REST API
GH_API_URL = 'https://api.github.com'
GH_HEADERS = OrderedDict({'Accept': 'application/vnd.github+json',
                          'Authorization': 'Bearer %s' % API_TOKEN,
                          'X-GitHub-Api-Version': '2022-11-28'})

# GraphQL API
GH_GQL_API_URL = 'https://api.github.com/graphql'
GH_GQL_HEADERS = {'Authorization': 'Bearer %s' % GQL_API_TOKEN}

# Output directories
TEST_DATA_DIR = join(dirname(dirname(__file__)), 'test_data')
GITHUB_JSON_DATA_DIR = join(TEST_DATA_DIR, 'github_json')
EXCEL_OUTPUT_DIR = join(TEST_DATA_DIR, 'output')
