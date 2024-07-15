from pydantic import BaseModel, Field

from exceptions import TypingError, ServiceError


class LLMGenInput(BaseModel):
    generator_configs: str = Field(
        default="generator_configs",
        description="description",
    )


def generator(GenerateQuery, llm_generator) -> str:

    context_text = GenerateQuery.context
    llm_generator.generate(query=context_text)

    if len(context_text) < 5:
        raise TypingError(message="Invalid input", name="input")

    elif context_text is None:
        raise ServiceError(message="unexpected error", name="unexpected error")

    else:
        return "This is a api testing for generator module"
