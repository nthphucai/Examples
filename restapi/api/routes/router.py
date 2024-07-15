from fastapi import APIRouter, Response
from dotenv import load_dotenv

from api.routes import generate, search


load_dotenv()

router = APIRouter()

router.include_router(search.router, tags=["Search"])
router.include_router(generate.router, tags=["Generate"])


@router.get("/", include_in_schema=False)
async def read_root():
    return Response("Server is serving...")
