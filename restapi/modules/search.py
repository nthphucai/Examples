from pydantic import BaseModel, Field
from exceptions import TypingError, ServiceError


class UserQuery(BaseModel):
    engine_type: str = Field(
        default="engine_type",
        description="description",
    )
    search_configs: str = Field(
        default="search_configs",
        description="description",
    )


def searcher(SearchQuery, search_engine) -> str:

    context_text = SearchQuery.context
    search_engine.search(query=context_text)

    if len(context_text) < 5:
        raise TypingError(message="Invalid input", name="input")

    elif context_text is None:
        raise ServiceError(message="unexpected error", name="unexpected error")

    else:
        return "This is a api testing for searching module"
