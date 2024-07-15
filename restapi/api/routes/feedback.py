import gc
import os

import fastapi
from fastapi import Response, status
from fastapi.openapi.docs import get_swagger_ui_html
from loguru import logger

from mongodb.mongo_client import connect_mongodb
from questgen.utils.file_utils import get_time
from restapi.schema.context_answer import FeedBack, UserFeedback


CONFIG_PATH = os.getenv(
    "API_FEEDBACK_CONFIG_PATH", "configs/faqg_pipeline_t5_vi_base_hl.yaml"
)
feedback_mongodb = connect_mongodb(CONFIG_PATH, "feedback_collection")
response_mongodb = connect_mongodb(CONFIG_PATH, "response_collection")

router = fastapi.APIRouter()


@router.get("/v1/feedback/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/v1/feedback/openapi.json",
        title="API",
    )


@router.post("/v1/feedback/webapp", include_in_schema=False, status_code=200)
async def webapp_feedback(response: Response, context: FeedBack):
    try:
        if feedback_mongodb is not None:
            try:
                result = {
                    "task": context.task,
                    "domain": context.domain,
                    "results": context.results,
                    "time": context.time,
                    "log_time": get_time(),
                }
                feedback_mongodb.insert_one(result)
                result = {"message": "feedback success"}
            except Exception as e:
                logger.exception(e)
                feedback_mongodb.insert_one({"error": str(e), "log_time": get_time()})
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                result = {"error": "validation error"}
        else:
            logger.error("Can not connect to database")
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            result = {"error": "something wrong with server"}
    except Exception as e:
        logger.exception(e)
    gc.collect()
    return result


@router.post("/v1/feedback/user", include_in_schema=True, status_code=200)
async def feedback(response: Response, request: UserFeedback):
    try:
        if response_mongodb is not None:
            try:
                result = {
                    "task": request.task,
                    "domain": request.domain,
                    "data": request.data,
                    "time": request.time,
                    "label": request.label,
                    "rating": request.rating,
                    "comment": request.comment,
                    "log_time": get_time(),
                }
                response_mongodb.insert_one(result)
                result = {"message": "feedback success"}
            except Exception as e:
                logger.exception(e)
                response_mongodb.insert_one({"error": str(e), "log_time": get_time()})
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                result = {"error": "validation error"}
        else:
            logger.error("Can not connect to database")
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            result = {"error": "something wrong with server"}
    except Exception as e:
        logger.exception(e)
    gc.collect()
    return result
