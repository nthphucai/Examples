import gc
import torch
import fastapi
from fastapi import File, Response, UploadFile, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import HTTPException, Request
from fastapi.params import Depends

from .limiter import limiter
from exceptions import TypingError, ServiceError
from modules.search import searcher
from modules.core import init_searcher, SearcherInit
from schemas import SearchQuery

router = fastapi.APIRouter()


@router.get("/v1/search/healthcheck", include_in_schema=False)
async def healthcheck():
    return {"message": "OK"}


@router.get("/v1/search/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/v1/search/openapi.json",
        title="API",
    )


@router.post("/v1/from_query", status_code=200, tags=["Search"])
@limiter.limit("1/second")
async def search(
    request: Request,
    item: SearchQuery,
    search_engine: SearcherInit = Depends(init_searcher),
):
    try:
        result = searcher(item, search_engine)

    except TypingError as error:
        raise HTTPException(status_code=404) from error

    except ServiceError as error:
        raise HTTPException(status_code=500) from error

    finally:
        print("save_to_db...")

    gc.collect()
    torch.cuda.empty_cache()
    return result
