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
    data: dict = Field(
        default={},
        description="""Generated QA results. Example:\n
    {
        "context": "Beethoven was born in Bonn, Germany, in 1770. His childhood was unhappy. His father drank too much.
         Beethoven's musical talent was obvious from childhood. He quickly became a talented performer on the piano.
         In 1792, he moved to Vienna, Austria, to study with Austrian composer Joseph Haydn. Soon Beethoven was
         playing music that he wrote himself.",\n
        "question": "When was Beethoven born?",\n
        "answer": "1770",\n
    }""",
    )
    time: float = Field(default=0, description="Generating QA time")
    label: bool = Field(
        default=False, description="User's acception about generated QA result"
    )
    rating: int = Field(
        default=0, description="Rating for generated QA result. Range from 1 to 5"
    )
    comment: str = Field(
        default="", description="Other user's comment about generated QA result"
    )
