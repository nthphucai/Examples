import streamlit as st
import requests
import httpx
import asyncio


class SearchEngine:
    """
    A client for interacting with a Weaviate backend.
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    async def a_query(self, **data_configs):
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
        async with httpx.AsyncClient(timeout=45) as client:

            response = await client.post(
                self.base_url, json=data_configs, headers=self.headers
            )
            response.raise_for_status()  # Raise an exception for error HTTP status codes
            return response.json()

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


ENDPOINT_URL = "http://0.0.0.0:5050/v1/from_query"


async def a_main():
    st.title("Search Engine Query")

    context = st.text_input("Enter Context:", "this is example query")

    data_configs = {
        "context": context,
        "engine_type": "weaviate",
        "search_configs": "search_configs",
    }

    if st.button("Submit Query"):
        client = SearchEngine(ENDPOINT_URL)
        response = await client.a_query(**data_configs)
        st.write("Response:")
        st.json(response)

def main():
    st.title("Search Engine Query")

    context = st.text_input("Enter Context:", "this is example query")

    data_configs = {
        "context": context,
        "engine_type": "weaviate",
        "search_configs": "search_configs",
    }

    if st.button("Submit Query"):
        client = SearchEngine(ENDPOINT_URL)
        response = client.query(**data_configs)
        st.write("Response:")
        st.json(response)


if __name__ == "__main__":
    #main()
    asyncio.run(a_main())
