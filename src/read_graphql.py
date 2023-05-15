"""
Iterate through PRs and Related issues
"""
import json
from datetime import datetime
from os.path import isfile, join

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

import shared_vals as svals


def read_graphql_api(output_file_prefix, graphql_query_file):
    """Run a GraphQL query and write the results to a JSON file"""
    print(f'\n--- Running GraphQL query: "{output_file_prefix}" ---\n')

    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url=svals.GH_GQL_API_URL,
                                 headers=svals.GH_GQL_HEADERS)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    graphql_query_filename = join(svals.GRAPHQL_QUERY_DIR, graphql_query_file)
    print(f'> Reading GraphQL query file: {graphql_query_filename}')
    if not isfile(graphql_query_filename):
        print(f'  > GraphQL file not found: {graphql_query_filename}')
        return

    # Read/Prepare GraphQL query
    graphql_query_str = open(graphql_query_filename).read()
    query = gql(graphql_query_str)

    # Execute the query on the transport
    result = client.execute(query)

    # Format output and write to file
    json_str = json.dumps(result, indent=4)

    today_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    json_output_filename = join(svals.GRAPHQL_RESULTS, (f'{output_file_prefix}_{today_str}.json'))
    open(json_output_filename, 'w').write(json_str)
    print(f'> File written: {json_output_filename}\n')


if __name__ == '__main__':
    # read_graphql_api('pr_issue_check', 'pr_issue_check.graphql')
    read_graphql_api('milestone_summary', 'milestone_summary.graphql')
