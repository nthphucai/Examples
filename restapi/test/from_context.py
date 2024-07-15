import os

import requests
from fastapi import APIRouter, Response, status
from loguru import logger

from restapi.schemas.generate import FromContextRequestItem


SERVER = os.getenv("SERVER")
PORT = os.getenv("SERVER_PORT")

router = APIRouter()


@router.post("/v1/from_context", status_code=200)
async def generate_from_context(
    response: Response, request_item: FromContextRequestItem
):
    item = {
        "task": request_item.task,
        "domain": request_item.domain,
        "context": request_item.context,
    }
    try:
        result = requests.post(SERVER + "/v1/from_context", json=item)
        response.status_code = result.status_code
        return result
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        item["error"] = "An exception happened"
        return item
