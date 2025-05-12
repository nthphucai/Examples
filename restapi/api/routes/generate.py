import gc

import fastapi
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.params import Depends
from .limiter import limiter

from exceptions import TypingError, ServiceError
from fastapi import HTTPException, Request
from modules.generate import generator
from modules.core import LLMGeneratorInit, init_generator
from schemas import GenerateQuery

router = fastapi.APIRouter()


@router.get("/v1/generate/healthcheck", include_in_schema=False)
async def healthcheck():
    return {"message": "OK"}


@router.get("/v1/generate/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/v1/generate/openapi.json",
        title="API",
    )


@router.post("/v1/from_search", status_code=200, tags=["Generate"])
@limiter.limit("1/second")
async def generate(
    request: Request,
    item: GenerateQuery,
    llm_generator: LLMGeneratorInit = Depends(init_generator),
):
    try:
        result = generator(item, llm_generator)

    except TypingError as error:
        raise HTTPException(status_code=404) from error

    except ServiceError as error:
        raise HTTPException(status_code=500) from error

    finally:
        print("save_to_db...")

    gc.collect()
    return result
