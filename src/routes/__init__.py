from fastapi import APIRouter
from src.routes.link import router_v1 as link_router_v1
from src.routes.forward import router_v1 as forward_router_v1

from src.schemas.general.error import BaseError

router = APIRouter(responses={404: {"description": "Not found", "model": BaseError}})
router.include_router(link_router_v1)
router.include_router(forward_router_v1)
