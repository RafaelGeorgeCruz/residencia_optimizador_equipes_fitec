from fastapi import APIRouter
from api.routes.team_router import (
    router as team_router,
)

main_router = APIRouter()

main_router.include_router(
    team_router,
    prefix="/team_details",
    tags=["team_formation_prediction"],
)
