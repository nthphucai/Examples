import copy
import gc
import os
import sys
import time

import fastapi
import torch
from fastapi import File, Response, UploadFile, status
from fastapi.openapi.docs import get_swagger_ui_html
from loguru import logger


router = fastapi.APIRouter()


@router.get("/v1/history/healthcheck", include_in_schema=False)
async def healthcheck():
    return {"message": "OK"}


@router.get("/v1/history/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/v1/history/openapi.json",
        title="API",
    )


@router.post("/v1/from_file", status_code=200, tags=["Upload file"])
async def upload_file(response: Response, task: str = "", file: UploadFile = File(...)):
    if isinstance(result, dict):
        response.status_code = status.HTTP_400_BAD_REQUEST
    else:
        start_time = time.time()
        try:
            result = "generate function here"
            result["time"] = round((time.time() - start_time) * 1000, 2)
        except Exception as e:
            logger.exception(e)
            result = {
                "task": task,
                "domain": "history",
                "filename": file.filename,
                "error": "An exception happened",
            }
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            pass

    gc.collect()
    torch.cuda.empty_cache()
    return result
