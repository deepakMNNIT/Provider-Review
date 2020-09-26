from python_graphql_client import GraphqlClient

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="http://127.0.0.1:5000/")

# Create the query string and variables required for the request.
query = """mutation addResult($pId : Int!, $review : String!, $result : String!){
                    addReview(pId : $pId, review : $review, result : $result) {
                        post {
                            pId,
                            review,
                            result
                        }
                    }
                }"""

variables = {"pId": "1001", "review": "Lengthy and boring.", "result": ""}

# Synchronous request
data = client.execute(query=query, variables=variables)
print(data)  # => {'data': {'country': {'code': 'CA', 'name': 'Canada'}}}

