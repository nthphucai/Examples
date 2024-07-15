from typing import Any
from modules.search import UserQuery
from modules.generate import LLMGenInput


class SearcherInit:
    def __init__(self, **kwargs) -> None:
        self.engine_type = kwargs.get("engine_type", "weaviate")
        self.search_configs = kwargs.get("search_configs", None)

        print(f"***** Init searcher *****")

    def search(self, query) -> Any:
        print(
            f"***** Searcher from query {query} and the configs: {self.search_configs} *****"
        )


def init_searcher():
    user_query = UserQuery(engine_type="engine_type", search_configs="search_configs")
    search_engine = SearcherInit(**user_query.__dict__)
    return search_engine


class LLMGeneratorInit:
    def __init__(self, **kwargs) -> None:
        self.generator_configs = kwargs.get("generator_configs", None)

        print(f"***** Init generator *****")

    def generate(self, query) -> Any:
        print(
            f"***** Init generator from query {query} and the configs: {self.generator_configs} *****"
        )


def init_generator():
    llm_inpt = LLMGenInput(generator_configs="generator_configs")
    llm_generator = LLMGeneratorInit(**llm_inpt.__dict__)
    return llm_generator
