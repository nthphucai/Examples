import requests

class SearchEngine:
    """
    A client for interacting with a Weaviate backend.
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def query(self, **data_configs):
        """
        Sends a query to the Weaviate backend.

        Args:
            engine_type (str): The type of engine to use for search.
            search_configs (dict): The search configurations.
            context (str): The context for the search.

        Returns:
            dict: The JSON response from the Weaviate backend.

        Raises:
            requests.exceptions.RequestException: If there's an error making the request.
        """
        
        response = requests.post(self.base_url, json=data_configs, headers=self.headers)
        response.raise_for_status()  # Raise an exception for error HTTP status codes
        return response.json()

# Example usage:
ENDPOINT_URL = "http://0.0.0.0:5050/v1/from_query"

client = SearchEngine(ENDPOINT_URL)

data_configs = {
    "context": "this is example query",
    "engine_type": "weaviate",
    "search_configs": "search_configs",
}

response = client.query(**data_configs)
print(response)


