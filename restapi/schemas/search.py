from typing import List, Union
from pydantic import BaseModel, Field, field_validator


class SearchQuery(BaseModel):
    engine_type: str = Field(
        default="weaviate",
        description="engine_type"
    )
    search_configs: str = Field(
        default="search_configs",
        description="search_configs",
    )
    context: Union[str, List[str]] = Field(description="Input context")



class SearchResponse(BaseModel):
    query: Union[str, List[str]] = Field(description="Input context")

    engine_type: str = Field(
        default="weaviate",
        description="engine_type"
    )
    search_configs: str = Field(
        default="search_configs",
        description="search_configs",
    )
    related_docs: str = Field(
        default="related_docs",
        description="related_docs",
    )
