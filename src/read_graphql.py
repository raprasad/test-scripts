"""
Iterate through PRs and Related issues
"""
import json
from os.path import join
from datetime import datetime

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

import shared_vals as svals

today_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url=svals.GH_GQL_API_URL,
                             headers={'Authorization': 'Bearer %s' % svals.GQL_API_TOKEN}
                             )  # "https://countries.trevorblades.com/")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
graphql_query_str = open(join(svals.GRAPHQL_QUERY_DIR, 'pr_issue_check.graphql')).read()
query = gql(graphql_query_str)

# Execute the query on the transport
result = client.execute(query)
# print(dir(result))
# print(type(result))

json_str = json.dumps(result, indent=4)

pr_issue_check_filename = join(svals.GRAPHQL_RESULTS, (f'pr_issue_check_{today_str}.json'))
open(pr_issue_check_filename, 'w').write(json_str)
print(f'file written: {pr_issue_check_filename}')

