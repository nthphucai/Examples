from typing import List, Union

from pydantic import BaseModel, Field, field_validator
from exceptions import TypingError


class GenerateQuery(BaseModel):
    task: str = Field(
        default="simple-question",
        description="`simple-question` -> Return the question and the answer;\n`multiple-choice` -> "
        "Return the question and four options for the question (one is the answer);"
        "\n`best-title`: Return the english 'choose the best title' question and answer;",
    )
    domain: str = Field(
        default="english",
        description="`english` -> Return the generation question and answer in English domain;\n`history` -> "
        "Return the question and answer in Vietnamese History domain",
    )
    context: Union[str, List[str]] = Field(description="Input context")


class FeedBack(BaseModel):
    task: str
    domain: str
    results: List[dict] = Field(...)
    time: float = Field(...)


class UserFeedback(BaseModel):
    pass
