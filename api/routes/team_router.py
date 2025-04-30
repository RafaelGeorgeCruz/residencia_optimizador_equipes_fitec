from typing import List
from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException

from api.contracts.team_formation import (
    TeamFormationRequest,
    TeamFormationResponse,
)
from core.application.team_formation_service import create_new_team

router = APIRouter()


@router.post(
    "/team_formation",
    status_code=status.HTTP_200_OK,
    response_model=TeamFormationResponse,
)
def generate_new_team(
    request: Request,
    document_request: TeamFormationRequest,
) -> TeamFormationResponse:
    # * Adicionar o processamento para adicionar um item na base
    if (
        not hasattr(request.app.state, "gemini_model")
        or request.app.state.gemini_model is None
    ):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Gemini Model is not ready",
        )
    try:
        suggested_workers, project_cv = create_new_team(
            arquiteto=document_request.arquiteto,
            front_end=document_request.front_end,
            back_end=document_request.back_end,
            quality_assurance=document_request.quality_assurance,
            iniciante=document_request.iniciante,
            team_description=document_request.team_description,
            gemini_model=request.app.state.gemini_model,
            team_formator=request.app.state.optimization_model,
        )

    except Exception:
        raise HTTPException(
            status_code="500",
            detail="An unexpected error occurred, component was not added to database",
        )

    return TeamFormationResponse(team=suggested_workers, team_details=project_cv)
