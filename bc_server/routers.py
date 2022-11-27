from fastapi import APIRouter

from bc_server.info_endpoints import info_router

main_router = APIRouter()
main_router.include_router(info_router)
