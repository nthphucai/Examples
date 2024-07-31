import os

import requests
from fastapi import APIRouter, File, Response, UploadFile, status
from loguru import logger


SERVER = os.getenv("SERVER")
PORT = os.getenv("SERVER_PORT")

router = APIRouter()


@router.post("/v1/from_file", status_code=200)
async def generate_from_file(
    response: Response, task: str = "", domain: str = "", file: UploadFile = File(...)
):
    item = {"task": task, "domain": domain, "filename": file.filename}
    try:
        file_bytes = open(file.filename, "rb")
        result = requests.post(
            SERVER + "/v1/from_file?task=" + task + "&domain=" + domain,
            files=[("files", (file.filename, file_bytes, "application/pdf"))],
            data={},
        )
        response.status_code = result.status_code
        file.close()
        return result
    
    except Exception as e:
        logger.exception(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        item["error"] = "An exception happened"
        return item
